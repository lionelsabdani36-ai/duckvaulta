# Panduan Master Admin OP, Navigasi Multi-World & Setup Hologram Quest
**Cycraft SMP — Crossplay Java & Bedrock Edition Operations Manual**  
*Disusun oleh: Judith (Master Guru & Mentor Akademik / Kompetisi)*  
*Kolaborasi Tim AI: Omnirush (Leader Core), Alex (Fullstack Dev), Athena (Security Engineer), Julius (QA Engineer), Judith (Mentor & Pedagogi)*

---

## 1. Visi & Filosofi Tata Kelola Cycraft SMP

Cycraft SMP didesain bukan sekadar sebagai server hiburan survival biasa, melainkan lingkungan terintegrasi (*sandbox learning environment*) yang menggabungkan:
1. **Exploration & Survival**: Petualangan survival murni lintas platform (Java & Bedrock).
2. **Computational Thinking & Hardware Logic**: Simulasi gerbang logika (AND, OR, XOR, latch) berbasis redstone di dalam dunia permainan.
3. **Cyber Security & CTF Arena**: Panggung simulasi kompetisi LKS (Lomba Kompetensi Siswa) Cyber Security, kriptografi praktis, dan observasi forensik terapan.

Untuk menjaga integritas dan ketertiban sistem, seluruh hak administratif dan alur permainan diatur melalui tata kelola terstruktur yang diuraikan dalam panduan ini.

---

## 2. Panduan Master Command Admin OP (Operator & Governance)

Operator (OP) memegang otoritas penuh terhadap siklus hidup dunia, moderasi pemain, dan eksekusi perintah server.

### A. Hierarki 4 Tingkat Hak Akses OP (Permission Levels)

Minecraft mengelompokkan hak operator ke dalam 4 tingkatan:
- **Level 1 (Bypass Spawn Protection)**: Pemain dapat memodifikasi blok di dalam radius zona proteksi spawn (`spawn-protection`).
- **Level 2 (Game Master / Cheats & Command Blocks)**: Akses ke perintah dasar gamemode, teleportasi, cuaca, waktu, pemanggilan entitas, dan pengoperasian Command Block.
- **Level 3 (Server Moderator)**: Akses ke tindakan disipliner pemain (`/kick`, `/ban`, `/pardon`, `/op`, `/deop`).
- **Level 4 (Server Administrator / Root OP)**: Hak penuh tak terbatas, termasuk perintah kontrol runtime server (`/stop`, `/reload`, `/save-all`, `/whitelist`, serta melewati batas kapasitas maksimal server).

### B. Prosedur Pemberian & Pencabutan OP

#### Format Username Java vs Bedrock:
- Pemain PC Java: `NamaPemain` (contoh: `WhiteJack`).
- Pemain HP Bedrock: `.NamaPemain` (wajib sertakan prefix titik `.` di depan, contoh: `.WhiteJack`).

#### 4 Jalur Eksekusi:
1. **Screen Interaktif VPS**:
   ```bash
   screen -r cycraft
   # Ketik: op WhiteJack (atau op .WhiteJack)
   # Keluar tanpa mematikan: Tekan Ctrl+A lalu D
   ```
2. **One-Liner Terminal (Direct Stuff)**:
   ```bash
   screen -S cycraft -X stuff "op WhiteJack^M"
   screen -S cycraft -X stuff "op .WhiteJack^M"
   ```
3. **Remote Console (RCON)**:
   Host: `127.0.0.1` (atau `34.135.45.195`), Port: `25575`, Password: `DuckVaultaMC2026Secured!`.
4. **File Konfigurasi `ops.json`**:
   Lokasi: `/home/lionelsabdani36/minecraft-server/ops.json`.

#### Pencabutan OP:
```bash
screen -S cycraft -X stuff "deop WhiteJack^M"
screen -S cycraft -X stuff "deop .WhiteJack^M"
```

---

### C. Katalog Perintah Admin EssentialsX

EssentialsX menyediakan kumpulan perintah esensial untuk manajemen server harian:

