# Panduan Akses & Administrasi Minecraft Crossplay (Java & Bedrock)
**Cycraft SMP Server (d/h DuckVaulta SMP) — Master Documentation & Operations Manual**  
*Disusun oleh: Judith (Master Guru & Mentor Akademik / Kompetisi)*  
*Kolaborasi Tim AI: Leader (Omnirush Core), Alex (Fullstack Dev), Athena (Security Engineer), Julius (QA Engineer), Judith (Mentor/Docs)*

> **Dokumen Terkait**: Untuk panduan lengkap command admin OP, tata kelola multi-world, setup hologram interaktif, dan arena quest kompetisi CTF/LKS, baca: [`JUDITH_ADMIN_COMMAND_GUIDE.md`](JUDITH_ADMIN_COMMAND_GUIDE.md).

---

## 1. Ringkasan Parameter Jaringan & Server

Berikut adalah rincian kredensial dan endpoint koneksi resmi server Minecraft Crossplay:

| Parameter | Nilai / Konfigurasi | Deskripsi / Catatan |
|---|---|---|
| **Server Name** | `Cycraft SMP` | Nama resmi server (bebas diatur di client) |
| **Server Host / IP** | `34.135.45.195` | IP Publik VPS Utama (alternatif: `duckvaulta.ai.id`) |
| **Port Java Edition** | `25565` | Port default Java Edition (TCP/UDP) |
| **Port Bedrock Edition** | `19132` | Port default Bedrock/PE via GeyserMC (UDP) |
| **Port RCON** | `25575` | Remote Console Administrasi (TCP) |
| **Password RCON** | `DuckVaultaMC2026Secured!` | Password autentikasi konsol jarak jauh |
| **Server Engine** | Purpur 1.21.4 (Build 2416) | Fork performa tinggi berbasis Paper/Spigot |
| **Runtime Java** | OpenJDK 21.0.13 64-Bit | Alokasi RAM 4GB (Aikar G1GC Flags) |
| **Mode Autentikasi** | Hybrid (`online-mode=false` + Floodgate) | Mendukung akun Original & Non-Original / Offline |
| **Protokol Didukung** | Java 1.16.x s.d. 1.21.4 & Bedrock Terkini | Ditenagai ViaVersion & ViaBackwards |

---

## 2. Panduan Koneksi Pemain HP / Tablet / Console (Bedrock Edition)

Platform yang didukung:
- Smartphone & Tablet: Android (APK / Google Play Store), iOS & iPadOS (App Store).
- Windows PC: Minecraft Bedrock Edition (Windows Store / Xbox App).
- Console: Nintendo Switch, PlayStation, Xbox (dengan DNS/BedrockConnect jika diperlukan).

### Langkah-Langkah Join:
1. Luncurkan aplikasi **Minecraft Bedrock** di perangkat HP Anda.
2. Di halaman utama, klik tombol **Play** (Main).
3. Pilih tab bagian atas yang bertuliskan **Servers** (Server).
4. Gulir daftar server rekanan ke bagian paling bawah, lalu klik tombol **Add Server** (Tambah Server).
5. Isi formulir konfigurasi server dengan rincian berikut:
   - **Server Name**: `DuckVaulta SMP`
   - **Server Address**: `34.135.45.195` (atau `duckvaulta.ai.id`)
   - **Port**: `19132` (Biarkan angka port default Bedrock ini)
6. Klik tombol **Save** (Simpan) untuk menyimpannya ke daftar, atau langsung tekan **Play** (Mainkan).
7. Tunggu proses loading koneksi (*Locating server* -> *Loading resources* -> *Joining world*).

### Catatan Khusus Autentikasi Bedrock (Floodgate):
- **Tanpa Lisensi Java**: Anda TIDAK perlu membeli akun Minecraft Java Edition untuk bermain di server ini. Akun Xbox/Microsoft Bedrock Anda sudah langsung dikenali.
- **Prefix Username Bedrock**: Sistem Floodgate secara otomatis menyematkan tanda titik (`.`) di awal nama pemain Bedrock (contoh: jika nama Xbox Anda adalah `WhiteJack`, di dalam permainan nama Anda akan terbaca sebagai `.WhiteJack`). Ini mencegah terjadinya tabrakan UUID/identitas dengan pemain versi Java.

---

## 3. Panduan Koneksi Pemain PC / Laptop (Java Edition)

Platform yang didukung:
- Sistem Operasi: Windows 10/11, macOS, Linux.
- Client / Launcher: Minecraft Official Launcher, Prism Launcher, Modrinth App, Feather Client, Lunar Client, Badlion, atau Launcher Offline/Non-Original (TLauncher, Legacy Launcher, SKLauncher).
- Versi Game: Versi bawaan server adalah **1.21.4**. Berkat plugin **ViaVersion** dan **ViaBackwards**, Anda juga dapat menggunakan versi Java dari **1.16.5** hingga **1.21.4**.

