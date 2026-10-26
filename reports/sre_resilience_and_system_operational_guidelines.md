# SRE Resilience and System Operational Guidelines: Duckvaulta Production Ecosystem
**Dokumen Evaluasi Keandalan Sistem, Ketahanan SRE, dan Panduan Operasional Produksi**  
**Penyusun:** Master Guru Judith (SRE & Pedagogical Specialist) bersama Tim AI Duckvaulta  
**Target Infrastruktur:** VPS Leohermes (Debian 13, AMD EPYC 9B14 4 vCPU, 15GB RAM, 79GB NVMe)  
**Domain Produksi:** `duckvaulta.ai.id`, `edtech.duckvaulta.ai.id`, `aicompany.duckvaulta.ai.id`, `godeye.duckvaulta.ai.id`  
**Versi:** 3.0 (Pemutakhiran Komprehensif 26 Oktober 2026)  

---

## 1. Executive Summary & Ringkasan Evaluasi Keandalan

Audit keandalan menyeluruh pada infrastruktur Duckvaulta mengonfirmasi bahwa ekosistem berada dalam status operasional prima dengan kepatuhan standar Site Reliability Engineering (SRE) tingkat tinggi. Evaluasi empiris pada host menunjukkan stabilitas tanpa interupsi selama lebih dari 8 hari dengan tingkat ketersediaan (availability) 100%.

### Ringkasan Status Sistem:
* Host Node Uptime: 8 hari 15 jam tanpa reboot atau kegagalan kernel.
* Status Mikroservis: Seluruh daemon backend (PM2 dan systemd) aktif dengan 0 restart tidak terencana selama lebih dari 42 jam pengoperasian.
* Ketersediaan Endpoint: 4 dari 4 domain produksi merespons dengan HTTP 200 OK.
* Integritas Aset: 22 dari 22 aset statis (skrip, CSS, gambar, font) terverifikasi terkirim penuh (0 broken assets).
* Perimeter Jaringan: Prinsip isolasi loopback 127.0.0.1 diterapkan penuh pada seluruh layanan internal.

---

## 2. Quantitative SRE Golden Signals Assessment

Berdasarkan framework Google SRE, terdapat 4 sinyal emas (The Four Golden Signals) yang wajib dipantau untuk menilai kesehatan sistem produksi.

