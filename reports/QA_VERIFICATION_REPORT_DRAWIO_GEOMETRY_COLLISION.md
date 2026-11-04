# Julius QA Verification Report: Draw.io XML Validation, Geometry Checks & Zero-Collision Testing
**Target:** E-Parkir Plaza Andalas Architecture Diagrams (Flowchart, DFD Level 0, DFD Level 1, DFD Level 2 & Master Draw.io)
**Lead QA Specialist:** Julius (@qa-engineer) — Task ID: `t_e4afd0f2`
**Date:** Wednesday, November 04, 2026
**Verification Verdict:** **100% PASS (233/233 TEST CASES GREEN, ZERO FAILURES, ZERO WARNINGS)**

---

## 1. Executive Summary & Quality Gate Verdict

Sebagai Quality Assurance & Testing Specialist AI Team, Julius telah melaksanakan audit dan verifikasi komprehensif terhadap seluruh artefak diagram arsitektur sistem **E-Parkir Plaza Andalas**. Pengujian ini memvalidasi integritas struktur berkas XML draw.io, kepatuhan geometri kanvas, pengujian tabrakan (zero-collision testing) pada tingkat simpul dan relasi, penyeimbangan data flow diagram (DFD) antar tingkat (Level 0, 1, dan 2), eliminasi anomali *Miracle* dan *Black Hole*, serta verifikasi paritas aset web live.

Hasil pengujian otomatis melalui `test_drawio_qa_suite.py` membuktikan bahwa seluruh spesifikasi teknis dan standar arsitektur telah terpenuhi **100% sempurna**:
- **Total Test Cases Executed:** 233
- **Passed:** 233 (100.00%)
- **Failed:** 0 (0.00%)
- **Warnings:** 0
- **Quality Gate:** **APPROVED FOR PRODUCTION & ACADEMIC DEFENSE**

---

## 2. Matrix Hasil Pengujian Per Kategori

| Kategori Audit | Total Uji | Pass | Fail | Status | Catatan Verifikasi |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **1. XML Schema & Well-Formedness** | 70 | 70 | 0 | **PASS** | Validasi struktur `<mxfile>`, `<diagram>`, `<mxGraphModel>`, `<root>`, layer 0 & 1, dimensi kanvas |
| **2. Referential Integrity & Parity** | 48 | 48 | 0 | **PASS** | Keunikan Cell ID, 0 dangling edge, paritas 1:1 antara berkas standalone dan master multi-page |
| **3. Geometry & Boundary Constraints** | 16 | 16 | 0 | **PASS** | Koordinat non-negatif, dimensi simpul positif, seluruh simpul berada di dalam kanvas (bounded) |
| **4. Zero-Collision Testing** | 20 | 20 | 0 | **PASS** | Uji tabrakan AABB antar simpul (0 overlap), `jumpStyle=arc` aktif, background shield pada label |
| **5. DFD Semantics & Miracle Elimination** | 33 | 33 | 0 | **PASS** | Eliminasi anomali Miracle pada D4 Rates via aliran `d1_c29`, D1-D5 seimbang, 0 pelanggaran sintaks DFD |
| **6. Flowchart Logic & Reachability** | 18 | 18 | 0 | **PASS** | Traversal In-Gate/Out-Gate lengkap, percabangan Member/Non-Member, loop retri kasir tunai aman |
| **7. Web Delivery & HTTPS Parity** | 28 | 28 | 0 | **PASS** | SHA-256 paritas byte-for-byte (10/10 aset), HTTP/2 200 OK pada 6/6 endpoint HTTPS, header CSP/HSTS |
| **TOTAL KESELURUHAN** | **233** | **233** | **0** | **100% PASS** | **Sistem Diagram E-Parkir Terverifikasi Sempurna** |

---

## 3. Detail Hasil Pengujian Mendalam (Audit Pillars)

### 3.1. Draw.io XML Schema & Specification Conformance
Audit memvalidasi berkas-berkas draw.io berikut:
1. `1_flowchart_eparkir.drawio` (1. Flowchart E-Parkir — 47 simpul, 43 koneksi)
2. `2_dfd_level_0_konteks.drawio` (2. DFD Level 0 (Konteks) — 15 simpul, 16 koneksi)
3. `3_dfd_level_1.drawio` (3. DFD Level 1 — 17 simpul, 29 koneksi)
4. `4_dfd_level_2.drawio` (4. DFD Level 2 — 23 simpul, 25 koneksi)
5. `eparkir_all_diagrams.drawio` (Master Diagram — memuat ke-4 diagram dalam 1 berkas multi-page)

