# Port Audit & Network Isolation Report: VPS Leohermes
**Execution Timestamp:** 25 Oktober 2026, 05:17 UTC (12:17 WIB)  
**Host:** `leohermes` (AMD EPYC 9B14, Debian 13)  
**Public IP:** `34.135.45.195` | **Internal IP:** `10.128.0.2`  

---

## 1. Ringkasan Eksekutif
- **Status Audit Jaringan:** COMPLIANT / PASS
- **Port Publik Terbuka:** Port 22 (SSH), Port 80 (HTTP Nginx), Port 443 (HTTPS Nginx)
- **Port Internal Terisolasi (Localhost Only):**
  - **Port 3001 (Ruang 3D Virtual Office):** 100% Terisolasi di `127.0.0.1` (Koneksi publik ditolak: `CLOSED/REFUSED errno 111`)
  - **Port 3002 (Duckvaulta Auth Service):** 100% Terisolasi di `127.0.0.1` (Koneksi publik ditolak: `CLOSED/REFUSED errno 111`)
  - **Port 4173 (God's Eye View Spatial Intelligence):** 100% Terisolasi di `127.0.0.1` (Koneksi publik ditolak: `CLOSED/REFUSED errno 111`)
  - **Port 11434 (Ollama LLM Engine):** 100% Terisolasi di `127.0.0.1` (Koneksi publik ditolak: `CLOSED/REFUSED errno 111`)
- **Port Layanan Khusus:**
  - **Port 20128 (Hermes API Gateway / 9router):** Terproteksi otentikasi wajib (`401 Unauthorized` bila diakses tanpa API key)
  - **Port 20201/20202 (Google Cloud Ops Agent):** Daemon metrik dan logging internal GCP

---

## 2. Matriks Verifikasi Soket Jaringan

### A. Interface Loopback (`127.0.0.1`)
- Port 22: OPEN (OpenSSH 9.2p1)
- Port 80: OPEN (Nginx Reverse Proxy)
- Port 443: OPEN (Nginx TLS v1.3)
- Port 3001: OPEN (Node.js Ruang 3D Virtual Office - HTTP 200 OK)
- Port 3002: OPEN (Node.js Duckvaulta Auth - HTTP 200 OK)
- Port 4173: OPEN (Vite Preview God's Eye View - HTTP 200 OK)
- Port 11434: OPEN (Ollama API - HTTP 200 OK)
- Port 20128: OPEN (Next.js 9router LLM Endpoint)

### B. Interface Internal Private (`10.128.0.2 - ens3`)
- Port 22: OPEN
- Port 80: OPEN
- Port 443: OPEN
- Port 3001: CLOSED/REFUSED (errno 111 - 100% Terisolasi)
- Port 3002: CLOSED/REFUSED (errno 111 - 100% Terisolasi)
- Port 4173: CLOSED/REFUSED (errno 111 - 100% Terisolasi)
- Port 11434: CLOSED/REFUSED (errno 111 - 100% Terisolasi)

### C. IP Publik (`34.135.45.195`)
- Port 22: OPEN (SSH Access)
- Port 80: OPEN (HTTP Ingress Web)
- Port 443: OPEN (HTTPS Ingress Web TLS v1.3)
- Port 3001: CLOSED/REFUSED (errno 111 - Terisolasi dari internet publik)
- Port 3002: CLOSED/REFUSED (errno 111 - Terisolasi dari internet publik)
- Port 4173: CLOSED/REFUSED (errno 111 - Terisolasi dari internet publik)
- Port 11434: CLOSED/REFUSED (errno 111 - Terisolasi dari internet publik)
- Port 20128: OPEN (Terproteksi HTTP 401 Unauthorized / Token Guard)

---

## 3. Orkesktrasi Tim AI (Kanban Board Attribution)
1. **Leader (Orchestrator):** Koordinasi perumusan tiket audit, dispatch tugas, dan integrasi repositori.
2. **trend-hunter (`t_72ad399b`):** Riset standar Zero-Trust Architecture (NIST SP 800-207 & CIS Benchmarks) terkait isolasi runtime model AI dan telemetry daemon.
3. **fullstack-dev (`t_f76f6b18`):** Verifikasi socket binding level kernel Linux (`ss -tulnp`) dan konfigurasi Nginx reverse proxy routing.
4. **qa-engineer (`t_62770926`):** Penetration testing soket jaringan eksternal dan reachability probe ke IP publik dan interface lokal.
5. **security-engineer (`t_3b09d3fa`):** Evaluasi attack surface, validasi otentikasi token port 20128, dan audit postur defense-in-depth.