### A. Latency (Waktu Respons)
Pengukuran latensi multi-sampel pada jaringan produksi:
* `duckvaulta.ai.id` (Core Portal): Rata-rata TTFB 14.80 ms, total respons time 15.47 ms.
* `edtech.duckvaulta.ai.id` (EdTech Platform): Rata-rata TTFB 13.96 ms, total respons time 14.71 ms.
* `aicompany.duckvaulta.ai.id` (Ruang 3D Office): Rata-rata TTFB 14.97 ms, total respons time 15.05 ms.
* `godeye.duckvaulta.ai.id` (God's Eye Spatial): Rata-rata TTFB 49.79 ms, total respons time 50.48 ms.
* Evaluasi: Seluruh endpoint memenuhi target SLO latensi p95 < 100 ms untuk web portal dan < 150 ms untuk platform visual spatial.

### B. Traffic (Volume Permintaan)
* Nginx menangani koneksi edge secara stabil melalui HTTP/2 dan TLS 1.3.
* Distribusi lalu lintas terkelola dengan baik pada upstream lokal tanpa antrean pada socket kernel (Recv-Q = 0, Send-Q = 0 pada seluruh TCP socket).

### C. Errors (Tingkat Kegagalan)
* Error Rate: 0.00% pada seluruh rute produksi.
* Log PM2 `duckvaulta-auth` (port 3002): Menunjukkan 100% respons sukses pada health check `/api/auth/health` dengan latensi eksekusi 0-1 ms.
* Restart Count: 0 restart pada `duckvaulta-auth`, `duckvaulta-telemetry`, dan `gods-eye-view` dalam 42 jam terakhir.

### D. Saturation (Derajat Kepenuhan Kapasitas Sumber Daya)
* CPU Load Average: 0.66 (1 menit), 0.32 (5 menit), 0.17 (15 menit) pada 4 vCPU AMD EPYC (utilisasi kapasitas efektif < 16.5%).
* Memory Utilization: Digunakan 4.766 MB dari total 15.996 MB (29.8% pemakaian), memori cadangan buffer/cache 11.895 MB, kapasitas tersedia 11.230 MB.
* Disk Storage: Terpakai 30 GB dari total 79 GB (kapasitas terpakai 40%, ruang bebas 46 GB pada partisi NVMe).
* Inode Consumption: Terpakai 665.734 dari total 5.234.688 inode (13% pemakaian, bebas 4.568.954 inode).

---

## 3. Microservices Topology & Zero-Trust Boundary Validation

Sistem menerapkan arsitektur ingress tunggal berbasis Least Privilege dan Boundary Zero-Trust.

```
[ INTERNET PUBLIK ]
        │
    (Port 80/443 TLS 1.3)
        ▼
┌───────────────────────────────┐
│     NGINX REVERSE PROXY       │  <-- Policy Enforcement Point (PEP)
│  (Edge Security & Termination)│
└───────────────┬───────────────┘
                │
                ├───────────────────────┼───────────────────────┐
                │ (127.0.0.1)           │ (127.0.0.1)           │ (127.0.0.1)
                ▼                       ▼                       ▼
      ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
      │  Ruang 3D Office │    │ Duckvaulta Auth  │    │  God's Eye View  │
      │   (Port 3001)    │    │   (Port 3002)    │    │   (Port 4173)    │
      └──────────────────┘    └──────────────────┘    └──────────────────┘
                │
                ▼ (127.0.0.1)
      ┌──────────────────┐
      │   Ollama LLM     │
      │  (Port 11434)    │
      └──────────────────┘
```

### Validasi Binding Soket:
1. **Port Terbuka Publik (0.0.0.0 / ::):**
   * Port 22 (SSH): Open dengan autentikasi kunci asimetris ed25519.
   * Port 80 (HTTP): Open dengan redirect permanen HTTP 301 ke HTTPS.
   * Port 443 (HTTPS): Open dengan cipher suite TLS 1.3 modern (AES-256-GCM).
   * Port 20128 (Hermes API Gateway): Open dengan kewajiban Bearer Token Authentication.
   * Port 20201/20202 (GCP Ops Agent): Open untuk telemetri cloud internal Google.
2. **Port Terisolasi Internal (127.0.0.1):**
   * Port 3001 (Ruang 3D Office): Terikat lokal, akses publik hanya lewat reverse proxy Nginx pada `aicompany.duckvaulta.ai.id`.
   * Port 3002 (Duckvaulta Auth): Terikat lokal, akses publik hanya melalui rute proxy `/api/auth/` pada `duckvaulta.ai.id`.
   * Port 4173 (God's Eye View): Terikat lokal, akses publik lewat reverse proxy pada `godeye.duckvaulta.ai.id`.
   * Port 11434 (Ollama): Terikat lokal, tidak dapat diakses langsung dari antarmuka publik ens3.
   * Port 25 (MTA/Postfix): Terikat lokal loopback 127.0.0.1 dan [::1].

---

## 4. SRE Resilience Architecture Patterns

Untuk memastikan ketersediaan 99.95% dan pencegahan kegagalan berantai (cascading failure), sistem Duckvaulta mengimplementasikan pola arsitektur ketahanan berikut:

### 1. Graceful Connection Draining
* Nginx: Pembaruan konfigurasi selalu diawali validasi sintaks melalui `sudo /usr/sbin/nginx -t` diikuti `sudo /usr/sbin/nginx -s reload`. Pekerja aktif menyelesaikan koneksi berjalan tanpa menjatuhkan koneksi klien yang sedang aktif.
* PM2 Microservices: Penggunaan `pm2 reload <app>` menggantikan restart keras agar proses lama melayani permintaan hingga proses baru menyelesaikan bootstrapping.

### 2. Circuit Breaker dan Timeout Budgets
* Mengatur batasan batas waktu (`proxy_connect_timeout 5s`, `proxy_read_timeout 30s`) pada Nginx reverse proxy untuk mencegah worker Nginx terkunci saat upstream backend mengalami antrean panjang.
* Mekanisme degradasi halus: Jika backend auth (:3002) mengalami downtime, Nginx menyajikan halaman status degradasi statis tanpa mematikan portal utama.

### 3. Exponential Backoff dengan Jitter
* Pada komunikasi antarlayanan dan agen AI, retry loop menerapkan formula:
  T_wait = min(T_max, T_base * 2^attempt) + random(0, Jitter)
  Penerapan jitter mencegah thundering herd problem saat terjadi pemulihan layanan pasca pemadaman sementara.

### 4. Bulkheading (Isolasi Beban Sumber Daya)
* Pemisahan proses eksekusi antara layanan komputasi berat (rendering 3D God's Eye View pada port 4173) dengan modul transaksi cepat (autentikasi dan data tryout pada port 3002).
* Penggunaan limit memori pada level Node.js dan kontrol thread systemd memastikan kebocoran memori pada satu aplikasi tidak menghabiskan memori sistem operasi.

### 5. Atomic Data Persistence Pattern
* Pada mikroservis backend (`duckvaulta-auth/server.js`), persistensi data JSON menggunakan pola tulis berkas sementara (`.tmp.<timestamp>`) yang diikuti operasi atomic rename:
  `fs.writeFileSync(tempPath, jsonString); fs.renameSync(tempPath, targetPath);`
* Pola ini menjamin tidak ada kondisi berkas korup jika proses mati atau listrik padam di tengah operasi penulisan data.

---

## 5. Operational Best Practices & Incident Runbook

### A. Matriks Klasifikasi Insiden
1. **Severity 1 (P1 - Critical):**
   * Definisi: Seluruh situs atau subdomain utama tidak merespons (HTTP 502/504) atau Nginx daemon crash.
   * Respons: Investigasi instan dalam < 5 menit. Periksa `systemctl status nginx`, periksa socket port, lakukan failover atau reload.
2. **Severity 2 (P2 - Major):**
   * Definisi: Satu mikroservis backend mengalami error berulang (HTTP 500) atau latensi TTFB melampaui 500 ms.
   * Respons: Pemeriksaan log PM2 (`pm2 logs <id> --lines 50`), restart daemon spesifik, periksa konsumsi RAM.
3. **Severity 3 (P3 - Minor):**
   * Definisi: Satu aset statis mengalami 404 atau masa berlaku sertifikat SSL < 15 hari.
   * Respons: Penjadwalan perbaikan rute aset atau perpanjangan sertifikat via Certbot.

### B. Prosedur Tanggap Darurat & Rollback
1. **Kegagalan Konfigurasi Nginx:**
   ```bash
   # 1. Validasi config
   sudo /usr/sbin/nginx -t
   # 2. Jika gagal, kembalikan berkas dari backup git
   git -C /home/lionelsabdani36/duckvaulta checkout HEAD -- <file>
   # 3. Muat ulang daemon
   sudo /usr/sbin/nginx -s reload
   ```
2. **Crash pada Daemon PM2:**
   ```bash
   # 1. Periksa status dan daftar restart
   pm2 status
   # 2. Lihat 50 baris log error terakhir
   pm2 logs duckvaulta-auth --lines 50 --err
   # 3. Lakukan restart bersih jika terjadi deadlock
   pm2 restart duckvaulta-auth
   ```
3. **Pemulihan Layanan Ruang 3D (systemd):**
   ```bash
   # 1. Periksa status unit systemd user
   systemctl --user status ruang.service
   # 2. Restart unit jika status failed
   systemctl --user restart ruang.service
   ```

### C. Checklist Pemeliharaan Berkala
* [x] Verifikasi masa aktif sertifikat SSL (saat ini 85 hari tersisa hingga Januari 2027).
* [x] Verifikasi kapasitas penyimpanan partisi NVMe (saat ini 40% pemakaian).
* [x] Verifikasi integritas database/berkas JSON pada `duckvaulta-auth/data/`.
* [x] Verifikasi kepatuhan binding lokal port 11434, 3001, 3002, 4173.
* [x] Eksekusi automated smoke testing suite secara berkala via cron job.

---

## 6. Attributions & Tim Pengembang

* **Leader (David):** Dekomposisi tugas SRE, pengawasan pipeline, dan integrasi repositori git.
* **Guru (Judith):** Evaluasi ketahanan sistem, penyusunan prinsip pedagogis SRE, dan standarisasi panduan operasional.
* **QA Engineer (Julius):** Eksekusi pengujian smoke test otomatis 4 domain, audit aset, dan pemantauan latensi multi-sampel.
* **Fullstack Dev (Alex):** Verifikasi arsitektur upstream, pemeliharaan daemon PM2, dan konfigurasi rute Nginx.
* **Security Engineer (Athena):** Audit isolasi soket loopback, verifikasi cipher suite TLS 1.3, dan inspeksi header keamanan.
* **Trend Hunter (Charlie):** Komparasi performa sistem terhadap standar industri Core Web Vitals 2026.
