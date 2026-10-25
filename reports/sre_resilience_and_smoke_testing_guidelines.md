# SRE Resilience Standards, Incident Prevention & Smoke Testing Guidelines
**Dokumen Standar Keandalan Sistem & Rekayasa SRE Ekosistem Duckvaulta**  
**Penyusun:** Master Guru Judith (`guru`) — SRE & Resilience Specialist  
**Target Infrastruktur:** `duckvaulta.ai.id`, `edtech.duckvaulta.ai.id`, `aicompany.duckvaulta.ai.id`, `godeye.duckvaulta.ai.id`  
**Klasifikasi:** Standar Arsitektur Produksi & Pedoman Pelatihan Kompetensi SRE  
**Tanggal Rilis:** 25 Oktober 2026  

---

## 1. Executive Summary & SRE Architectural Topology

Keandalan sistem (Reliability) bukanlah hasil kebetulan atau "harapan" (Hope is not a strategy), melainkan buah dari rekayasa arsitektural yang terukur, dapat diuji secara kontinu, dan tangguh terhadap kegagalan komponen (fault-tolerant).

Ekosistem Web Duckvaulta berjalan di atas single-node multi-tier architecture pada AMD EPYC 9B14 (4 vCPU, 15GB RAM, 79GB NVMe) dengan topologi layanan sebagai berikut:

```
                      [ INTERNET / KLIEN LUAR ]
                                 │
                   (Port 80/443 TLS 1.3 / HTTP/2)
                                 ▼
                     ┌───────────────────────┐
                     │   NGINX REVERSE PROXY │
                     │  (Edge Security & SSL)│
                     └───────────┬───────────┘
                                 │
      ┌──────────────────────────┼──────────────────────────┐
      │ (Static + Proxy)         │ (Reverse Proxy)          │ (Reverse Proxy)
      ▼                          ▼                          ▼
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│ duckvaulta.ai.id │    │ aicompany...     │    │ godeye...        │
│ & edtech...      │    │ (3D Office)      │    │ (God's Eye View) │
│ Root: /var/www/  │    │ Svc: ruang       │    │ PM2 Vite Daemon  │
│ Proxy: :3002     │    │ Socket: :3001    │    │ Socket: :4173    │
└────────┬─────────┘    └──────────────────┘    └──────────────────┘
         │
         ▼
┌──────────────────┐
│ duckvaulta-auth  │
│ (Node.js API)    │
│ PM2 Port: 3002   │
└──────────────────┘
```

