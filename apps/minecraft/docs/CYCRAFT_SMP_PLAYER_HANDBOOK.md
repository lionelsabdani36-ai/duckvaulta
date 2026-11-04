# Cycraft SMP — Player & Administrator Handbook
**Server Host:** `duckvaulta.ai.id` / `34.135.45.195`  
**Java Port:** `25565` (TCP) | **Bedrock Port:** `19132` (UDP)  
**Versi Engine:** Purpur 1.21.4 (Java 21 LTS) + Geyser Crossplay  

---

## 1. Hub Metropolitan Skyblock & Cyber Quest
Hub utama Cycraft SMP dirancang dengan arsitektur void murni (*zero other blocks*). Di atas kehampaan kosmis, berdiri megastruktur metropolitan modern berhiaskan neon conduit, cyan concrete, sea lanterns, dan beacon arrays.

### Navigasi Hub Cepat
* `/warp hub` — Pusat Nexus Spawn utama.
* `/warp quest` — Menara laboratorium siber & podium NPC Quest Master.
* `/warp arena` — Cyber CTF Battle Colosseum (arena kompetisi PVP resmi).
* `/warp survival` — Portal transmisi menuju dunia Survival SMP.

### Sistem Quest Cybersecurity (CTF In-Game)
Di distrik utara (`/warp quest`), pemain dapat menemui NPC **`[CYSEC] Quest Master`**:
1. **Klik Kanan NPC** untuk membuka daftar misi siber aktif.
2. Atau jalankan perintah mandiri:
   * `/challenge` — Menampilkan seluruh tantangan terbuka dan status penyelesaian.
   * `/challenge <id>` — Membaca rincian skenario, kategori, dan petunjuk (hint).
   * `/submit <flag>` — Memvalidasi flag jawaban (contoh: `/submit CYBER{sql_injection_bypass_2026}`).
   * `/ctfstats` — Memeriksa profil hacker, total misi selesai, dan riwayat solve.
3. **Hadiah Penyelesaian Misi:**
   * **CyBits:** Saldo ekonomi server langsung masuk ke akun pemain via Vault.
   * **Claim Blocks:** Bonus luas tanah pribadi GriefPrevention langsung bertambah.
   * **Item Eksklusif:** Berlian murni (*Diamonds*) dan mineral langka.

---

## 2. Sistem Random Spawn Survival (`/rtp`)
Untuk memulai petualangan di dunia Survival tanpa harus berjalan ribuan blok dari titik tengah:
* **Perintah:** `/rtp` atau `/wild`
* **Mekanisme Asinkron (AsyncRTP):** Server memindai chunk aman di luar *main thread*, menjamin nol lag pada server saat teleportasi.
* **Keamanan Lokasi:** Algoritma otomatis memfilter dan melarang teleportasi ke tengah samudera dalam, danau lava, atau tebing berbahaya.
* **Warmup & Cooldown:** Diam selama 3 detik sebelum teleportasi. Cooldown penggunaan ulang adalah 60 detik.

---

## 3. Sistem Proteksi Area Pribadi (Anti-Kerusuhan / Anti-Griefing)
Di dunia Survival (`world`), kerusuhan, pencurian peti, perusakan bangunan (*griefing*), dan sabotase dilarang secara sistemik menggunakan sistem proteksi **GriefPrevention**:

### Cara Mengklaim Tanah Pribadi
1. Ambil cangkul emas (**Golden Shovel**):
   * Otomatis didapatkan dari starter kit: `/kit starter`.
2. Klik kanan blok sudut pertama dari tanah yang ingin diproteksi.
3. Berjalan ke sudut diagonal seberangnya, lalu klik kanan blok sudut kedua.
4. Indikator batas emas (*Gold & Glowstone*) akan muncul di tanah menandakan klaim aktif.

### Perintah Manajemen Proteksi
* `/trust <player>` — Memberikan izin membangun dan menghancurkan blok kepada teman.
* `/containertrust <player>` — Mengizinkan teman membuka peti (*chest*), tungku, dan hopper.
* `/accesstrust <player>` — Mengizinkan teman membuka pintu dan tombol.
* `/untrust <player>` — Mencabut seluruh izin akses teman.
* `/abandonclaim` — Menghapus proteksi area yang sedang diinjak dan mengembalikan saldo claim blocks.
* `/claimslist` — Melihat daftar seluruh area yang telah diklaim.

### Akumulasi Claim Blocks
* Pemain baru langsung mendapatkan modal **100 Claim Blocks**.
* Setiap 1 jam aktif bermain mendapatkan tambahan **+100 Claim Blocks**.
* Bonus klaim blok ekstra dapat diraih dengan menyelesaikan tantangan di `/challenge`.

---

## 4. Sistem Deklarasi Perang Sah (*Legitimate Clan War*)
Jika dua kelompok pemain atau faksi memiliki perselisihan wilayah dan ingin bertempur secara sah tanpa dianggap melakukan pelanggaran aturan (*zero-chaos protocol*):

### Pembentukan Clan / Kelompok
* `/clan create <TAG> <NamaClan>` — Mendirikan klan baru (contoh: `/clan create CYB CyberArmy`).
* `/clan invite <player>` — Mengundang anggota baru bergabung.
* `/clan home set` — Menentukan markas klan.
* `/clan home` — Teleportasi ke markas klan.

### Alur Deklarasi Perang Sah
1. **Pernyataan Perang:**  
   Pemimpin klan penantang menjalankan perintah resmi:  
   `/clan war declare <clan_lawan>` atau `/clan war start <clan_lawan>`.
2. **Konfirmasi & Persetujuan:**  
   Pemimpin klan lawan menerima notifikasi deklarasi perang di layar. Jika bersedia meladeni pertempuran, jalankan:  
   `/clan war accept`.
3. **Masa Perang Aktif:**  
   Setelah diterima secara sah, status perang aktif di server:
   * Anggota kedua belah pihak dapat saling menyerang secara legal.
   * Skor pembunuhan (*Kills, Deaths, KDR*) tercatat di papan peringkat klan.
   * Pertempuran dapat dilakukan di alam liar atau di arena resmi `/warp arena`.
4. **Gencatan Senjata / Menyerah:**  
   Kedua pihak dapat mengakhiri perang secara terhormat melalui:  
   `/clan war end`.

---

## 5. Cyber CTF Battle Colosseum (`/warp arena`)
Fasilitas arena turnamen khusus di dunia Skyblock:
* **Format:** Stadion oktagonal 32x32 terapung dengan 4 Menara Beacon Matrix.
* **Fitur:** PVP otomatis aktif di dalam ring arena, dengan perlindungan *KeepInventory* aktif sehingga pemain tidak akan kehilangan barang saat berlatih tanding.
* **Balkon Penonton:** Tribun kaca modern bagi pemain lain yang ingin menonton pertandingan klan atau duel hacker dari atas ring.