#### 1. Manajemen Pemain & Kondisi Fisik:
- `/gamemode <creative|survival|adventure|spectator> [pemain]` (alias: `/gmc`, `/gms`, `/gma`, `/gmsp`).
- `/heal [pemain]`: Memulihkan health dan food level ke status maksimal.
- `/feed [pemain]`: Memulihkan rasa lapar pemain.
- `/god [pemain]`: Mengaktifkan mode kebal kerusakan (*invulnerable*).
- `/fly [pemain]`: Mengaktifkan kemampuan terbang bebas di mode survival.
- `/speed <1-10> [pemain]`: Mengatur kecepatan berjalan atau terbang.
- `/vanish` (alias `/v`): Menghilangkan avatar admin dari pandangan pemain lain untuk observasi rahasia.
- `/clear [pemain]`: Mengosongkan seluruh item di inventori pemain.
- `/kill <pemain>`: Mengeliminasi entitas atau pemain tertentu.

#### 2. Inspeksi Inventori & Investigasi Fair-Play:
- `/invsee <pemain>`: Membuka dan melihat isi inventori pemain secara langsung secara real-time.
- `/enderchest <pemain>` (alias `/ec`): Membuka isi peti Ender pemain untuk audit penyimpanan tersembunyi.

#### 3. Teleportasi & Lokasi:
- `/tp <pemain1> <pemain2>`: Memindahkan pemain 1 ke posisi pemain 2.
- `/tphere <pemain>`: Memindahkan pemain ke koordinat admin secara paksa.
- `/back`: Kembali ke lokasi kematian terakhir atau posisi sebelum teleportasi.
- `/top`: Memindahkan pemain ke blok tertinggi di atas kepalanya secara instan.
- `/jump` (alias `/j`): Melompat ke blok yang sedang disorot kursor.

#### 4. Pengendalian Lingkungan & Waktu:
- `/time set <day|noon|night|midnight>`: Mengatur siklus waktu dunia.
- `/weather <clear|rain|thunder> [durasi]`: Mengatur kondisi atmosfer.
- `/gamerule keepInventory true`: Menjaga barang tetap aman saat pemain mati.
- `/gamerule doDaylightCycle false`: Mengunci siklus waktu siang hari.

#### 5. Moderasi & Penegakan Disiplin:
- `/kick <pemain> [alasan]`: Memutus koneksi pemain dari server.
- `/ban <pemain> [alasan]`: Memblokir username dari server secara permanen.
- `/tempban <pemain> <waktu> [alasan]`: Memblokir sementara (contoh: `/tempban Pemain 2h Melanggar Aturan`).
- `/mute <pemain> [waktu]`: Menonaktifkan hak berbicara di chat publik.
- `/broadcast <pesan>` (alias `/bc`): Mengirim pengumuman resmi server dengan sorotan warna ke seluruh pemain.

---

### D. Manajemen Izin Berbasis Kelompok (LuckPerms)

Cycraft SMP menggunakan sistem permissions modern LuckPerms untuk membagi peran:

| Grup | Deskripsi Peran | Perintah Penting yang Diizinkan |
|---|---|---|
| `default` | Pemain baru & umum | `essentials.warp`, `essentials.spawn`, `essentials.kit`, `essentials.msg`, `multiverse.access.*` |
| `participant` | Peserta lomba / quest | Izin default + akses arena khusus + interaksi tombol tantangan |
| `mod` | Moderator server | `/kick`, `/mute`, `/invsee`, `/tp`, `/vanish` |
| `admin` | Administrator penuh | `*` (seluruh permissions node) |

#### Perintah Manajemen LuckPerms:
- Menetapkan grup pemain:
  ```text
  /lp user <pemain> parent set <nama_grup>
  Contoh: /lp user WhiteJack parent set admin
  ```
- Menambahkan izin ke grup default:
  ```text
  /lp group default permission set essentials.warp true
  /lp group default permission set essentials.warps.* true
  ```
- Membuka Web Visual Editor:
  ```text
  /lp editor
  # Salin URL yang dihasilkan ke browser untuk mengelola izin dengan antarmuka grafis
  ```

---

## 3. Panduan Navigasi & Warp Antar World (Multiverse-Core & Essentials)

Cycraft SMP mengimplementasikan arsitektur multi-world yang memisahkan area publik/aman dari arena bertahan hidup liar.

### A. Peta Dimensi Cycraft SMP

| Nama Dunia | Tipe Lingkungan | Peruntukan Utama | Kebijakan Proteksi |
|---|---|---|---|
| `cyber_hub` | FLAT (Normal) | Lobi utama, papan pengumuman, portal teleportasi | Non-PvP, Spawn Protected, No Mob Spawn |
| `world` | NORMAL (Overworld) | Survival bebas, eksplorasi sumber daya alam | Normal Survival, PvP Enabled |
| `world_nether` | NETHER | Pengumpulan bahan nether, dungeon, stage CTF tingkat lanjut | Hazard Extreme, Normal Mob Spawning |
| `world_the_end` | THE_END | Arena Ender Dragon, elytra hunting, endgame podium | Void Hazard |