### Langkah-Langkah Join:
1. Luncurkan Minecraft Java Edition dengan versi 1.21.4 (atau versi kompatibel pilihan Anda).
2. Dari menu utama, pilih opsi **Multiplayer** (Multipemain).
3. Klik tombol **Add Server** (Tambah Server) di bagian bawah.
4. Isi data server:
   - **Server Name**: `DuckVaulta SMP`
   - **Server Address**: `34.135.45.195` (karena port 25565 adalah standar default Java, Anda tidak wajib menuliskan `:25565`, namun penulisan `34.135.45.195:25565` tetap valid).
5. Klik **Done** (Selesai).
6. Sorot server DuckVaulta SMP dari daftar, lalu klik tombol **Join Server** (atau klik ganda baris server).
7. Anda akan langsung mendarat di dunia DuckVaulta SMP.

### Catatan Fleksibilitas Akun Java:
- Konfigurasi server mengaktifkan mode crossplay non-intrusif (`online-mode=false`).
- Artinya, pemain yang memiliki lisensi akun resmi Microsoft/Mojang maupun pengguna launcher alternatif dapat terhubung tanpa kendala otentikasi eksternal.

---

## 4. Panduan Lengkap Hak Akses Operator (OP Admin)

Operator (OP) adalah pemegang hak administratif tertinggi di dalam server.

### A. Memahami 4 Tingkatan Level OP
Minecraft memiliki hierarki 4 tingkat akses (Permission Level):
1. **Level 1 (Bypass Proteksi Spawn)**: Pemain dapat membangun dan menghancurkan blok di dalam radius wilayah proteksi spawn (*spawn protection area*).
2. **Level 2 (Game Master / Cheats)**: Pemain memiliki akses ke perintah standar cheats, seperti `/gamemode`, `/give`, `/tp`, `/clear`, `/gamerule`, `/weather`, `/time`, `/locate`, serta dapat mengoperasikan command block.
3. **Level 3 (Server Moderator)**: Pemain memiliki akses ke manajemen hukuman pemain, seperti `/kick`, `/ban`, `/ban-ip`, `/pardon`, `/pardon-ip`, `/op`, `/deop`.
4. **Level 4 (Full Administrator / Root OP)**: Pemain memiliki akses penuh tak terbatas, termasuk perintah kontrol server seperti `/stop`, `/reload`, `/restart`, `/whitelist`, `/save-all`, serta dapat melewati batasan kapasitas maksimal pemain (*bypassesPlayerLimit*).

---

### B. Prosedur Pemberian Hak OP (4 Cara Praktis)

#### 1. Cara 1: Melalui Screen Console Server Langsung (Interaktif di VPS)
Server Minecraft dijalankan di dalam sesi GNU Screen dengan nama sesi `minecraft`.
Langkah operasional:
1. Masuk ke terminal VPS via SSH atau Hermes Terminal.
2. Buka tampilan konsol interaktif dengan menjalankan:
   ```bash
   screen -r minecraft
   ```
3. Ketikkan perintah OP:
   - Untuk pemain PC Java:
     ```text
     op <NamaPemain>
     ```
     Contoh: `op WhiteJack`
   - Untuk pemain HP Bedrock (Penting: Wajib pakai tanda titik di depan!):
     ```text
     op .<NamaPemain>
     ```
     Contoh: `op .WhiteJack`
4. Untuk keluar dari konsol tanpa mematikan server:
   Tekan kombinasi tombol **Ctrl + A**, lalu tekan tombol **D** (*Detach*). Server akan tetap berjalan di latar belakang.

---

#### 2. Cara 2: Eksekusi Perintah ke Console Tanpa Perlu Attach (Bash One-Liner)
Jika Anda ingin memberikan OP secara cepat tanpa harus membuka layar screen secara interaktif, gunakan perintah direct-stuff dari shell:
- Untuk pemain Java:
  ```bash
  screen -S minecraft -X stuff "op WhiteJack^M"
  ```
- Untuk pemain Bedrock:
  ```bash
  screen -S minecraft -X stuff "op .WhiteJack^M"
  ```
*(Catatan: Karakter `^M` merepresentasikan penekanan tombol Enter pada konsol).*

---

#### 3. Cara 3: Melalui Remote Console (RCON)
Server telah dikonfigurasi dengan antarmuka RCON yang aman pada port 25575.
Rincian kredensial RCON:
- **Host**: `34.135.45.195` (atau `127.0.0.1` dari localhost VPS)
- **Port**: `25575`
- **Password**: `DuckVaultaMC2026Secured!`