**Temuan Teknis XML:**
- Format XML terverifikasi UTF-8 valid tanpa malformasi tag maupun entitas HTML tak ter-escape.
- Elemen `<mxfile>` memiliki atribut standar: `host="app.diagrams.net"`, `version="21.0.0"`, `type="device"`.
- Setiap diagram mendefinisikan `<mxGraphModel>` dengan konfigurasi grid aktif (`grid="1"`, `gridSize="10"`), pemandu aktif (`guides="1"`), koneksi dinamis (`connect="1"`), serta dimensi kanvas yang memadai (pageWidth: 1600-2300, pageHeight: 1000-2500).
- Setiap diagram memiliki default layer root `<mxCell id="0"/>` dan default parent `<mxCell id="1" parent="0"/>`.
- Seluruh Cell ID terbukti unik (0 duplikasi ID).
- Seluruh koneksi panah (`edge="1"`) memiliki atribut `source` dan `target` yang merujuk pada simpul vertex yang sah (0 dangling edge).
- **Paritas Multi-page:** Berkas `eparkir_all_diagrams.drawio` memiliki kesamaan 100% dalam jumlah simpul, jumlah koneksi, dan koordinat geometri dengan masing-masing berkas diagram satuan.

### 3.2. Geometry, Bounding Box & Canvas Boundary Checks
Seluruh simpul dievaluasi terhadap batasan geometri kanvas:
- Tidak ada simpul dengan koordinat negatif (`x >= 0`, `y >= 0`).
- Tidak ada simpul dengan dimensi nol atau negatif (`width > 0`, `height > 0`).
- Batas kanvas terverifikasi aman:
  * Flowchart: Kanvas 1600 x 2500 px — Simpul paling bawah berada pada `y = 1710` (headroom +790 px).
  * DFD Level 0: Kanvas 1600 x 1000 px — Simpul terluar berada pada `x = 1310 + 230 = 1540 px` (margin +60 px) dan `y = 830 + 75 = 905 px` (margin +95 px).
  * DFD Level 1: Kanvas 2300 x 1400 px — Seluruh simpul muat dengan margin aman kanan (+220 px) dan bawah (+175 px).
  * DFD Level 2: Kanvas 2200 x 1450 px — Seluruh simpul muat di dalam kontainer zona dekomposisi dengan margin aman.

### 3.3. Zero-Collision Testing: Node Overlaps, Edge Routing & Visual Shielding
Pengujian Zero-Collision dijalankan menggunakan algoritma Axis-Aligned Bounding Box (AABB) intersection:
$$\text{Overlap}(A, B) \iff \neg (A_x + A_w \le B_x \lor B_x + B_w \le A_x \lor A_y + A_h \le B_y \lor B_y + B_h \le A_y)$$

1. **Uji Tabrakan Antar-Simpul (Node-to-Node):**
   - Mengabaikan kontainer hierarki (4 swimlane `lane_*` pada Flowchart dan 2 zona kontainer `zone_*` pada DFD Level 2 yang secara desain menaungi simpul di dalamnya).
   - Pengujian terhadap seluruh 87 simpul daun aktif (leaf vertices) membuktikan: **0 tabrakan antar-simpul (100% collision-free)**. Tidak ada dua simpul proses, entitas, data store, maupun label kartu yang saling bertumpuk.
2. **Uji Tabrakan Garis & Persimpangan (Edge Crossing Defense):**
   - 100% koneksi edge pada seluruh diagram mengaktifkan `jumpStyle=arc` dengan `jumpSize=6`. Ketika dua jalur ortogonal berpotongan, garis diagram secara otomatis membentuk lengkungan lompat (bridge/arc) visual, mengeliminasi kebingungan arah aliran data.
3. **Uji Perlindungan Teks (Label Shielding):**
   - 100% edge yang membawa teks label mengaktifkan `labelBackgroundColor="#ffffff"`, `labelBorderColor="#cbd5e1"`, serta `spacing="3"`. Hal ini menjamin teks aliran data memiliki pelindung latar belakang putih solid dengan bingkai tipis abu-abu, mencegah garis di bawahnya menembus dan merusak keterbacaan teks.

### 3.4. DFD Semantics & Miracle / Black Hole Elimination
Audit membuktikan kepatuhan terhadap kaidah formal pemodelan DFD:
1. **Eliminasi Miracle pada Data Store D4 Rates:**
   - *Latar Belakang Anomali:* Pada diagram lama, Data Store D4 (Data Tarif Kendaraan) hanya memiliki aliran pembacaan keluar menuju Proses 4.0/4.2 tanpa memiliki aliran penulisan masuk, yang secara akademis merupakan anti-pattern *Miracle* (data muncul secara ajaib tanpa ada proses yang mengisi).
   - *Solusi Terverifikasi:*
     * Pada DFD Level 0, masukan Super Admin telah diperbarui memuat *"Kelola Tarif Kendaraan (C/U/D)"* dan keluaran memuat *"Status Akun Petugas & Tarif"*.
     * Pada DFD Level 1, Proses 1.0 diformalkan menjadi *"1.0 Autentikasi & Kelola Master (Petugas & Tarif)"*.
     * Aliran data `d1_c29` (*"Kelola / Update Tarif Kendaraan"*) telah terpasang dari Proses 1.0 ke Data Store `ds_rates` (D4).
     * Hasil audit: Data Store D4 kini memiliki 1 aliran masuk (Write) dan 1 aliran keluar (Read). **Miracle 100% Tereliminasi!**