---

### B. Perintah Esensial Multiverse-Core (`/mv`)

Untuk admin mengelola dunia secara dinamis:

1. **Melihat Seluruh Daftar Dunia**:
   ```text
   /mv list
   ```
2. **Teleportasi Antar Dunia**:
   ```text
   /mv tp [pemain] <nama_dunia>
   Contoh: /mv tp cyber_hub
   Contoh: /mv tp WhiteJack world
   ```
3. **Mengatur Titik Lahir Dunia (Spawn Point)**:
   Berdirilah di posisi yang diinginkan di dalam dunia target, lalu jalankan:
   ```text
   /mv setspawn
   ```
4. **Membuat Dunia Baru**:
   ```text
   /mv create <nama> <NORMAL|NETHER|END> [-t FLAT]
   Contoh: /mv create arena_lks NORMAL -t FLAT
   ```
5. **Mengimpor Dunia yang Sudah Ada di Disk**:
   ```text
   /mv import <nama_folder> <NORMAL|NETHER|END>
   ```
6. **Mengatur Aturan Khusus Dunia (Rules Modifier)**:
   - Matikan PvP di Cyber Hub:
     ```text
     /mv modify set pvp false cyber_hub
     ```
   - Matikan kelaparan di Hub:
     ```text
     /mv modify set hunger false cyber_hub
     ```
   - Matikan monster di Hub:
     ```text
     /mv modify set monsters false cyber_hub
     ```
   - Matikan binatang liar di Hub:
     ```text
     /mv modify set animals false cyber_hub
     ```

---

### C. Sistem Warp Pemain (EssentialsX)

Untuk memudahkan pemain berpindah antar fasilitas tanpa perlu menghafal nama dunia Multiverse:

1. **Membuat Titik Warp Baru**:
   Berdiri di posisi tujuan, lalu ketik:
   ```text
   /setwarp <nama_warp>
   Contoh:
   /setwarp hub
   /setwarp quest
   /setwarp survival
   ```
2. **Menggunakan Warp (Semua Pemain)**:
   ```text
   /warp <nama_warp>
   Contoh: /warp survival
   ```
3. **Melihat Daftar Warp Tersedia**:
   ```text
   /warp
   ```
4. **Menghapus Titik Warp**:
   ```text
   /delwarp <nama_warp>
   ```

---

## 4. Panduan Setup Hologram Interaktif (DecentHolograms)

Hologram melayang adalah sarana komunikasi visual terbaik di area spawn dan arena kompetisi tanpa mengganggu estetika bangunan fisik.

### A. Fitur & Kapabilitas Visual DecentHolograms

- **Sistem Formatting Kaya**: Mendukung pewarnaan standar (`&a` hijau, `&b` aqua, `&e` kuning, `&c` merah, `&l` bold, `&n` underline).
- **Format RGB & Hex Modern**: Mendukung kode hex spesifik (contoh: `&#38bdf8Cyber Hub`).
- **Placeholder Terintegrasi**: Mengganti teks otomatis berdasarkan konteks pemain, misalnya `%player_name%` untuk menyapa pemain yang memandang hologram.
- **Interaksi Klik (Click Actions)**: Hologram dapat diklik kiri atau kanan untuk menjalankan perintah.

---

### B. Perintah Esensial DecentHolograms (`/dh`)

#### 1. Membuat & Menghapus Hologram:
- Membuat hologram baru di posisi berdiri pemain:
  ```text
  /dh h create <nama_hologram> <isi_baris_pertama>
  Contoh: /dh h create selamat_datang &b&lSELAMAT DATANG DI CYCRAFT SMP
  ```
- Membuat hologram via koordinat spesifik (dapat dijalankan dari konsol VPS):
  ```text
  /dh h create selamat_datang cyber_hub:0.5:-57.0:0.5 &b&lCYCRAFT SMP
  ```
- Menghapus hologram:
  ```text
  /dh h delete <nama_hologram>
  ```