### Karakteristik & Titik Kritis (Failure Domains)
1. **Edge Proxy Single-Point:** Nginx bertindak sebagai ingress tunggal. Jika konfigurasi Nginx crash atau reload gagal, seluruh 4 subdomain offline.
2. **Upstream Daemons Heterogen:**
   - `:3001` (Ruang 3D Office): Systemd user service (`ruang.service` / Node.js).
   - `:3002` (Duckvaulta Auth & EdTech API): PM2 process daemon (`duckvaulta-auth` / Node.js).
   - `:4173` (God's Eye View): PM2 process daemon (`gods-eye-view` / Vite preview).
   - `:20128` (Hermes Gateway / 9Router): Daemon perantara toolset & AI agents.
3. **Loopback Binding Isolation:** Seluruh upstream daemons terikat secara eksklusif ke `127.0.0.1`, mencegah paparan port langsung ke antarmuka publik `ens3`.

---

## 2. Service Level Engineering: SLI, SLO, SLA & Error Budgets

Penerapan prinsip Google SRE menuntut pengukuran kuantitatif terhadap kepuasan pengguna.

### A. Metrik Inti (The Four Golden Signals)
1. **Latency:** Waktu yang dibutuhkan untuk merespons permintaan.
2. **Traffic:** Beban permintaan yang masuk per satuan waktu (RPS/QPS).
3. **Errors:** Rasio permintaan yang gagal (HTTP 5xx, koneksi putus, timeout) terhadap total permintaan.
4. **Saturation:** Derajat kepenuhan sumber daya (CPU utilization, RAM usage, file descriptors, disk I/O).

### B. Rumus & Spesifikasi Target Layanan

| Domain Layanan | SLI (Service Level Indicator) | Target SLO | Toleransi Downtime (Error Budget) |
|---|---|---|---|
| **duckvaulta.ai.id** (Portal) | Rasio respons HTTP 200 dalam waktu < 50ms | **99.95%** | 21,6 menit / bulan |
| **edtech.duckvaulta.ai.id** | Rasio ketersediaan endpoint auth & tryout | **99.90%** | 43,8 menit / bulan |
| **godeye.duckvaulta.ai.id** | Rasio keberhasilan spatial tile load < 150ms | **99.80%** | 87,6 menit / bulan |
| **aicompany.duckvaulta.ai.id** | Rasio koneksi WebRTC/WebSocket stabil | **99.50%** | 3,65 jam / bulan |

### C. Matematika Error Budget & Multi-Window Burn Rate
Error budget dihitung sebagai:
$$\text{Error Budget} = 1 - \text{SLO}$$
Untuk target 99.9% pada 1.000.000 request per bulan, kuota kegagalan maksimal adalah 1.000 request.

**Kebijakan Burn Rate Alerting:**
- **Burn Rate 14.4x (1-hour window):** Menghabiskan 2% error budget dalam 1 jam. Tindakan: Paging darurat level P1 (Immediate incident response).
- **Burn Rate 6x (6-hour window):** Menghabiskan 5% error budget dalam 6 jam. Tindakan: Notifikasi darurat level P2 ke channel Discord/Telegram.
- **Burn Rate 1x (30-day window):** Habis tepat waktu. Status: Stabil / Normal.

---

## 3. Resilience Architectural Patterns

Untuk memastikan zero-downtime dan stabilitas mikroservis, sistem Duckvaulta menerapkan 5 pola ketahanan arsitektural:

### 1. Graceful Connection Draining & Zero-Downtime Reloads
- **Nginx Reloading:** Dilarang keras menggunakan `systemctl restart nginx` saat traffic aktif. Gunakan `nginx -t && nginx -s reload`. Nginx master process akan membaca config baru, menyalakan worker baru, dan membiarkan worker lama menyelesaikan koneksi aktif (*connection draining*) sebelum terminasi.
- **PM2 Zero-Downtime Reload:** Gunakan `pm2 reload all` sebagai pengganti `pm2 restart all`. PM2 akan merestart proses satu per satu tanpa menjatuhkan port upstream.

### 2. Circuit Breaker Pattern (Sekring Pelindung)
Mencegah cascading failures saat upstream backend `:3002` atau model eksternal mengalami penurunan performa:
- **Closed State:** Semua traffic diarahkan normal.
- **Open State:** Jika error rate melebihi 20% dalam 10 detik terakhir, sirkuit terbuka (trip). Request langsung dijawab fallback cache (HTTP 503 degraded atau static offline page) tanpa membebani backend.
- **Half-Open State:** Setelah interval cooldown 30 detik, beberapa request sampel dilewatkan untuk menguji kesehatan upstream. Jika sukses, status kembali ke *Closed*.

### 3. Exponential Backoff dengan Random Jitter
Mencegah fenomena **Thundering Herd Problem** (ketika ribuan klien atau agen AI melakukan retry secara bersamaan setelah terjadi gangguan jaringan):
$$T_{\text{wait}} = \min(T_{\max}, T_{\text{base}} \times 2^{\text{attempt}}) + \text{rand}(0, J)$$
Di mana:
- $T_{\text{base}} = 500\text{ ms}$
- $T_{\max} = 10.000\text{ ms}$
- $J = \text{jitter acak antara } 0 - 250\text{ ms}$

### 4. Bulkheading (Kompartementalisasi Sumber Daya)
Membatasi alokasi resource antar-layanan agar lonjakan beban pada satu layanan (misal: God's Eye 3D rendering) tidak menenggelamkan layanan esensial lainnya (Duckvaulta Auth):
- Isolasi proses via systemd slices dan PM2 cluster limit.
- Batasan `worker_connections` dan `keepalive_timeout` pada Nginx disetel per upstream.

### 5. Adaptive Rate Limiting & Concurrency Shedding
Penerapan `limit_req_zone` pada Nginx untuk menangkal serangan brute-force dan crawler agresif:
```nginx
limit_req_zone $binary_remote_addr zone=portal_limit:10m rate=30r/s;
limit_req_zone $binary_remote_addr zone=auth_limit:10m rate=5r/s;
```

---

## 4. Smoke Testing: Metodologi & Otomasi Validasi Kontinu

Smoke Testing (Sanity Testing) adalah pengujian kilat non-destruktif untuk memvalidasi fungsi vital dan integritas aset sistem sebelum atau sesudah rilis produksi.

### A. Anatomi Smoke Test Suite Duckvaulta (`smoke_test_portals.py`)
Pengujian smoke test otomatis di Duckvaulta mengeksekusi 4 lapisan verifikasi:

```
┌────────────────────────────────────────────────────────┐
│               LAPISAN 1: NETWORK TIMING                │
│ DNS Lookup ➔ TCP Handshake ➔ TLS Handshake ➔ TTFB ➔ Transfer
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│              LAPISAN 2: PROTOKOL & STATUS              │
│ Status Code 200 OK ➔ HTTP/2 Protocol ➔ TLS 1.3 Active  │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│              LAPISAN 3: KEAMANAN KONTRAK               │
│ HSTS Preload ➔ CSP Active ➔ X-Frame-Options ➔ Nosniff  │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│          LAPISAN 4: INTEGRITAS ASET (ZERO 404)         │
│ Crawl DOM ➔ Parse CSS url() ➔ Resolve JS Module Imports │
│ ➔ 100% Asset Delivery Verification (Scripts, Styles,   │
│   Images, Fonts, Icons, Manifests)                     │
└────────────────────────────────────────────────────────┘
```

### B. Validasi Latensi Real-Time Terkini
Berdasarkan audit benchmark terbaru:
- **Duckvaulta Core Portal:** TTFB rata-rata **12.04 ms** (Total: 12.69 ms). DNS: 0.96 ms, TLS: 11.64 ms.
- **God's Eye View:** TTFB rata-rata **29.94 ms** (Total: 30.52 ms). DNS: 1.06 ms, TLS: 12.88 ms.
- **Integritas Aset:** 17 dari 17 aset (100%) lolos dengan kode status 200 OK, zero broken assets terdeteksi.

### C. Kebijakan Pipeline CI/CD & Cron Gating
Smoke test diintegrasikan dalam 3 tahapan siklus hidup sistem:
1. **Pre-Deployment Smoke Gate:** Dijalankan sebelum git merge ke `main`. Jika broken asset > 0 atau status != 200, build otomatis di-abort.
2. **Post-Deployment Smoke Verification:** Dijalankan secara otomatis 5 detik setelah Nginx reload atau PM2 restart.
3. **Continuous Synthetic Cron:** Dijalankan secara periodik via cronjob atau daemon telemetry untuk mendeteksi degradasi performa sebelum dilaporkan oleh user.

---

## 5. Incident Prevention, Detection & Blameless Post-Mortem

### A. Failure Mode and Effects Analysis (FMEA)

| Komponen | Potensi Kegagalan | Efek / Dampak | Mekanisme Pencegahan | Aksi Pemulihan Otomatis |
|---|---|---|---|---|
| **Nginx** | Kesalahan sintaks saat reload | Web server menolak traffic baru | `nginx -t` wajib lolos sebelum reload | Skrip membatalkan update dan rollback file `.conf` |
| **PM2 Daemons** | Uncaught exception / memory leak | Endpoint 502 Bad Gateway | Max-memory-restart 300MB, error handling catch-all | PM2 auto-restart dalam < 2 detik |
| **SSL / Let's Encrypt** | Sertifikat kedaluwarsa | Browser menampilkan security warning merah | Cron renewal mingguan + alert pada H-30 | Certbot auto-renew via Let's Encrypt API |
| **Disk Storage** | Log overflow / scratch space penuh | Sistem operasi menolak penulisan file | Logrotate aktif, retensi log maksimal 14 hari | Skrip pembersih otomatis membersihkan TMPDIR |
| **SQLite DB** | Database locked (`SQLITE_BUSY`) | Transaksi antrean gagal / timeout | Mode WAL (`PRAGMA journal_mode=WAL`), timeout 5000ms | Retry handler dengan jitter backoff |

### B. Matriks Eskalasi Insiden
- **Taraf P1 (Critical Outage):** Subdomain utama down, TTFB > 2000ms, atau data corruption.
  - *Response Time Target:* < 5 Menit.
  - *Aksi:* Otomatisasi failover, notifikasi sirene Discord/Telegram, status card lock.
- **Taraf P2 (Major Degradation):** Salah satu modul internal bermasalah (misal: spatial layer rendering lambat), TTFB 500-2000ms.
  - *Response Time Target:* < 30 Menit.
  - *Aksi:* Graceful degradation, pemulihan instance PM2 sekunder.
- **Taraf P3 (Minor Glitch):** Broken asset non-kritis (misal: favicon sekunder), anomali log ringan.
  - *Response Time Target:* < 4 Jam.
  - *Aksi:* Tiket backlog kanban, perbaikan terjadwal.

### C. Budaya Blameless Post-Mortem
Setiap kali terjadi insiden produksi (P1 atau P2), tim wajib menyusun laporan evaluasi tanpa menyalahkan individu (*blameless culture*). Fokus evaluasi adalah:
1. **Timeline Kronologis Kejadian:** Dari deteksi awal (TTD) hingga perbaikan tuntas (TTR).
2. **5 Whys Analysis:** Menelusuri rantai kausalitas hingga ke akar struktural/proses, bukan kelalaian manusia.
3. **Action Items (Preventative Fixes):** Langkah konkret untuk menjamin insiden yang persis sama mustahil terulang di masa depan.

---

## 6. Pedagogi SRE Masterclass: Bedah Distraktor & Jebakan Konsep

Sebagai materi pengayaan kompetensi untuk White Jack dan tim engineering, berikut adalah bedah distractor/anti-pattern paling berbahaya dalam dunia keandalan sistem:

### Jebakan 1: "The Zombie 200 OK" (Ilusi Sehat Palsu)
- **Miskonsepsi:** Banyak engineer mengira jika monitoring HTTP mengembalikan kode `200 OK`, maka aplikasi pasti berjalan normal.
- **Realitas:** Web server Nginx sering kali mengembalikan status 200 OK untuk halaman HTML statis, namun di balik layar JavaScript framework mengalami *Fatal Runtime Error* (layar putih / crash bundle).
- **Solusi SRE:** Smoke testing harus melakukan parsing DOM, menguji ketersediaan seluruh bundle aset (JS, CSS, fonts), dan memvalidasi string integritas payload respon (*deep health check*).

### Jebakan 2: "The Retry Storm" (Badai Penyerbuan Balik)
- **Miskonsepsi:** Jika request gagal, langsung ulangi (retry) secepat mungkin dengan loop `while True: retry()`.
- **Realitas:** Saat server baru mulai pulih dari restart, ribuan retry serentak dari agen/klien akan seketika membunuh server kembali (*cascading denial-of-service* mandiri).
- **Solusi SRE:** Wajib mengimplementasikan Exponential Backoff dipadukan dengan **Full Jitter**.

### Jebakan 3: "Alert Fatigue" (Kelelahan Alarm)
- **Miskonsepsi:** Kirim notifikasi alarm untuk setiap warning kecil, lonjakan CPU sesaat, atau request 404 acak dari bot internet.
- **Realitas:** Tim engineer akan terbiasa mengabaikan notifikasi ("paling cuma bot biasa"), sehingga ketika insiden fatal P1 terjadi, alarm tersebut tidak digubris.
- **Solusi SRE:** Alarm paging darurat hanya boleh berbunyi jika **User Experience / SLO** terancam secara nyata (berbasis Error Budget Burn Rate).

---

## 7. Specialist Workgroup Attributions

Penyusunan standar ini mengintegrasikan seluruh keahlian lintas profil AI Team Duckvaulta:

* **Leader (David):** Penetapan batas tata kelola (governance), pengorkestrasian Kanban board, dan sinkronisasi repositori GitHub.
* **Master Guru (Judith):** Penyusunan arsitektur SRE, metodologi mitigasi kegagalan, formula matematis SLO/Error Budget, dan pedagogi bedah distraktor.
* **QA Engineer (Julius):** Perancangan dan validasi suite crawler smoke test 4-layer dengan jaminan zero broken assets.
* **Fullstack Developer (Alex):** Konfigurasi runtime daemon (PM2, systemd, Vite), arsitektur reverse proxy Nginx HTTP/2, dan mekanisme graceful reload.
* **Security Engineer (Athena):** Penyelarasan standar enkripsi TLS 1.3, mitigasi eksfiltrasi kredensial, dan kepatuhan security headers (HSTS, CSP, XFO).
* **Trend Hunter (Charlie):** Kalibrasi ambang batas performa latensi terhadap standar industri Google Core Web Vitals 2026.

---
*Dokumen ini merupakan standar resmi operasional keandalan sistem dan telah terverifikasi secara langsung di VPS Duckvaulta.*
