# Panduan Operasional SRE: Standar Isolasi Port VPS & Boundary Zero-Trust
**Dokumen Referensi Arsitektur & Pedoman Teknis Site Reliability Engineering**  
**Penyusun:** Master Guru Judith (`guru`) bersama Tim AI Duckvaulta  
**Target Infrastruktur:** VPS Leohermes (Debian 13, AMD EPYC 9B14, 4 vCPU, 15GB RAM, IP: 34.135.45.195)  
**Versi:** 2.0 (Pemutakhiran 26 Oktober 2026)  

---

## 1. Fondasi Teori & First Principles: Mengapa Port Binding Penting?

Dalam rekayasa sistem keandalan (SRE) dan keamanan informasi, salah kaprah paling fatal adalah menganggap bahwa jika sebuah layanan internal "tidak diberi domain publik", layanan tersebut otomatis aman. 

Secara level kernel Linux (`AF_INET` socket):
1. **Binding `0.0.0.0` (`INADDR_ANY`):**
   Memerintahkan kernel untuk mendengarkan paket TCP pada seluruh antarmuka jaringan yang aktif di mesin (loopback `lo`, antarmuka ethernet `ens3`, dan tunnel internal). Jika port ini tidak diblokir oleh firewall eksternal, siapa pun di internet publik dapat mengirim paket SYN dan membentuk koneksi langsung ke layanan backend.
2. **Binding `127.0.0.1` (`INADDR_LOOPBACK`):**
   Memerintahkan kernel hanya menerima paket yang berasal dari antarmuka loopback lokal. Paket dari luar yang tiba di antarmuka fisik (`ens3`) dengan port tujuan tersebut akan langsung ditolak pada tingkat kernel dengan flag TCP RST/ACK (`errno 111 Connection Refused`) tanpa membebani aplikasi.
3. **Analogi Feynman:**
   Bayangkan VPS sebagai gedung perkantoran dengan satu pintu gerbang utama yang dijaga resepsionis ketat (Nginx pada port 80/443). Ruang penyimpanan uang dan server (Ollama, database, auth service) berada di dalam gedung.
   - Binding `0.0.0.0` sama dengan menjebol dinding luar ruangan server dan memasang pintu langsung ke trotoar jalan raya tanpa satpam.
   - Binding `127.0.0.1` memastikan ruangan server hanya memiliki pintu di dalam koridor gedung, sehingga setiap orang yang ingin masuk wajib melewati resepsionis depan.

---

## 2. Topologi Jaringan & Hasil Audit Empiris

### A. Arsitektur Kompartemen Layanan
```
[ INTERNET PUBLIK ]
        |
    (Port 80/443)
        v
+-------------------------------+
|     NGINX REVERSE PROXY       |  <-- Policy Enforcement Point (PEP)
|   (Edge TLS 1.3 Termination)  |
+---------------+---------------+
                |
                +-------------------+-------------------+
                | (127.0.0.1)       | (127.0.0.1)       | (127.0.0.1)
                v                   v                   v
      +-----------------+   +-----------------+   +-----------------+
      |  Ruang 3D Office|   | Duckvaulta Auth |   | God's Eye View  |
      |   (Port 3001)   |   |   (Port 3002)   |   |   (Port 4173)   |
      +-----------------+   +-----------------+   +-----------------+
                |
                v (127.0.0.1)
      +-----------------+
      |   Ollama LLM    |
      |  (Port 11434)   |
      +-----------------+
```

### B. Matriks Soket Empiris (Hasil Probe 26 Oktober 2026)
- **Port Publik (34.135.45.195):**
  - Port 22 (SSH): OPEN (Akses terenkripsi kunci publik ed25519)
  - Port 80 (HTTP): OPEN (Redirect 301 menuju HTTPS)
  - Port 443 (HTTPS): OPEN (TLS 1.3 dengan cipher suite modern)
  - Port 20128 (Hermes API Gateway): OPEN (Mandatory Bearer Auth, HTTP 401 Unauthorized tanpa token)