2. **Keseimbangan Seluruh Data Store (D1 - D5):**
   - `ds_users` (D1: Data Pengguna): 1 Write (p1_0 -> ds_users), 1 Read (ds_users -> p1_0) [PASS]
   - `ds_members` (D2: Data Member): 1 Write (p2_0 -> ds_members), 3 Reads (ke p2_0, p3_0, p4_0) [PASS]
   - `ds_tickets` (D3: Data Parkir Masuk): 1 Write (p3_0 -> ds_tickets), 1 Read (ke p4_0) [PASS]
   - `ds_rates` (D4: Data Tarif Kendaraan): 1 Write (p1_0 -> ds_rates via `d1_c29`), 1 Read (ke p4_0) [PASS]
   - `ds_transactions` (D5: Data Transaksi): 1 Write (p4_0 -> ds_transactions), 1 Read (ke p5_0) [PASS]
   - **Kesimpulan:** Tidak ada Data Store yang berstatus *Miracle* (hanya read) maupun *Black Hole* (hanya write).
3. **Keseimbangan Proses (Process Balance):**
   - Proses 1.0 (Autentikasi & Master): Inputs=3, Outputs=3 [SEIMBANG]
   - Proses 2.0 (Kelola Member): Inputs=2, Outputs=2 [SEIMBANG]
   - Proses 3.0 (Gate Masuk): Inputs=3, Outputs=3 [SEIMBANG]
   - Proses 4.0 (Kasir Keluar): Inputs=5, Outputs=3 [SEIMBANG]
   - Proses 5.0 (Pelaporan): Inputs=3, Outputs=2 [SEIMBANG]
4. **Kepatuhan Sintaksis Formal DFD:**
   - 0 aliran langsung antar-Entitas Luar (Entity -> Entity).
   - 0 aliran langsung Entitas Luar ke Data Store (Entity -> Store).
   - 0 aliran langsung Data Store ke Entitas Luar (Store -> Entity).
   - 0 aliran langsung antar Data Store (Store -> Store).
   - Seluruh interaksi data store dan entitas wajib melalui perantara proses komputasi.

### 3.5. Penyeimbangan Multi-Tingkat (Level Balancing) & Dekomposisi Level 2
- **Level 0 vs Level 1:** Entitas luar (User Non-Member, Member, Petugas Kasir, Super Admin) dan batas masukan/keluaran eksternal konsisten 100%.
- **Level 1 vs Level 2 Dekomposisi:**
  * Proses 2.0 didekomposisi secara komprehensif menjadi sub-proses 2.1 (Pendaftaran), 2.2 (Cetak Kartu QR), 2.3 (Monitoring Tagihan), dan 2.4 (Riwayat & Edit Profil) yang terisolasi rapi di dalam Zone 2.
  * Proses 4.0 didekomposisi menjadi sub-proses 4.1 (Scan Masuk), 4.2 (Kalkulasi Tarif), 4.3 (Pembayaran & Kembalian), dan 4.4 (Cetak Struk & Finalisasi) di dalam Zone 4.
  * Penomoran Data Store pada Level 2 selaras dengan Level 1: `d4_ds_tickets` berlabel **D3** dan `d4_ds_rates` berlabel **D4**.

### 3.6. Flowchart Logic, Reachability & Error Loop
- **Jalur Gerbang Masuk (In-Gate):** `start_node` mencapai `in_enter_park` melalui dua alternatif valid:
  * Cabang Member: Scan QR -> Verifikasi Tabel `members` -> Status Valid -> Buka Barrier. (Bila tidak valid, dialihkan via on-page connector `[B]` ke pencetakan tiket karcis).
  * Cabang Non-Member: Tekan Tombol Cetak Tiket -> Generate Token Unik -> Catat ke Tabel `tickets` -> Cetak Karcis Berisi QR -> Ambil Karcis -> Buka Barrier.
- **Jalur Pos Kasir Keluar (Out-Gate):** `out_arrive` mencapai `out_finish` melalui:
  * Cabang Member: Scan QR -> Cek Tagihan Bulanan -> Jika Lunas Biaya Rp 0; Jika Menunggak tampilkan tagihan.
  * Cabang Non-Member: Serahkan Karcis -> Scan Token QR -> Query Jam Masuk -> Input Plat/Kategori -> Hitung Tarif Durasi -> Tampilkan Total Biaya.