#### 2. Menambah, Mengedit & Menyusun Baris Teks:
- Menambah baris baru di bawah baris terakhir:
  ```text
  /dh line add <nama_hologram> 1 <teks_baris>
  Contoh: /dh line add selamat_datang 1 &7Klik disini untuk mulai bermain!
  ```
- Mengubah teks pada baris tertentu:
  ```text
  /dh line set <nama_hologram> 1 <nomor_baris> <teks_baru>
  Contoh: /dh line set selamat_datang 1 2 &eGunakan /warp survival untuk bertualang
  ```
- Menyisipkan baris di tengah-tengah:
  ```text
  /dh line insert <nama_hologram> 1 <nomor_baris> <teks>
  ```
- Menghapus satu baris tertentu:
  ```text
  /dh line remove <nama_hologram> 1 <nomor_baris>
  ```

#### 3. Penataan Posisi & Rotasi:
- Memindahkan hologram ke posisi admin saat ini:
  ```text
  /dh h movehere <nama_hologram>
  ```
- Memindahkan hologram ke tengah-tengah blok:
  ```text
  /dh h center <nama_hologram>
  ```
- Menjajarkan dua hologram pada sumbu tertentu:
  ```text
  /dh h align <nama_hologram_1> XZ <nama_hologram_2>
  ```

#### 4. Menambahkan Aksi Klik (Interactive Click Action):
Format aksi mendukung eksekusi sebagai pemain (`[PLAYER]`) atau sebagai konsol server (`[CONSOLE]`):
- Klik kiri untuk teleportasi:
  ```text
  /dh click add selamat_datang LEFT [PLAYER] warp survival
  ```
- Klik kanan untuk klaim starter kit:
  ```text
  /dh click add selamat_datang RIGHT [PLAYER] kit starter
  ```
- Klik untuk mengirim pengumuman via konsol:
  ```text
  /dh click add selamat_datang RIGHT [CONSOLE] tellraw {player} {"text":"§aSelamat datang di Cyber Hub!"}
  ```

---

### C. Konfigurasi Deklaratif Berbasis File YAML

Seluruh hologram di Cycraft SMP tersimpan rapi dalam format YAML di:  
`/home/lionelsabdani36/minecraft-server/plugins/DecentHolograms/holograms/`

#### Template 1: Papan Sambutan Hub (`cyber_hub_welcome.yml`)
```yaml
name: cyber_hub_welcome
location: cyber_hub:0.5:-57.0:0.5
enabled: true
display-range: 48
update-range: 48
update-interval: 20
facing: 0.0
down-origin: false
pages:
- lines:
  - content: '&b&l⚡ CYCRAFT SMP ⚡'
    height: 0.35
  - content: '&7&oOfficial Crossplay Java & Bedrock'
    height: 0.28
  - content: '&e====================================='
    height: 0.25
  - content: '&fSelamat Datang di &b&lCyber Hub&r&f!'
    height: 0.32
  - content: '&7Dunia Eksplorasi, Logika & Kompetisi CTF/LKS'
    height: 0.28
  - content: '&a▶ &fKetik &a/warp survival &funtuk Dunia Survival'
    height: 0.3
    actions:
      LEFT:
      - '[PLAYER] warp survival'
      RIGHT:
      - '[PLAYER] warp survival'
  - content: '&b▶ &fKetik &b/warp quest &funtuk Area Quest & Arena'
    height: 0.3
    actions:
      LEFT:
      - '[PLAYER] warp quest'
      RIGHT:
      - '[PLAYER] warp quest'
  - content: '&e====================================='
    height: 0.25
  - content: '&dMentor & Pengawas: &fJudith (Master Guru)'
    height: 0.28
```

#### Template 2: Papan Misi Quest & Arena CTF (`quest_board.yml`)
```yaml
name: quest_board
location: cyber_hub:8.5:-57.0:0.5
enabled: true
display-range: 48
update-range: 48
update-interval: 20
facing: 0.0
down-origin: false
pages:
- lines:
  - content: '&6&l🏆 CYCRAFT QUEST & CTF ARENA 🏆'
    height: 0.35
  - content: '&e&nPusat Tantangan Akademik & LKS Cyber Security'
    height: 0.28
  - content: '&7-------------------------------------'
    height: 0.25
  - content: '&a[Tier 1] &fReconnaissance: Temukan Beacon Tersembunyi'
    height: 0.3
  - content: '&e[Tier 2] &fHardware Logic: Pecahkan Redstone AND/XOR Gate'
    height: 0.3
  - content: '&c[Tier 3] &fCrypto Challenge: Dekripsi Caesar Cipher di Chest'
    height: 0.3
  - content: '&7-------------------------------------'
    height: 0.25
  - content: '&b▶ Klik disini untuk klaim Kit Pelajar: &f/kit starter'
    height: 0.3
    actions:
      LEFT:
      - '[PLAYER] kit starter'
      RIGHT:
      - '[PLAYER] kit starter'
  - content: '&aKirim bukti flag & skor ke Mentor Judith!'
    height: 0.28
```