- **Port Terisolasi (Ditolak pada 34.135.45.195 dan 10.128.0.2):**
  - Port 3001 (Node.js Ruang 3D): REFUSED (errno 111)
  - Port 3002 (Node.js Auth API): REFUSED (errno 111)
  - Port 4173 (Node.js God's Eye View): REFUSED (errno 111)
  - Port 11434 (Ollama Inference Engine): REFUSED (errno 111)

---

## 3. Boundary Zero-Trust (NIST SP 800-207)

Penerapan standar Zero-Trust Architecture pada node VPS:
1. **Asumsi Pelanggaran Perimeter (Assume Breach):**
   Tidak ada komponen yang dipercaya hanya karena berada dalam satu mesin fisik yang sama. Komunikasi antara reverse proxy dan backend menggunakan socket loopback terisolasi.
2. **Autentikasi Eksplisit pada Setiap Titik Akses:**
   Setiap request API internal yang diproxy melalui Nginx wajib menyertakan token verifikasi JWT atau session cookie yang divalidasi oleh backend auth di port 3002.
3. **Penyusutan Permukaan Serangan (Attack Surface Reduction):**
   Dengan mengunci 4 service internal ke loopback, potensi serangan DoS langsung ke engine model AI (Ollama) atau eksploitasi deserialisasi Node.js dari internet publik berhasil ditekan hingga 0%.

---

## 4. Standar Operasional SRE (SRE Operational Guidelines)

### A. The Four Golden Signals pada Manajemen Port
1. **Latency:**
   - Loopback Socket RTT: < 0.5 ms
   - Public Ingress Nginx TTFB: < 45 ms
   - Alarm: Jika loopback latency > 5.0 ms, periksa saturasi CPU atau penumpukan context-switching di proses Node.js/Ollama.
2. **Traffic:**
   - Ambang batas wajar ingress publik: 50 RPS per IP client.
   - Nginx rate-limiting: Blokir request jika melampaui batas burst `burst=20 nodelay`.
3. **Errors:**
   - HTTP 502 (Bad Gateway) atau HTTP 504 (Gateway Timeout): Indikasi backend upstream mati atau crash loop.
   - Deteksi otomatis: Nginx error log `/var/log/nginx/error.log`.
4. **Saturation:**
   - Socket Descriptor Usage: Pastikan `ulimit -n` mencukupi (default 65535 untuk beban tinggi).
   - Memory RSS: Pantau konsumsi memori Ollama dan Node.js agar tidak memicu Linux Kernel OOM (Out Of Memory) Killer.

### B. Standard Operating Procedure (SOP) Deployment Layanan Baru
Setiap developer atau agen AI yang menambahkan mikroservis baru wajib mengikuti protokol berikut:
1. Konfigurasikan listener server hanya pada `127.0.0.1` atau `localhost`.
2. Larang keras opsi `0.0.0.0`, `::`, atau `*` pada settingan host.
3. Tuliskan reverse proxy block pada konfigurasi Nginx (`/etc/nginx/sites-available/`).
4. Uji validasi konfigurasi dengan `nginx -t`.
5. Terapkan perubahan dengan reload graceful: `nginx -s reload`.
6. Lakukan probe verifikasi eksternal untuk memastikan port baru tidak bocor ke publik.

### C. Runbook Respon Insiden (Socket Exposure Incident)
Jika automated healthcheck mendeteksi port internal terbuka ke IP publik:
1. **Fase 1: Triage Kilat**
   ```bash
   # Cari tahu PID proses yang mendengarkan di port yang bocor
   ss -tulpn | grep :<PORT>
   ```
2. **Fase 2: Mitigasi Darurat**
   - Jika proses dikelola PM2:
     ```bash
     pm2 stop <APP_NAME>
     ```
   - Jika proses dikelola systemd:
     ```bash
     systemctl --user stop <SERVICE_NAME>
     ```
   - Tambahkan aturan darurat iptables jika proses tidak dapat dimatikan:
     ```bash
     sudo iptables -I INPUT -p tcp --dport <PORT> ! -s 127.0.0.1 -j DROP
     ```
3. **Fase 3: Remediasi Permanen**
   Perbaiki binding pada source code atau unit service, lalu jalankan kembali layanan dan verifikasi ulang dengan skrip probe.

---

## 5. Matriks Best Practices Hardening (Defense-in-Depth)

Keamanan yang tangguh tidak hanya mengandalkan satu dinding pertahanan. Pendekatan defense-in-depth Duckvaulta mencakup 4 lapis:

### Lapis 1: Strict Application Code Binding
Pastikan kode inisialisasi server mendefinisikan loopback secara eksplisit:
- **Node.js / Express:**
  ```javascript
  const PORT = process.env.PORT || 3001;
  const HOST = '127.0.0.1';
  app.listen(PORT, HOST, () => {
    console.log(`Server aman aktif di http://${HOST}:${PORT}`);
  });
  ```
- **Vite / Nuxt / Next.js:**
  ```javascript
  // vite.config.js
  export default {
    server: {
      host: '127.0.0.1',
      port: 4173
    }
  }
  ```
- **Python / FastAPI / Uvicorn:**
  ```python
  uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)
  ```

### Lapis 2: Systemd Unit Sandboxing & Network Namespaces
Gunakan fitur isolasi bawaan systemd pada file unit (`~/.config/systemd/user/<service>.service`):
```ini
[Unit]
Description=Layanan Mikroservis Terisolasi
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/node /path/to/server.js
Restart=always