Eksekusi via utilitas `mcrcon` atau skrip Python:
```python
import socket, struct

def rcon_command(host, port, password, cmd):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    sock.connect((host, port))
    
    # Auth packet (type=3)
    auth_pkg = struct.pack('<iii', len(password) + 10, 1, 3) + password.encode('utf-8') + b'\x00\x00'
    sock.sendall(auth_pkg)
    sock.recv(4096)
    
    # Exec command packet (type=2)
    cmd_pkg = struct.pack('<iii', len(cmd) + 10, 2, 2) + cmd.encode('utf-8') + b'\x00\x00'
    sock.sendall(cmd_pkg)
    res = sock.recv(4096)
    sock.close()
    return res[12:-2].decode('utf-8', errors='ignore')

# Eksekusi:
print(rcon_command('127.0.0.1', 25575, 'DuckVaultaMC2026Secured!', 'op WhiteJack'))
```

---

#### 4. Cara 4: Melalui File Konfigurasi `ops.json`
Daftar operator disimpan secara terstruktur dalam file JSON di direktori server:
Lokasi: `/home/lionelsabdani36/minecraft-server/ops.json`

Struktur konfigurasi standar:
```json
[
  {
    "uuid": "00000000-0000-0000-0000-000000000000",
    "name": "WhiteJack",
    "level": 4,
    "bypassesPlayerLimit": true
  }
]
```
Jika mengedit file ini saat server sedang aktif, jalankan perintah reload di konsol:
```bash
screen -S minecraft -X stuff "reload confirm^M"
```

---

### C. Cara Mencabut Hak Akses OP (De-OP)
Untuk menghapus hak operator dari pemain, jalankan:
- Pemain Java: `deop WhiteJack`
- Pemain Bedrock: `deop .WhiteJack`
Eksekusi dapat dilakukan via konsol screen, RCON, maupun in-game oleh sesama Level 4 OP.

---

## 5. Ringkasan Perintah Penting untuk Admin Server

| Perintah | Fungsi / Kegunaan |
|---|---|
| `/gamemode creative [pemain]` | Mengubah mode permainan menjadi kreatif |
| `/gamemode survival [pemain]` | Mengubah mode permainan menjadi survival |
| `/tp [pemain1] [pemain2]` | Melakukan teleportasi pemain |
| `/weather clear` | Mengubah cuaca menjadi cerah |
| `/time set day` | Mengatur waktu menjadi siang hari |
| `/whitelist on / off` | Mengaktifkan atau mematikan sistem whitelist |
| `/whitelist add [pemain]` | Memasukkan nama pemain ke daftar putih izin masuk |
| `/kick [pemain] [alasan]` | Mengeluarkan pemain dari server secara paksa |
| `/ban [pemain] [alasan]` | Memblokir pemain secara permanen dari server |
| `/tps` | Memeriksa stabilitas Tick Per Second (ideal: 20.0 TPS) |
| `/geyser version` | Memeriksa versi dan status bridge GeyserMC |
| `/chunky start` | Memulai pre-generasi map dunia untuk memangkas lag |

---

## 6. Distribusi Peran Tim AI DuckVaulta

Sesuai tata kelola multi-agent arsitektur DuckVaulta, tugas setup server Minecraft Crossplay didistribusikan secara terkoordinasi:

1. **Leader (Omnirush Core)**:
   - Mengorkestrasi pipeline eksekusi, dependensi tugas, dan tuning bridge crossplay.
2. **Alex (Fullstack Developer)**:
   - Menyiapkan direktori server `/home/lionelsabdani36/minecraft-server`.
   - Mengunduh Purpur 1.21.4 engine, eula.txt, server.properties, start.sh.
   - Mengintegrasikan plugin crossplay Geyser-Spigot (UDP 19132), Floodgate-Spigot, ViaVersion, ViaBackwards, dan Chunky.
3. **Athena (Security Engineer)**:
   - Hardening port RCON 25575 dengan password terenkripsi kuat.
   - Audit firewall, pembatasan binding interface, serta verifikasi pemisahan UUID Java dan Bedrock.
4. **Julius (QA Engineer)**:
   - Pengujian startup dan verifikasi konektivitas listening port (TCP 25565, UDP 19132, TCP 25575).
   - Pengujian query status via UDP socket, verifikasi TPS stabil pada 20.0 TPS tanpa lag.
5. **Judith (Master Guru & Mentor)**:
   - Penyusunan panduan akses komprehensif untuk pengguna HP dan PC.
   - Perumusan instruksi operasional OP admin bertingkat dengan pendekatan pedagogis yang terstruktur dan mudah dipahami.
   - Sinkronisasi dokumentasi ke portal DuckVaulta dan repositori GitHub.