#### Prosedur Hot-Reload:
Setelah menambah atau menyunting file `.yml`, terapkan perubahan tanpa restart:
```text
/dh reload
```

---

## 5. Panduan Desain Quest, Arena Kompetisi & Tantangan CTF / LKS

Sebagai Master Guru & Mentor Kompetisi, kurikulum tantangan in-game dirancang berdasarkan prinsip **Scaffolded Mastery** (Tantangan bertingkat dari fondasi hingga analisis tingkat tinggi).

### A. 3 Tingkatan Desain Quest Kompetisi

```
+-------------------------------------------------------------+
| TIER 3: CYBER DEFENSE & KRIPTOGRAFI                         |
| Analisis sandi, dekripsi pesan tersembunyi, forensik buku  |
+------------------------------^------------------------------+
                               |
+------------------------------+------------------------------+
| TIER 2: HARDWARE & REDSTONE LOGIC GATES                     |
| Perancangan sirkuit AND, OR, XOR, pemecahan puzzle kombinasi|
+------------------------------^------------------------------+
                               |
+------------------------------+------------------------------+
| TIER 1: OBSERVASI & RECONNAISSANCE                          |
| Navigasi koordinat presisi, observasi lingkungan, checkpoint|
+-------------------------------------------------------------+
```

#### Rincian Spesifikasi Tantangan:
1. **Tier 1: Observasi & Koordinat Presisi**
   - **Tujuan Pembelajaran**: Memahami orientasi ruang, sistem koordinat 3D $(X, Y, Z)$, dan pembacaan metadata lingkungan.
   - **Mekanisme**: Admin menyembunyikan sebuah Beacon di koordinat tertentu di dunia survival atau cyber hub.
   - **Verifikasi**: Peserta mencatat koordinat dan mengambil token bernama khusus dari dispenser atau chest.

2. **Tier 2: Gerbang Logika Hardware (Redstone Logic)**
   - **Tujuan Pembelajaran**: Menghubungkan konsep dasar arsitektur komputer (gerbang logika biner) dengan mekanika visual redstone.
   - **Mekanisme**: Pintu besi menuju ruang rahasia dikunci oleh 4 tuas (*levers*). Peserta harus menekan tuas dengan kombinasi biner yang memenuhi persamaan logika boolean:
     $$F = (A \land B) \lor (C \oplus D)$$
   - **Verifikasi**: Jika kombinasi benar, sirkuit inverter mentrigger pintu besi terbuka.

3. **Tier 3: Kriptografi & Cyber Security Flag Hunt (LKS)**
   - **Tujuan Pembelajaran**: Melatih analisis kriptografi klasik (Caesar Cipher, Base64) dan penalaran deduktif.
   - **Mekanisme**: Di dalam peti tersembunyi di dimensi Nether, tersimpan sebuah `written_book` berisi teks sandi:
     `S3VycHVyX0NURntDaXBnaGVyX1N1Y2Nlc3NfMjAyNn0=`
   - **Verifikasi**: Peserta mendekode string Base64 tersebut menjadi flag: `Purpur_CTF{Cipgher_Success_2026}` dan menyetorkannya ke mentor/admin.

---

### B. Mekanisme Otomatisasi & Distribusi Hadiah

#### 1. Essentials Kit & Tanda Klaim (Reward Signs)
Konfigurasi paket reward di `/home/lionelsabdani36/minecraft-server/plugins/Essentials/kits.yml`:
- Kit Pemula: `/kit starter` (Pedang Akademik, Beliung Logika, Roti, Obor, Perisai).
- Kit Hadiah: `/kit quest_reward` (5 Diamond, 10 Emerald, 2 Golden Apple, serta broadcast pengumuman kemenangan).

Admin dapat membuat plang interaktif klaim reward:
```text
Line 1: [Kit]
Line 2: quest_reward
Line 3: (Biarkan kosong)
Line 4: (Biarkan kosong)
```