# Isolasi Jaringan Socket Level Systemd
IPAddressAllow=localhost
IPAddressDeny=any

# Sandboxing Hak Akses File System
ProtectSystem=strict
ProtectHome=read-only
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=default.target
```

### Lapis 3: Host Firewall (Packet Filter Level OS)
Konfigurasi UFW atau nftables standar untuk memastikan paket yang lolos ke antarmuka fisik langsung di-drop:
```bash
# Setel default policy
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Izinkan loopback penuh
sudo ufw allow in on lo to any

# Izinkan hanya port publik resmi
sudo ufw allow 22/tcp comment 'SSH Secure Access'
sudo ufw allow 80/tcp comment 'Nginx HTTP Ingress'
sudo ufw allow 443/tcp comment 'Nginx HTTPS Ingress'

# Aktifkan firewall
sudo ufw enable
```

### Lapis 4: Cloud VPC Ingress Firewall Rules
Pada tingkat Google Cloud Platform (GCP Console / `gcloud compute firewall-rules`):
- Target Tags: `http-server`, `https-server`
- Allowed Protocols/Ports: `tcp:80`, `tcp:443`, `tcp:22`
- Denied Ingress: All other TCP/UDP ports dari `0.0.0.0/0`.

---

## 6. Integrasi & Orkesktrasi Tim AI

Dokumentasi dan audit berkala ini diorkestrasi melalui kolaborasi multi-agent:
- **Leader (Orchestrator):** Manajemen roadmap, dekomposisi task pada Kanban board, dan rilis repositori git.
- **trend-hunter (`t_2860d558`):** Intelijen standar industri, adopsi NIST SP 800-207, dan benchmarking arsitektur zero-trust.
- **fullstack-dev (`t_313646a1`):** Implementasi reverse proxy upstream, inspeksi struktur soket Linux, dan tuning Nginx.
- **qa-engineer (`t_3c8ebed1`):** Otomasi pen-testing soket TCP, regression testing jaringan, dan pengujian boundary failure.
- **security-engineer (`t_5bba7a95`):** Validasi layer pertahanan berlapis, token guard gateway, dan audit telemetri host.
- **guru (`t_40518c57`):** Sintesis operasional SRE, verifikasi boundary zero-trust, kurikulum edukatif, dan best practices hardening.
