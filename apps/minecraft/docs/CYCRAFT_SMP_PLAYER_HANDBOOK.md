# ⚡ CYCRAFT SMP — HARDENED SECURITY & ARCHITECTURAL HANDBOOK ⚡

Buku panduan resmi arsitektur server, proteksi anti-griefing, dan referensi perintah lengkap untuk **Cycraft SMP**.

---

## 🌐 INFORMASI AKSES SERVER

- **Host (Domain):** `duckvaulta.ai.id` (IP: `34.135.45.195`)
- **Java Edition:** Port `25565`
- **Bedrock Edition:** Port `19132` (Android, iOS, Windows Bedrock, Konsol)
- **Engine Server:** Purpur 1.21.4 (OpenJDK 21 LTS)
- **Status TPS:** Solid 20.0
- **Unduh Dokumen PDF Resmi:** [https://duckvaulta.ai.id/downloads/cycraft_smp_command_guide.pdf](https://duckvaulta.ai.id/downloads/cycraft_smp_command_guide.pdf)

---

## 🏛️ ARSITEKTUR METROPOLITAN SKYBLOCK & WORLD OVERVIEW

1. **Central Metropolitan Citadel (Spawn Nexus, X=0, Z=0):**
   - **Level 1 (Y=64):** Grand Lobby marmer kuarsa & sirkuit cyan, konter resepsionis, pohon cyber shroomlight, dan central beacon bertenaga netherite.
   - **Level 2 (Y=74):** CSOC (Cyber Security Operations Center) & Server Vault dengan rak server chiseled bookshelf, copper bulb, dan instalasi kabel overhead.
   - **Level 3 (Y=83):** Sky Lounge & VIP Observation Deck dengan balkon kaca panoramik 360 derajat menggantung di atas void.
   - **Level 4 (Y=91):** Rooftop Helipad berkode 'H' emas, radar satelit array, dan antena pemancar petir menjulang ke Y=110.
2. **Metropolitan Elevated Sky-Highways:**
   - Jalan layang selebar 7 blok menghubungkan Nexus ke seluruh sektor.
   - Dilengkapi dinding pelindung ganda (polished deepslate & tinted glass setinggi 2-3 blok) serta lampu end rod berkala sehingga pemain terlindungi penuh dari risiko terpeleset.
3. **CySec Quest Research Complex & Hacker Bunker (Utara, Z=-45 s.d. -80):**
   - Laboratorium riset brutalist tertutup dengan airlock masuk, deretan workstation terminal hacker, dan panggung komando di mana NPC **Quest Master** bertugas.
4. **Grand Cyber Battle Colosseum 2.0 (Timur, X=48 s.d. 102):**
   - Stadion tempur gladiator berbenteng ganda setinggi 10 blok dengan lantai kisi neon sea lantern, benteng pertahanan taktis, dais sentral King of the Hill, serta bunker Red Team (Barat) dan Blue Team (Timur).
5. **Sanctuary Survival Spawn (Overworld, X=64, Y=84, Z=-96):**
   - Paviliun megah berkubah kaca di dunia survival alami yang dilindungi oleh WorldGuard dari segala bentuk griefing, PvP liar, dan monster.

---

## 🛡️ SISTEM PROTEKSI & KEAMANAN ANTI-RUSAK (HARDENED)

1. **CoreProtect v24.1 (Block Audit & Rollback Engine):**
   - Seluruh interaksi peletakan blok, pembongkaran, pembukaan peti/container, pembakaran, dan ledakan dicatat secara presisi ke dalam database SQLite server.
   - Tim administrator dapat melakukan inspeksi instan (`/co i`) dan mengembalikan dunia ke detik sebelum dirusak (`/co rollback`).
2. **GriefPrevention Anti-Theft Hardening:**
   - Penarikan item via Hopper di bawah chest dikunci (`HoppersRequireBuildTrust: true`).
   - Pintu kayu, jebakan trapdoor, tombol, dan tuas diproteksi otomatis dari orang luar yang tidak memiliki trust.
   - Hewan ternak dan peliharaan terlindungi dari serangan pemain lain.
3. **Autonomous Anti-Void Safety Watchdog:**
   - Terintegrasi langsung dalam plugin native `CycraftCyberQuest`.
   - Melakukan monitoring berkala setiap 250ms (5 ticks). Pemain yang jatuh di bawah elevasi Y=48 di skyblock otomatis diselamatkan oleh stabilizer gravitasi dan diteleportasi kembali ke Nexus Spawn tanpa kehilangan nyawa maupun barang.
4. **WorldGuard Multi-Region Hardening:**
   - Region `cyber_skyblock` (__global__): 18 flag proteksi ketat (anti-build, anti-pvp, anti-tnt, anti-creeper, anti-fire, anti-drop, dsb.).
   - Region `cyber_arena`: Khusus mengizinkan PvP dan drop/pickup item di dalam stadion tempur.
   - Region `survival_spawn`: Melindungi pendatang baru di dunia survival agar tidak di-spawnkill atau ditipu.
5. **Vanilla WorldBorder Enforcer:**
   - Dunia skyblock dibatasi radius 400 blok agar pemain fokus di area metropolitan.
   - Dunia survival dibatasi radius 8000 blok untuk menjamin TPS tetap stabil di angka 20.0.

---

## 📜 DAFTAR PERINTAH RESMI PEMAIN

### 1. Navigasi & Hub
- `/warp hub` — Teleportasi ke Grand Metropolitan Citadel.
- `/warp quest` — Menuju CySec Hacker Bunker & NPC Quest Master.
- `/warp arena` — Masuk ke Grand Cyber Battle Colosseum 2.0.
- `/warp survival` — Menuju Sanctuary Spawn di Overworld.
- `/spawn` — Alternatif instan untuk kembali ke titik spawn server.
- `/warps` — Daftar seluruh warp resmi.

### 2. Survival & Proteksi Klaim Tanah
- `/kit starter` — Klaim senjata, obor, Golden Shovel, & Inspection Stick.
- `/rtp` — Teleportasi acak asinkron bebas lag di Overworld.
- `Klik Kanan Golden Shovel` — Menentukan 2 sudut batas klaim wilayah pribadi.
- `Klik Kanan Stick` — Memeriksa kepemilikan dan batas tanah yang sedang dilihat.
- `/trust <player>` — Beri izin bangun dan akses kontainer ke teman.
- `/containertrust <player>` — Hanya izin membuka chest/barrel/furnace.
- `/accesstrust <player>` — Hanya izin membuka pintu dan memencet tombol.
- `/untrust <player>` — Cabut hak akses pemain.
- `/abandonclaim` — Hapus klaim tanah tempat Anda berdiri.
- `/claimslist` — Lihat seluruh lokasi tanah yang Anda miliki.

### 3. Quest CTF Cybersecurity
- `/challenge` — Menu daftar misi cybersecurity dan perolehan hadiah.
- `/challenge <id>` — Baca deskripsi detail soal dan hint target peretasan.
- `/submit <flag>` — Kirim jawaban bendera (`CYBER{...}`).
- `/ctfstats [player]` — Cek rekam jejak penyelesaian tantangan siber.

### 4. Sistem Klan & Perang Sah (SimpleClans)
- `/clan create <tag> <nama>` — Dirikan klan aliansi baru.
- `/clan invite <player>` — Ajak kawan bergabung dalam klan.
- `/clan war declare <clan>` — Nyatakan deklarasi perang resmi.
- `/clan war accept` — Terima tantangan perang dan buka pertempuran.
- `/clan war end` — Usulkan gencatan senjata damai.
- `/clan ff allow / block` — Atur perlindungan friendly-fire sesama klan.
- `/clan stats` — Pantau statistik K/D dan reputasi klan.

### 5. Utilitas Esensial
- `/sethome [nama]` — Simpan koordinat base rumah.
- `/home [nama]` — Teleportasi cepat ke rumah.
- `/tpa <player>` & `/tpaccept` / `/tpdeny` — Sistem teleportasi antar pemain.
- `/balance` & `/pay <player> <jumlah>` — Cek saldo CyBits dan transfer uang.
- `/msg <player> <teks>` — Bisikan rahasia antar pemain.
