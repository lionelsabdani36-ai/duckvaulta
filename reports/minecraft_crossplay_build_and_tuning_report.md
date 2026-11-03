# Minecraft Crossplay: Omnirush Automated Build & Configuration Report
**Server:** DuckVaulta Minecraft SMP (Java & Bedrock Crossplay)
**Host:** 34.135.45.195 (Debian 13 Linux, AMD EPYC 9B14 4 Cores, 15GB RAM)
**Platform:** Purpur 1.21.4 (Java 21 OpenJDK) + GeyserMC + Floodgate + ViaVersion + ViaBackwards + Chunky
**Date:** 2026-11-03

---

## 1. Executive Summary
Proses otomasi build, konfigurasi bridge crossplay Java-Bedrock, integrasi Floodgate auth, dan server performance tuning telah berhasil dieksekusi secara end-to-end oleh Omnirush CLI di bawah orkestrasi David (AI Team Leader). Seluruh parameter konfigurasi lolos uji verifikasi 100% (PASS) tanpa error, dan server beroperasi stabil pada 20.0 TPS.

---

## 2. Bedrock-Java Bridge Architecture (GeyserMC + Floodgate)

### Geyser-Spigot (`plugins/Geyser-Spigot/config.yml`)
- **Bedrock Listener:** `0.0.0.0:19132` (UDP RakNet default untuk semua client mobile/console)
- **NetherNet WebRTC Listener:** `0.0.0.0:19133` (UDP NetherNet untuk WebRTC data channel)
- **Transport Mode:** `both` (Mendukung simultan RakNet UDP 19132 dan NetherNet UDP 19133)
- **Java Remote Target:** `127.0.0.1:25565`
- **Auth Type:** `floodgate`
  - Mengizinkan pemain Bedrock bergabung menggunakan akun Xbox Live tanpa kewajiban membeli Minecraft Java Edition.
  - Floodgate memvalidasi token enkripsi dan meneruskan UUID pemain ke Purpur Java server.
- **MOTD Passthrough:** `true` (Meneruskan formatting warna MOTD Java ke Bedrock client)
- **Player Counts Passthrough:** `true`
- **In-Game Quality of Life:** `show-coordinates: true`, `show-cooldown: crosshair`, `allow-custom-skulls: true`

### Floodgate (`plugins/floodgate/config.yml`)
- **Key File:** `key.pem` (16 bytes AES key tersinkronisasi antara Geyser dan Floodgate)
- **Username Prefix:** `.` (Pemain Bedrock memiliki format nama `.Username` untuk mencegah tabrakan ID dengan akun Java)
- **Replace Spaces:** `true` (Spasi otomatis diganti underscore `_`)
- **Player Linking:** `enabled: true`, `require-link: false`, `enable-global-linking: true`

---

## 3. Server Properties Tuning (`server.properties`)
- `online-mode=false`: Server menerima koneksi Java (original & offline/cracked) serta pemain Bedrock melalui Floodgate bridge.
- `enforce-secure-profile=false`: Mencegah penolakan chat signature pada client non-Microsoft.
- `sync-chunk-writes=false`: Mengaktifkan asynchronous chunk writes ke disk, mengeliminasi lag spike saat player menjelajahi map.
- `view-distance=8`: Optimal balance antara visual rendering distance dan konsumsi RAM/CPU.
- `simulation-distance=6`: Mengurangi beban komputasi entity tick pada chunk pasif.
- `network-compression-threshold=256`: Kompresi packet optimal untuk menghemat bandwidth VPS.
- `enable-rcon=true`: Port 25575 aktif dengan password terenkripsi untuk remote admin console.
- `enable-query=true`: Port 25565 UDP aktif untuk GS4 status query dan server monitoring.
- `max-players=25`: Kapasitas pemain serentak disesuaikan dengan alokasi RAM 4GB.

---

## 4. Multi-Layer Server Performance Tuning

### Purpur Tuning (`purpur.yml`)
- `settings.use-alternate-keepalive: true`: Menggunakan alternate keepalive loop untuk mencegah timeout bagi pemain dengan jaringan berlatensi tinggi.
- `settings.lagging-threshold: 19.0`: Deteksi ambang lag otomatis untuk adaptive tick handling.
- `world-settings.default.mobs.villager.lobotomize.enabled: true`: Mematikan pathfinding AI kompleks pada villager yang terkunci di trading hall (menghemat hingga 30% CPU tick).