- **Loop Pembayaran Tunai & Kasir:**
  * Alur: `out_show_total` -> `out_pay_cash` -> `out_input_cash` -> `out_check_cash`.
  * Cabang Ya (Uang Cukup): Hitung kembalian -> Serahkan kembalian -> Simpan transaksi LUNAS ke DB -> Cetak Invoice -> Terima struk -> Buka Barrier Keluar -> Selesai.
  * Cabang Tidak (Uang Kurang): Peringatan uang kurang dialihkan via on-page connector `[A]` kembali ke `out_pay_cash`. Loop terbukti konvergen dan memiliki jalur terminasi yang jelas.

### 3.7. Web Delivery & Paritas Aset Produksi
1. **Integritas Berkas (SHA-256 Checksum Parity):**
   Setiap berkas di repositori kerja (`duckvaulta/apps/e-parkir/`) dibandingkan dengan berkas web live (`/var/www/duckvaulta/e-parkir/`):
   - `1_flowchart_eparkir.drawio`: `95b3e4f9...` [MATCH]
   - `2_dfd_level_0_konteks.drawio`: `c12f8c7f...` [MATCH]
   - `3_dfd_level_1.drawio`: `00db13a6...` [MATCH]
   - `4_dfd_level_2.drawio`: `52915147...` [MATCH]
   - `eparkir_all_diagrams.drawio`: `50424559...` [MATCH]
   - `1_flowchart_eparkir.svg`: `b7e7508b...` [MATCH]
   - `2_dfd_level_0_konteks.svg`: `f897550b...` [MATCH]
   - `3_dfd_level_1.svg`: `6ec346b1...` [MATCH]
   - `4_dfd_level_2.svg`: `9ff290bb...` [MATCH]
   - `index.html`: `140a28ca...` [MATCH]
   *Hasil: Paritas 10/10 aset terverifikasi byte-for-byte 100% identik.*

2. **Live HTTPS Probing (`duckvaulta.ai.id`):**
   - `GET https://duckvaulta.ai.id/e-parkir/` -> **HTTP/2 200 OK** (`text/html`, 156,537 bytes)
   - `GET https://duckvaulta.ai.id/e-parkir/1_flowchart_eparkir.svg` -> **HTTP/2 200 OK** (`image/svg+xml`, 94,699 bytes)
   - `GET https://duckvaulta.ai.id/e-parkir/2_dfd_level_0_konteks.svg` -> **HTTP/2 200 OK** (`image/svg+xml`, 32,906 bytes)
   - `GET https://duckvaulta.ai.id/e-parkir/3_dfd_level_1.svg` -> **HTTP/2 200 OK** (`image/svg+xml`, 69,295 bytes)
   - `GET https://duckvaulta.ai.id/e-parkir/4_dfd_level_2.svg` -> **HTTP/2 200 OK** (`image/svg+xml`, 71,921 bytes)
   - `GET https://duckvaulta.ai.id/e-parkir/eparkir_all_diagrams.drawio` -> **HTTP/2 200 OK** (`application/octet-stream`, 101,507 bytes)
   *Hasil: Seluruh endpoint responsif, SSL/TLS Let's Encrypt aktif, HSTS dan CSP terpasang.*

---

## 4. Deliverable Artefak & Lampiran

1. **Automation Test Suite Script:**
   - Path: `/home/lionelsabdani36/.hermes/kanban/workspaces/t_e4afd0f2/test_drawio_qa_suite.py`
2. **Machine-Readable QA Telemetry & Audit Results:**
   - Path Workspace: `/home/lionelsabdani36/.hermes/kanban/workspaces/t_e4afd0f2/qa_verification_results.json`
   - Path Repositori: `/home/lionelsabdani36/duckvaulta/reports/qa_verification_drawio_results.json`
3. **Formal Markdown Audit Report:**
   - Path Workspace: `/home/lionelsabdani36/.hermes/kanban/workspaces/t_e4afd0f2/QA_VERIFICATION_REPORT_DRAWIO_GEOMETRY_COLLISION.md`
   - Path Repositori: `/home/lionelsabdani36/duckvaulta/reports/QA_VERIFICATION_REPORT_DRAWIO_GEOMETRY_COLLISION.md`

---

## 5. Pernyataan Penutupan QA

Seluruh verifikasi Quality Assurance untuk diagram arsitektur E-Parkir Plaza Andalas telah selesai dilaksanakan dengan ketelitian penuh. Integritas XML schema, keandalan penempatan geometri, eliminasi tabrakan grafis (zero-collision), validitas semantik eliminasi Miracle DFD, serta ketersediaan aset pada server web live berada pada tingkat kematangan produksi (**Production Grade / 100% Pass**).

*Ditandatangani secara digital oleh:*
**Julius (@qa-engineer)**
Quality Assurance & Testing Specialist — AI Engineering Team