#### 2. Pelacak Skor In-Game (Scoreboard System)
Sistem bawaan Minecraft untuk memantau progres peserta kompetisi:
1. **Membuat Objective Poin**:
   ```text
   /scoreboard objectives add QuestPoint dummy "§e§lPoin Prestasi"
   ```
2. **Menampilkan di Layar Kanan (Sidebar)**:
   ```text
   /scoreboard objectives setdisplay sidebar QuestPoint
   ```
3. **Menambahkan Poin ke Pemenang**:
   ```text
   /scoreboard players add WhiteJack QuestPoint 100
   ```
4. **Mereset Skor**:
   ```text
   /scoreboard players reset WhiteJack QuestPoint
   ```

#### 3. Otomatisasi Validasi via Command Block
Aktifkan command block di `server.properties` (`enable-command-block=true`).
- **Mendeteksi Peserta di Lokasi Finis**:
  ```text
  /execute if entity @p[distance=..3] run title @p title {"text":"§aTANTANGAN SELESAI!","bold":true}
  ```
- **Memberikan Hadiah Otomatis**:
  ```text
  /execute if entity @p[distance=..3] run give @p diamond 5
  ```
- **Siaran Kemenangan ke Seluruh Server**:
  ```text
  /execute if entity @p[distance=..3] run broadcast §6§l[Juara] §e@p §fberhasil memecahkan teka-teki logika Cyber Hub!
  ```

---

### C. Isolasi & Proteksi Wilayah Arena via WorldGuard

Agar arena kompetisi tidak dirusak oleh pemain biasa dan terbebas dari ledakan creeper/TNT:

1. **Seleksi Wilayah**:
   Gunakan wooden axe (WorldEdit wand) atau command posisi:
   ```text
   //pos1
   //pos2
   ```
2. **Definisikan Region**:
   ```text
   /rg define arena_quest
   ```
3. **Pasang Bendera Pengaman (Flags)**:
   - Larang menghancurkan blok:
     ```text
     /rg flag arena_quest block-break deny
     ```
   - Larang memasang blok:
     ```text
     /rg flag arena_quest block-place deny
     ```
   - Larang PvP antar peserta:
     ```text
     /rg flag arena_quest pvp deny
     ```
   - Matikan ledakan creeper dan TNT:
     ```text
     /rg flag arena_quest creeper-explosion deny
     /rg flag arena_quest tnt deny
     ```
   - Izinkan interaksi dengan pintu, tuas, dan tombol:
     ```text
     /rg flag arena_quest use allow
     ```

---

## 6. Protokol Pemeliharaan & Troubleshooting Cepat

| Gejala Masalah | Akar Masalah | Solusi Tepat |
|---|---|---|
| Pemain biasa tidak bisa teleportasi `/warp` | Permission node belum disetel di grup `default` | Jalankan `/lp group default permission set essentials.warp true` dan `essentials.warps.* true` |
| Pemain ditolak saat masuk dunia `/mv tp` | Izin akses dunia Multiverse tertutup | Jalankan `/lp group default permission set multiverse.access.* true` |
| Hologram tidak muncul setelah edit file | Plugin DecentHolograms belum di-reload | Jalankan `/dh reload` di konsol atau in-game |
| TPS server turun di bawah 19.0 | Terlalu banyak entitas atau generasi chunk baru | Cek status dengan `/tps`, gunakan `/chunky trim` atau `/spark profiler` |
| Pemain Bedrock gagal terhubung | Port UDP 19132 terhalang firewall VPS | Periksa `sudo ufw status`, izinkan UDP: `sudo ufw allow 19132/udp` |

---

## 7. Koordinasi Tim AI DuckVaulta

Dokumentasi ini adalah bagian dari peluncuran ekosistem Cycraft SMP:
- **Leader (Omnirush)**: Sinkronisasi arsitektur dan orkestrasi taskboard.
- **Alex (Fullstack Dev)**: Pembuatan world `cyber_hub` dan integrasi plugin suite Purpur.
- **Athena (Security Engineer)**: Hardening port, enkripsi RCON, dan audit flag WorldGuard.
- **Julius (QA Engineer)**: Verifikasi 12 plugin tanpa error dan audit 20.0 TPS.
- **Judith (Master Guru & Mentor)**: Penyusunan panduan master OP, standardisasi multi-world, setup hologram visual, dan desain kurikulum tantangan quest.