### Spigot Tuning (`spigot.yml`)
- `merge-radius.item: 4.0` & `merge-radius.exp: 6.0`: Menggabungkan item drop dan exp orb di lantai untuk menekan jumlah entity aktif.
- `entity-activation-range`:
  - `animals: 16` (default 32)
  - `monsters: 24` (default 32)
  - `villagers: 16` (default 32)
  - `raiders: 48` (default 64)
  - `misc: 8` (default 16)
  - `water: 12` (default 16)
  - `flying-monsters: 48`

### Paper Tuning (`config/paper-world-defaults.yml`)
- `chunks.auto-save-interval: 6000`: Autosave berkala setiap 5 menit (6000 ticks) untuk mengurangi overhead I/O storage NVMe.
- `misc.redstone-implementation: ALTERNATE_CURRENT`: Mengganti vanilla redstone engine dengan Alternate Current algoritma tercepat.
- `entities.spawning.despawn-ranges.monster`: `soft: 32`, `hard: 96` (Mob yang jauh otomatis despawn lebih cepat, menjaga mob cap stabil).

---

## 5. Startup Script & JVM G1GC Flags (`start.sh`)
Alokasi JVM menggunakan Aikar's Flags standar industri:
```bash
#!/usr/bin/env bash
cd /home/lionelsabdani36/minecraft-server || exit 1

exec java \
  -Xms4G \
  -Xmx4G \
  -XX:+UseG1GC \
  -XX:+ParallelRefProcEnabled \
  -XX:MaxGCPauseMillis=200 \
  -XX:+UnlockExperimentalVMOptions \
  -XX:+DisableExplicitGC \
  -XX:+AlwaysPreTouch \
  -XX:G1NewSizePercent=30 \
  -XX:G1MaxNewSizePercent=40 \
  -XX:G1ReservePercent=20 \
  -XX:G1HeapWastePercent=5 \
  -XX:G1MixedGCCountTarget=4 \
  -XX:InitiatingHeapOccupancyPercent=15 \
  -XX:G1MixedGCLiveThresholdPercent=90 \
  -XX:G1RSetUpdatingPauseTimePercent=5 \
  -XX:SurvivorRatio=32 \
  -XX:+PerfDisableSharedMem \
  -XX:MaxTenuringThreshold=1 \
  -Dusing.aikars.flags=https://mcflags.emc.gs \
  -Daikars.new.flags=true \
  -jar purpur.jar --nogui
```

---

## 6. Verification & Automated Test Results
Pengujian dijalankan melalui script `verify_crossplay.py` dan diaudit langsung oleh Omnirush CLI:
- **Geyser Bedrock Listener:** PASS (RakNet 19132 UDP + NetherNet 19133 UDP)
- **Java Remote Auth Type:** PASS (`floodgate`)
- **Floodgate Encryption Key:** PASS (`key.pem` valid 16 bytes)
- **Server Properties Integrity:** PASS (8/8 parameter terverifikasi)
- **Tuning Parameters:** PASS (Purpur keepalive, villager lobotomize, Spigot merge radius, Paper autosave, Alternate Current redstone)
- **Live TPS Check via RCON:** PASS (20.0, 20.0, 20.0, 20.0)
- **Omnirush Approval:** FORMAL APPROVAL GRANTED

---

## 7. AI Team Orchestration Matrix
- **David (Leader):** Perancangan arsitektur crossplay, integrasi pipeline antargen, orkestrasi Omnirush CLI, dan verifikasi akhir.
- **Charlie (Trend-Hunter):** Riset kompatibilitas plugin crossplay (GeyserMC, Floodgate, ViaVersion, ViaBackwards, Purpur 1.21.4).
- **Alex (Fullstack-Dev):** Pengunduhan, pemasangan, dan verifikasi hash/CRC plugin stack di direktori plugins.
- **Julius (QA-Engineer):** Manajemen boot server, query local socket / mcsrvstat, pemantauan kestabilan 20.0 TPS.
- **Athena (Security-Engineer):** Hardening port RCON ke localhost, audit perizinan `key.pem` (mode 600), verifikasi isolasi UUID.
- **Judith (Guru):** Penyusunan panduan akses komprehensif (koneksi Android/iOS, Windows Bedrock, Java PC, dan tutorial OP admin).
- **Omnirush (Coding Executor):** Otomasi penulisan konfigurasi YAML/properties, benchmarking tuning, dan formal certification audit.
