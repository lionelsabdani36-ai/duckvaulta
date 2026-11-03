# LAPORAN PRAKTIK KELOMPOK PROYEK KEWARGANEGARAAN
## Studi Kasus & Audit Sederhana Transparansi Layanan Publik di Lingkungan Sekitar: Kementerian Sosial Republik Indonesia (Kemensos RI)

**Mata Kuliah / Pelajaran:** Pendidikan Kewarganegaraan  
**Fokus Kajian:** Keterbukaan Informasi Publik, Efektivitas Pelayanan Bantuan Sosial, dan Akuntabilitas Penanganan Pengaduan Masyarakat  
**Objek Audit Digital:** Portal Resmi `kemensos.go.id`, `ppid.kemensos.go.id`, dan `cekbansos.kemensos.go.id`  
**Tahun Akademik:** 2026  

---

## RINGKASAN EKSEKUTIF (EXECUTIVE SUMMARY)

Laporan ini disusun sebagai pemenuhan tugas praktik kelompok Proyek Kewarganegaraan dengan tema *"Studi Kasus & Audit Sederhana Transparansi Layanan Publik di Lingkungan Sekitar"*. Kelompok kami memilih **Kementerian Sosial Republik Indonesia (Kemensos RI)** sebagai entitas objek audit karena lembaga ini mengelola anggaran bantuan sosial (bansos) bernilai sangat besar (berkisar antara Rp 75 hingga Rp 80 Triliun per tahun) yang bersentuhan langsung dengan hak dasar warga miskin dan rentan.

Audit sederhana ini mengevaluasi kinerja Kementerian Sosial melalui 3 indikator pokok:
1. **Transparansi Anggaran:** Ketersediaan dan keterbukaan dokumen perencanaan, penganggaran (DIPA), dan laporan keuangan auditan.
2. **Kemudahan Alur Pelayanan:** Aksesibilitas portal `cekbansos.kemensos.go.id`, mekanisme Data Terpadu Kesejahteraan Sosial (DTKS), serta partisipasi warga melalui fitur "Usul-Sanggah".
3. **Penanganan Keluhan Warga:** Responsivitas saluran pengaduan Command Center 171 (24 Jam Bebas Pulsa), integrasi SP4N-LAPOR!, dan Whistleblowing System (WBS).

Hasil pengamatan digital dan kajian data sekunder (LHP BPK RI dan evaluasi Komisi Informasi Pusat) menunjukkan bahwa Kemensos RI telah mencapai predikat **Badan Publik Informatif** dengan kepatuhan unggah dokumen berkala yang baik. Namun demikian, audit mengidentifikasi sejumlah kelemahan struktural: dokumen anggaran masih bersifat pasif (PDF tebal) tanpa dashboard spasial per kelurahan; terjadi jurang pemisah digital (*digital divide*) pada warga miskin pelosok dan lansia yang belum memiliki gawai cerdas; serta lamanya siklus penyelesaian sengketa kartu bansos non-aktif (30–60 hari).

Sebagai luaran penugasan, kelompok kami menyusun **4 Rekomendasi Solusi Inovatif** berbasis teknologi dan tata kelola:
1. Portal Dashboard Bansos Interaktif (*Open Budget Web-GIS*);
2. Kanal Multisaluran WhatsApp Bot Terverifikasi & SMS Gratis 1708;
3. Pelacakan Tiket Keluhan Transparan dengan SLA 7 Hari Berbasis Notifikasi SMS;
4. Posko Pendampingan Digital Desa Jemput Bola bagi Kaum Lansia dan Disabilitas.

Seluruh materi telah diwujudkan dalam slide presentasi 16:9 siap tayang (`Audit_Transparansi_Kemensos_Kelompok.pptx`), infografis visual beresolusi tinggi (1080p), serta web viewer interaktif yang dapat diakses publik pada domain `https://duckvaulta.ai.id/kemensos-audit/`.

---

## BAB I: PENDAHULUAN

### 1.1 Latar Belakang Masalah
Pelayanan publik merupakan tolak ukur paling nyata dari kehadiran negara dalam kehidupan warganya. Dalam era keterbukaan informasi dan transformasi digital, masyarakat menuntut birokrasi yang transparan, mudah diakses, akuntabel, dan bebas dari korupsi. Pasal 28F Undang-Undang Dasar Negara Republik Indonesia Tahun 1945 secara tegas menyatakan bahwa setiap orang berhak untuk berkomunikasi dan memperoleh informasi untuk mengembangkan pribadi dan lingkungan sosialnya, serta berhak untuk mencari, memperoleh, memiliki, menyimpan, mengolah, dan menyampaikan informasi dengan menggunakan segala jenis saluran yang tersedia.

Di antara berbagai kementerian teknis, Kementerian Sosial Republik Indonesia (Kemensos RI) memegang peranan krusial sebagai garda terdepan perlindungan sosial nasional. Program-program strategis seperti Program Keluarga Harapan (PKH), Bantuan Pangan Non-Tunai (BPNT/Sembako), dan Bantuan Sosial Kebencanaan mengalokasikan dana puluhan triliun rupiah setiap tahun anggaran. Besarnya volume anggaran ini mengharuskan adanya transparansi menyeluruh guna mencegah kebocoran, praktik rente, nepotisme pendataan, serta salah sasaran (*inclusion error* dan *exclusion error*).

Sebagai generasi pembelajar kewarganegaraan, mahasiswa/siswa dituntut untuk tidak sekadar memahami teori konstitusi di ruang kelas, tetapi juga mampu melakukan audit sosial (*civic audit*) terhadap lembaga pelayanan publik di sekitarnya. Pengamatan kritis terhadap platform digital Kemensos RI menjadi studi kasus ideal untuk menakar keselarasan antara norma hukum keterbukaan informasi publik dan kenyataan pelayanan di lapangan.

### 1.2 Rumusan Masalah
Berdasarkan rubrik penugasan proyek kewarganegaraan, masalah dirumuskan ke dalam pertanyaan-pertanyaan berikut:
1. Sejauh mana Kementerian Sosial RI membuka informasi anggaran belanja perlindungan sosial dan dokumen pertanggungjawaban fiskal kepada masyarakat umum?
2. Bagaimana efektivitas dan kemudahan alur pelayanan bantuan sosial digital melalui platform `cekbansos.kemensos.go.id` dan aplikasi mobile, serta hambatan apa yang dihadapi warga rentan?
3. Seberapa responsif saluran penanganan keluhan Kemensos (Command Center 171 dan SP4N-LAPOR!) dalam menindaklanjuti ketidakakuratan data dan sengketa hak bantuan warga?
4. Solusi strategis dan desain infografis apa yang dapat direkomendasikan untuk menyempurnakan kualitas pelayanan publik Kemensos RI?

### 1.3 Tujuan Penugasan Praktik Kelompok
1. Melakukan pengamatan lapangan digital (*digital field observation*) terhadap portal resmi dan layanan daring Kemensos RI.
2. Menganalisis secara objektif kelebihan dan kekurangan pada 3 indikator utama (Transparansi Anggaran, Alur Pelayanan, dan Penanganan Keluhan).
3. Menyusun dokumen matriks evaluasi berbasis bukti empiris dan audit regulator resmi (KIP, BPK, KPK).
4. Merancang infografis rekomendasi perbaikan layanan yang aplikatif dalam format PowerPoint (16:9) dan grafis visual.
5. Membangun refleksi kritis mengenai nilai-nilai Pancasila (khususnya Sila ke-5) dan partisipasi aktif warga negara (*active citizenship*).

### 1.4 Landasan Yuridis & Konstitusional
Audit kewarganegaraan ini berpijak pada kerangka hukum perundang-undangan Republik Indonesia:
1. **UUD NRI 1945:**
   - **Pasal 28F:** Hak atas pemenuhan dan akses informasi publik.
   - **Pasal 34 ayat (1) & (2):** Fakir miskin dan anak terlantar dipelihara oleh negara; negara mengembangkan sistem jaminan sosial bagi seluruh rakyat.
2. **Undang-Undang No. 14 Tahun 2008 tentang Keterbukaan Informasi Publik (UU KIP):**
   - Mengatur kewajiban badan publik mengumumkan informasi berkala, informasi serta-merta, dan informasi setiap saat.
3. **Undang-Undang No. 25 Tahun 2009 tentang Pelayanan Publik:**
   - Menetapkan standar pelayanan, maklumat pelayanan, kepastian waktu, dan penyediaan sistem pengaduan yang transparan dan terukur.
4. **Undang-Undang No. 13 Tahun 2011 tentang Penanganan Fakir Miskin:**
   - Mengatur legalitas Data Terpadu Kesejahteraan Sosial (DTKS) dan mekanisme verifikasi-validasi berjenjang.
5. **Undang-Undang No. 27 Tahun 2022 tentang Pelindungan Data Pribadi (UU PDP):**
   - Mengharuskan lembaga pemerintah mengamankan NIK dan data sensitif warga negara dalam portal layanan publik terbuka.

---

## BAB II: PROFIL LEMBAGA & METODOLOGI PENGAMATAN

### 2.1 Profil Singkat Kementerian Sosial RI
Kementerian Sosial Republik Indonesia adalah kementerian dalam Pemerintah Indonesia yang membidangi urusan sosial. Kemensos bertugas menyelenggarakan urusan pemerintahan di bidang sosial untuk membantu Presiden dalam menyelenggarakan pemerintahan negara. Struktur utama Kemensos meliputi Direktorat Jenderal Perlindungan dan Jaminan Sosial (Linjamsos), Direktorat Jenderal Pemberdayaan Sosial (Dayasos), Direktorat Jenderal Rehabilitasi Sosial (Rehsos), dan Inspektorat Jenderal.

### 2.2 Objek Pengamatan Digital
Pengamatan kelompok difokuskan pada infrastruktur digital pelayanan publik Kemensos:
1. **Portal Utama (`kemensos.go.id`):** Etalase informasi kebijakan menteri, program prioritas, regulasi (Permensos/Kepmensos), siaran pers, dan berita operasional.
2. **Portal PPID (`ppid.kemensos.go.id`):** Pejabat Pengelola Informasi dan Dokumentasi yang menyajikan Daftar Informasi Publik (DIP), DIPA, RKA-K/L, Laporan Kinerja (LAKIP), serta tata cara permohonan informasi publik.
3. **Portal Pengecekan Mandiri (`cekbansos.kemensos.go.id`):** Aplikasi berbasis web yang memungkinkan siapa saja mengecek status kepesertaan bansos berdasarkan wilayah administrasi dan nama.
4. **Aplikasi Mobile "Cek Bansos" (Android OS):** Aplikasi mobile yang dilengkapi fitur pembuatan akun terverifikasi identitas kependudukan dan modul "Usul-Sanggah".
5. **Layanan Terpadu & Saluran Kontak:** Call Center Command Center 171 (bebas pulsa 24 jam), portal SP4N-LAPOR!, dan kanal Whistleblowing System (`wbs.kemensos.go.id`).

### 2.3 Metodologi Audit Sederhana
Metodologi yang digunakan adalah pendekatan kualitatif-deskriptif berbasis audit sosial digital:
1. **Digital Walkthrough & User Journey:** Kelompok menguji secara langsung navigasi situs web resmi dari sudut pandang warga pengguna biasa (kecepatan memuat, ketersediaan tautan, kemudahan pencarian dokumen, keterbacaan pada perangkat seluler).
2. **Heuristic Evaluation Layanan Publik:** Menguji ketersediaan informasi wajib sesuai standar Perki No. 1 Tahun 2021 tentang Standar Layanan Informasi Publik.
3. **Triangulasi Data Sekunder:** Membandingkan temuan antarmuka web dengan laporan independen lembaga pengawas negara:
   - Hasil Penilaian Keterbukaan Informasi Publik oleh Komisi Informasi Pusat (KIP).
   - Laporan Hasil Pemeriksaan (LHP) atas Pengelolaan Bansos oleh Badan Pemeriksa Keuangan (BPK RI).
   - Kajian Tata Kelola Bansos dan Integritas DTKS oleh Komisi Pemberantasan Korupsi (KPK RI).

---

## BAB III: HASIL AUDIT & ANALISIS 3 INDIKATOR

### 3.1 Indikator 1: Transparansi Anggaran
Keterbukaan fiskal adalah pilar utama pencegahan korupsi. Mengingat alokasi belanja bansos Kemensos mencapai kisaran Rp 75 - 80 Triliun per tahun, keterbukaan informasi penggunaan anggaran menjadi keharusan mutlak.

#### A. Fakta dan Temuan Lapangan
- Pada portal PPID Kemensos (`ppid.kemensos.go.id`), kelompok menemukan tabulasi "Informasi Berkala" yang memuat dokumen DIPA (Daftar Isian Pelaksanaan Anggaran) tahun anggaran 2022, 2023, hingga 2024.
- Tersedia dokumen Rencana Kerja dan Anggaran Kementerian/Lembaga (RKA-K/L), Laporan Akuntabilitas Kinerja Instansi Pemerintah (LAKIP/LKjP), serta ringkasan Laporan Keuangan auditan BPK RI.
- Laporan Keuangan Kemensos RI konsisten memperoleh opini **Wajar Tanpa Pengecualian (WTP)** dari BPK RI selama beberapa tahun berturut-turut.
- Komisi Informasi Pusat (KIP) memberikan predikat **Badan Publik Informatif** bagi Kemensos RI atas komitmen publikasi reguler ini.

#### B. Evaluasi Kritis: Kelebihan vs Kekurangan
- **Kelebihan (Good Practice):**
  1. Kepatuhan regulasi terhadap UU No. 14/2008 dan Perki No. 1/2021 sangat tinggi; dokumen wajib tersedia tanpa harus mengajukan sengketa informasi.
  2. Keterbukaan rincian alokasi belanja bantuan sosial per unit eselon I dapat dipantau masyarakat umum dan pegiat transparansi anggaran.
- **Kekurangan & Catatan Kritis:**
  1. **Format Pasif & Dokumen Raksasa:** Seluruh dokumen anggaran diunggah dalam format PDF pindaian atau tabel ratusan halaman yang kaku. Masyarakat awam yang bukan sarjana ekonomi atau akuntan publik akan sangat kesulitan membaca dan memahami angka-angka tersebut.
  2. **Ketiadaan Realisasi Mikro Spasial:** Warga tidak dapat memantau realisasi anggaran secara riil hingga level kecamatan, desa, apalagi RW/RT melalui portal web.
  3. **Minimnya Format Data Terbuka (Open Data):** Belum tersedia API publik, data tabular CSV/JSON mentah yang mudah diolah oleh akademisi, media massa, maupun pengembang aplikasi pemantau korupsi independen.

---

### 3.2 Indikator 2: Kemudahan Alur Pelayanan (DTKS & Bansos)
Alur pelayanan publik mencerminkan sejauh mana birokrasi mempermudah atau justru mempersulit pemenuhan hak-hak dasar warga negara sesuai amanat UU No. 25/2009.

#### A. Fakta dan Temuan Lapangan
- Melalui portal `cekbansos.kemensos.go.id`, siapa pun dapat memeriksa status bantuan tanpa perlu login akun atau membuat kata sandi. Cukup memilih Provinsi, Kabupaten/Kota, Kecamatan, Desa/Kelurahan, dan memasukkan nama sesuai KTP.
- Kemensos meluncurkan aplikasi mobile "Cek Bansos" di platform Android yang dilengkapi fitur inovatif **"Usul-Sanggah"**. Fitur ini memungkinkan warga secara mandiri mengusulkan tetangganya yang miskin agar masuk DTKS, atau menyanggah penerima bansos yang dinilai sudah mapan secara ekonomi (misalnya memiliki mobil, rumah mewah, atau berstatus ASN).
- Pemutakhiran DTKS dilakukan secara terpusat dan berjenjang melalui sistem daring SIKS-NG (Sistem Informasi Kesejahteraan Sosial Next Generation) yang dikelola oleh operator Dinas Sosial kabupaten/kota.

#### B. Evaluasi Kritis: Kelebihan vs Kekurangan
- **Kelebihan (Good Practice):**
  1. Efisiensi tinggi: Pengecekan tanpa login pada web browser memutus potensi pungutan liar dan manipulasi status bantuan oleh calo lokal atau oknum pamong desa.
  2. Partisipasi publik dilembagakan melalui fitur Usul-Sanggah di aplikasi ponsel pintar.
- **Kekurangan & Hambatan di Lapangan:**
  1. **Jurang Kesenjangan Digital (*Digital Divide*):** Kelompok sasaran utama bansos adalah masyarakat miskin ekstrem, keluarga prasejahtera pelosok, lansia sebatang kara, dan penyandang disabilitas berat. Sebagian besar dari mereka tidak memiliki smartphone, tidak mampu membeli paket data, atau buta huruf digital (*digital illiteracy*). Akibatnya, mereka yang paling membutuhkan justru paling tidak mampu mengakses platform ini secara mandiri.
  2. **Bottleneck Verifikasi di Tingkat Daerah:** Usulan warga lewat fitur Usul-Sanggah tidak serta-merta cair. Usulan tersebut harus diverifikasi ulang lewat Musyawarah Kelurahan/Desa (Musdes) dan ditandatangani oleh Kepala Daerah sebelum disahkan oleh Mensos. Banyak pemerintah daerah lambat atau pasif dalam memvalidasi data usulan warga.
  3. **Kendala Verifikasi KTP (OCR Issue):** Banyak ulasan warga di Google Play Store mengeluhkan kegagalan verifikasi swafoto KTP akibat algoritma pemindaian otomatis (OCR) yang terlalu sensitif terhadap kualitas kamera ponsel murah atau kondisi KTP yang telah buram.

---

### 3.3 Indikator 3: Penanganan Keluhan Warga
Sistem penanganan aduan adalah indikator vital untuk menguji seberapa peduli lembaga terhadap keluhan, ketidakadilan, dan malapraktik birokrasi.

#### A. Fakta dan Temuan Lapangan
- **Command Center 171:** Saluran panggilan bebas pulsa 24 jam sehari, 7 hari seminggu (24/7) yang disediakan Kemensos untuk merespons kasus kedaruratan sosial, kekerasan perempuan dan anak, anak telantar, serta respon bencana.
- **Integrasi SP4N-LAPOR!:** Seluruh keluhan tertulis diintegrasikan ke sistem nasional `lapor.go.id` dan SMS 1708 yang diawasi oleh Kementerian PAN-RB, Ombudsman RI, dan Kantor Staf Presiden (KSP).
- **Whistleblowing System (WBS):** Portal daring `wbs.kemensos.go.id` yang dirancang dengan jaminan anonimitas untuk pelaporan tindak pidana korupsi pegawai, pemotongan dana bansos, atau gratifikasi.
- **Tim Reaksi Cepat (TRC):** Kemensos memiliki satuan tugas lapangan yang aktif mendatangi korban atau lokasi aduan viral di media sosial dalam hitungan jam.

#### B. Evaluasi Kritis: Kelebihan vs Kekurangan
- **Kelebihan (Good Practice):**
  1. Kecepatan respon kedaruratan sosial luar biasa tinggi; laporan kekerasan atau penelantaran lansia melalui 171 langsung direspons dengan penjemputan ke balai rehabilitasi sosial.
  2. Penggunaan platform nasional SP4N-LAPOR! memberikan nomor tiket tracking resmi yang dapat dicek publik.
- **Kelemahan & Catatan Kritis:**
  1. **Sengketa Kepesertaan Bansos Memakan Waktu Lama:** Keluhan yang paling dominan di masyarakat adalah kasus: *"Bulan lalu bansos cair, kenapa bulan ini saldo kartu ATM/KKS kosong?"*. Penanganan keluhan semacam ini memakan waktu sangat panjang (30 hingga 60 hari kerja), karena melibatkan verifikasi antar-lembaga yang rumit: bank penyalur (Himbara), Ditjen Linjamsos, Pusdatin Kemensos, dan Dinas Sosial daerah.
  2. **Minimnya Umpan Balik Alasan Pencoretan:** Ketika nama seorang warga dicoret dari DTKS atau dinilai tidak layak, sistem sering kali hanya memberikan status generik *"Tidak Layak Bansos"* tanpa penjelasan rincian aset apa yang menyebabkan pencoretan tersebut (misalnya: tagihan listrik >900VA, ada anggota keluarga berstatus ASN, atau terdeteksi kepemilikan BPJS Ketenagakerjaan upah di atas UMR). Hal ini memicu kecurigaan dan frustrasi di kalangan warga miskin.
  3. **Belum Tersedianya Kanal Pesan Instan (WhatsApp Resmi):** Layanan pengaduan masih didominasi panggilan telepon suara (171) dan form web, padahal kanal komunikasi paling populer bagi masyarakat Indonesia kelas menengah ke bawah adalah aplikasi pesan WhatsApp.

---

## BAB IV: MATRIKS KOMPARATIF & TEMUAN AUDIT OBJEKTIF

Tabel berikut merangkum hasil evaluasi komparatif pada ketiga indikator layanan publik:

| No | Indikator Evaluasi | Bukti Digital / Dokumen Acuan | Kelebihan (Praktik Positif) | Kelemahan (Ruang Perbaikan) | Skor (Skala 1-10) |
|---|---|---|---|---|:---:|
| 1 | **Transparansi Anggaran** | Portal `ppid.kemensos.go.id`, Dokumen DIPA 2022-2024, Laporan Keuangan WTP BPK RI | Dokumen lengkap diunggah berkala; konsisten meraih predikat Informatif dari Komisi Informasi Pusat (KIP). | Dokumen berbentuk PDF tebal non-interaktif; belum ada open data visual real-time per kecamatan/desa. | **8.5** |
| 2 | **Kemudahan Alur Pelayanan** | Portal `cekbansos.kemensos.go.id`, Aplikasi Mobile Play Store, Audit KPK atas DTKS | Cek bansos tanpa login memutus celah pungli; fitur Usul-Sanggah membuka ruang partisipasi warga. | Kendala *digital divide* bagi lansia/miskin pelosok; verifikasi musdes daerah lambat; error OCR KTP. | **7.8** |
| 3 | **Penanganan Keluhan Warga** | Call Center Bebas Pulsa 171, SP4N-LAPOR!, `wbs.kemensos.go.id`, Satgas TRC | Command Center 171 aktif 24 jam bebas pulsa; respons kasus kedaruratan sosial sangat tanggap di lapangan. | Sengketa pembekuan kartu bansos butuh waktu 30-60 hari; minim transparansi alasan pencoretan nama. | **8.0** |

**Skor Rata-Rata Keterbukaan & Layanan Kemensos RI: 8.1 / 10 (Kategori: Baik / Cukup Memuaskan dengan Catatan Aksesibilitas)**

---

## BAB V: INFOGRAFIS REKOMENDASI & SOLUSI STRATEGIS

Sebagai wujud kontribusi konstruktif mahasiswa/siswa, kelompok merekomendasikan **4 Solusi Terintegrasi** yang dirangkum ke dalam satu lembar infografis rekomendasi (tertera pada Slide 7 PPTX dan visual banner web):

### 5.1 Solusi 1: Dashboard Bansos Interaktif (Open Budget Web-GIS)
- **Konsep:** Mentransformasikan tumpukan dokumen PDF DIPA dan tabel angka yang rumit menjadi peta tematik spasial (Geographic Information System) yang interaktif dan ramah warga (*citizen-friendly*).
- **Mekanisme Kerja:** Warga dapat membuka peta Indonesia di peramban, mengeklik wilayah provinsinya, hingga memilih desa/kelurahan setempat. Sistem secara grafis menampilkan:
  - Jumlah kuota alokasi bansos PKH dan BPNT di kelurahan tersebut.
  - Jumlah anggaran yang telah terealisasi vs anggaran yang tersisa.
  - Grafik distribusi desil kemiskinan warga penerima manfaat.
- **Dampak Kunci:** Mencegah monopoli informasi oleh pamong desa, mempermudah pengawasan anggaran oleh jurnalis lokal, serta memastikan dana tersalurkan 100% tanpa potongan.

### 5.2 Solusi 2: Omnichannel WhatsApp Bot & SMS Gateway 1708 Gratis
- **Konsep:** Meruntuhkan tembok pemisah digital (*digital divide*) yang selama ini menghalangi masyarakat miskin tanpa smartphone dan tanpa paket kuota data.
- **Mekanisme Kerja:**
  - Kemensos membuka saluran resmi WhatsApp Bot terverifikasi (Centang Hijau) dan SMS Gratis 1708.
  - Warga cukup mengetik pesan singkat berformat: `CEK#NIK#NAMA` atau `BANTUAN#NIK`.
  - Server otomatis membalas dengan status kepesertaan bansos dan nama bank penyalur tanpa memungut pulsa sepeser pun.
- **Dampak Kunci:** Menjamin asas aksesibilitas universal bagi kelompok marjinal, lansia sebatang kara, penyandang disabilitas, dan masyarakat kawasan 3T (Tertinggal, Terdepan, Terluar).

### 5.3 Solusi 3: Tracking Tiket Aduan Transparan (SLA 7 Hari Berbasis Notifikasi SMS)
- **Konsep:** Modernisasi alur penanganan keluhan dengan standar *Service Level Agreement* (SLA) terukur yang transparan layaknya nomor resi ekspedisi logistik modern.
- **Mekanisme Kerja:**
  - Setiap pengaduan sengketa bansos atau usul sanggah mendapatkan ID Tiket unik.
  - Setiap ada pergerakan status di tingkat Dinsos atau Bank, sistem otomatis mengirimkan SMS notifikasi: *"Tiket #KM-9821: Berkas Anda sedang diverifikasi Dinas Sosial Kab. Cilacap (Tahap 2 dari 3)"*.
  - Jika usulan ditolak, sistem wajib memberikan alasan spesifik berbasis data objektif (Contoh: *"Ditolak karena NIK terdaftar sebagai pemilik kendaraan roda 4 pada Samsat"*), bukan sekadar penolakan tanpa dasar.
- **Dampak Kunci:** Membangun kepercayaan publik (*public trust*), meniadakan prasangka buruk warga terhadap pemerintah, serta memaksa aparat birokrasi daerah bekerja sesuai tenggat waktu.

### 5.4 Solusi 4: Posko Pendamping Sosial Digital Desa (Jemput Bola)
- **Konsep:** Pendekatan humanis dan proaktif (*outreach proactive*) dengan memperkuat garda terdepan pendamping sosial di tingkat akar rumput.
- **Mekanisme Kerja:**
  - Membekali para pendamping PKH dan Tenaga Kesejahteraan Sosial Kecamatan (TKSK) dengan perangkat tablet khusus yang memiliki kemampuan penyimpanan luring (*offline-sync*).
  - Melakukan patroli jemput bola secara berkala dari pintu ke pintu (*door-to-door*) untuk memvalidasi lansia terlantar, penderita penyakit menahun, dan anak yatim yang belum memiliki identitas kependudukan.
  - Membantu perekaman data kependudukan langsung di tempat bekerja sama dengan Disdukcapil setempat.
- **Dampak Kunci:** Mengeliminasi permasalahan *exclusion error* (orang sangat miskin yang terlewat dari bantuan karena tidak mampu mendaftar sendiri).

---

## BAB VI: PANDUAN DAN SCRIPT PRESENTASI KELOMPOK

Agar presentasi tugas kelompok di hadapan dosen/guru dan rekan mahasiswa berjalan lancar dan berbobot akademis, berikut naskah pembagian peran (*role-play script*) yang dirancang untuk durasi 10–12 menit:

### 6.1 Distribusi Peran Anggota
- **Penyaji 1 (Moderator & Latar Belakang):** Membuka presentasi, menyampaikan urgensi audit kewarganegaraan, profil lembaga Kemensos RI, dan landasan konstitusional UUD 1945 serta UU KIP/Pelayanan Publik (Slide 1 dan 2).
- **Penyaji 2 (Analis Indikator Lapangan):** Memaparkan temuan empiris pada ketiga indikator (Anggaran, Alur Pelayanan Cek Bansos, dan Aduan 171) lengkap dengan bukti pendukung dan matriks komparatif (Slide 3, 4, 5, dan 6).
- **Penyaji 3 (Inovator Solusi & Refleksi Nilai):** Memaparkan infografis 4 rekomendasi strategis, sintesis nilai Sila ke-5 Pancasila, konsep active citizenship, dan menutup sesi presentasi (Slide 7 dan 8).

---

### 6.2 Script Presentasi Lengkap per Slide

#### [Slide 1: Cover] — Penyaji 1
> *"Selamat pagi/siang kepada Bapak/Ibu Dosen pengampu mata kuliah Kewarganegaraan dan rekan-rekan mahasiswa yang kami banggakan. Puji syukur pada hari ini kelompok kami berkesempatan memaparkan hasil tugas praktik kelompok proyek kewarganegaraan kami yang berjudul: **'Audit Sederhana Transparansi Layanan Publik pada Kementerian Sosial Republik Indonesia'**.*  
>  
> *Mengapa kami memilih Kemensos? Karena Kemensos mengelola anggaran perlindungan sosial rata-rata Rp 75 hingga 80 Triliun setiap tahunnya yang bersentuhan langsung dengan hajat hidup warga miskin. Transparansi di Kemensos bukan sekadar urusan teknis administrasi, melainkan cerminan langsung dari keadilan sosial."*

#### [Slide 2: Profil & Metodologi] — Penyaji 1
> *"Pada Slide kedua ini, kami memetakan ruang lingkup pengamatan digital kelompok kami. Kami mengobservasi portal resmi `kemensos.go.id`, portal dokumen keterbukaan informasi `ppid.kemensos.go.id`, serta aplikasi pengecekan mandiri `cekbansos.kemensos.go.id`.*  
>  
> *Landasan hukum penugasan ini berpijak pada amanat Pasal 28F UUD 1945, UU No. 14 Tahun 2008 tentang Keterbukaan Informasi Publik, serta UU No. 25 Tahun 2009 tentang Pelayanan Publik. Kami menggunakan metode digital walkthrough mandiri dan membandingkannya dengan data audit resmi dari BPK RI dan Komisi Informasi Pusat. Selanjutnya, rincian hasil audit 3 indikator akan dijelaskan oleh rekan saya."*

#### [Slide 3: Indikator 1 - Transparansi Anggaran] — Penyaji 2
> *"Terima kasih. Masuk ke Indikator Pertama, yaitu **Transparansi Anggaran**. Pada portal PPID Kemensos, kami mendapati dokumen DIPA tahun 2022 hingga 2024, LAKIP, serta laporan keuangan auditan BPK terunggah secara lengkap dengan predikat WTP. Kemensos juga berhak diapresiasi karena konsisten meraih status Badan Publik Informatif dari KIP.*  
>  
> *Namun catatan kritis kelompok kami: data anggaran masih disajikan dalam format file PDF setebal ratusan halaman yang pasif dan kaku. Belum ada dashboard visual interaktif yang memudahkan warga awam melihat alokasi anggaran hingga tingkat desa, serta belum tersedianya format open-data mentah yang ramah peneliti."*

#### [Slide 4: Indikator 2 - Alur Pelayanan DTKS] — Penyaji 2
> *"Pada Indikator Kedua, yakni **Kemudahan Alur Pelayanan**, kami mengapresiasi inovasi portal `cekbansos.kemensos.go.id` yang memungkinkan siapa saja memeriksa kepesertaan bansos tanpa perlu login atau mendaftar kata sandi, serta hadirnya fitur 'Usul-Sanggah' di aplikasi mobile.*  
>  
> *Tetapi fakta di lapangan menunjukkan adanya jurang kesenjangan digital atau digital divide. Sebagian besar warga miskin ekstrem dan lansia di pelosok tidak memiliki smartphone dan paket data. Selain itu, usulan mandiri warga kerap mandek di birokrasi Musyawarah Desa dan verifikasi Pemda yang berjalan lambat."*

#### [Slide 5: Indikator 3 - Penanganan Keluhan] — Penyaji 2
> *"Pada Indikator Ketiga, **Penanganan Keluhan Warga**, Kemensos menyediakan saluran bebas pulsa Command Center 171 selama 24 jam dan integrasi SP4N-LAPOR!. Respon tanggap darurat Tim Reaksi Cepat (TRC) sangat tanggap terhadap kasus-kasus kedaruratan sosial yang viral.*  
>  
> *Sayangnya, untuk sengketa kartu bansos yang tiba-tiba tidak cair, proses penyelesaiannya memakan waktu lama hingga 30 sampai 60 hari kerja akibat birokrasi kliring perbankan. Warga yang namanya dicoret pun sering tidak memperoleh penjelasan tertulis mengenai alasan objektif di balik pencoretan tersebut."*

#### [Slide 6: Matriks Evaluasi Kritis] — Penyaji 2
> *"Sebagai kesimpulan dari pengamatan empiris ini, kelompok kami menyusun matriks skor: Indikator Anggaran memperoleh nilai 8.5, Kemudahan Pelayanan bernilai 7.8, dan Penanganan Keluhan bernilai 8.0, dengan rata-rata total 8.1 dari 10. Nilai ini menunjukkan kinerja Kemensos sudah tergolong baik, namun memiliki ruang perbaikan besar pada aspek inklusivitas dan kemudahan akses bagi kaum rentan. Bagian rekomendasi solusi akan dipaparkan oleh rekan saya."*

#### [Slide 7: Infografis Rekomendasi Solusi] — Penyaji 3
> *"Terima kasih. Pada Slide ketujuh ini, kami merumuskan **4 Solusi Terintegrasi** dalam bentuk infografis rekomendasi:  
> 1. **Open Budget Web-GIS:** Dashboard anggaran berbasis peta digital agar warga dapat melihat kuota bansos per desa secara transparan;  
> 2. **WhatsApp Bot & SMS Gratis 1708:** Akses multisaluran tanpa internet agar warga miskin tanpa smartphone tetap dapat mengecek status bansos mereka;  
> 3. **Tracking Tiket Keluhan Transparan:** Pelacakan status aduan berstandar SLA 7 hari dengan notifikasi SMS berkala dan transparansi alasan jika usulan ditolak;  
> 4. **Posko Pendamping Sosial Digital Desa:** Aksi jemput bola dengan gawai tablet offline-sync bagi lansia dan disabilitas agar terdaftar dalam DTKS secara akurat."*

#### [Slide 8: Refleksi Pancasila & Penutup] — Penyaji 3
> *"Sebagai penutup pada Slide kedelapan, audit sederhana ini memberikan refleksi mendalam mengenai nilai-nilai Pancasila, khususnya **Sila ke-5: Keadilan Sosial bagi Seluruh Rakyat Indonesia**. Transparansi pelayanan publik adalah hak asasi warga negara dan sarana memastikan tidak ada satu pun orang miskin yang tertinggal (*no one left behind*).*  
>  
> *Sebagai generasi muda, melakukan audit sosial dan mengawal keterbukaan informasi pemerintah adalah bentuk nyata bela negara non-militer dalam bingkai active citizenship. Demikian presentasi dari kelompok kami, kami membuka ruang seluas-luasnya untuk sesi tanya jawab dan masukan. Terima kasih."*

---

### 6.3 Panduan Mengantisipasi Tanya Jawab (Q&A Defense Guide)
Berikut adalah antisipasi pertanyaan kritis yang lazim dilontarkan dosen/guru beserta formula jawabannya:

**Pertanyaan 1: "Mengapa kelompok Anda menilai penyajian anggaran berformat PDF di ppid.kemensos.go.id sebagai suatu kekurangan, padahal secara hukum Kemensos sudah mematuhi UU KIP?"**
> **Jawaban Mahasiswa:**  
> *"Secara kepatuhan formal hukum (*formal compliance*), Kemensos memang sudah memenuhi kewajiban Pasal 9 UU KIP No. 14 Tahun 2008. Namun, dalam perspektif Pelayanan Publik modern (UU No. 25/2009) dan prinsip *Right to Understand*, transparansi sejati bukan hanya sekadar mengunggah dokumen, melainkan memastikan masyarakat selaku pemilik kedaulatan mampu memahami isi data tersebut secara mudah dan tidak membingungkan. Dokumen PDF setebal ratusan halaman justru menciptakan fenomena 'transparansi semu' (*dark transparency*) bagi warga awam. Oleh sebab itu, kami merekomendasikan transisi ke Dashboard Visual Web-GIS."*

**Pertanyaan 2: "Terkait solusi SMS Gratis dan Bot WhatsApp, bukankah Kemensos sudah memiliki aplikasi Cek Bansos di Google Play Store? Mengapa harus membuat SMS lagi yang terkesan kuno?"**
> **Jawaban Mahasiswa:**  
> *"Pendekatan teknologi pelayanan publik harus berpijak pada profil sosiologis penerima manfaat. Berdasarkan data BPS dan Kemensos, penerima bansos terkonsentrasi pada kelompok desil 1 dan 2 (masyarakat termiskin), lansia telantar, dan warga wilayah 3T. Di kelompok ini, angka penetrasi smartphone berspesifikasi tinggi masih terbatas dan kepemilikan paket data internet sangat fluktuatif. SMS dan WhatsApp teks adalah teknologi paling inklusif yang tidak memerlukan bandwidth besar. Kemajuan teknologi seharusnya merangkul semua orang, bukan meninggalkan mereka yang paling rentan."*

**Pertanyaan 3: "Bagaimana kaitan langsung antara audit transparansi Kemensos ini dengan konsep Bela Negara dalam Pendidikan Kewarganegaraan?"**
> **Jawaban Mahasiswa:**  
> *"Dalam konteks kontemporer, ancaman terbesar bangsa bukan semata invasi militer asing, melainkan ketimpangan sosial, kemiskinan ekstrem, dan ketidakpercayaan warga terhadap institusi negara (*cynicism & distrust*). Bela negara diwujudkan melalui partisipasi aktif (*active citizenship*) dengan cara mengawal integritas anggaran sosial negara, mencegah kebocoran dana bantuan rakyat, serta menyumbangkan gagasan inovatif bagi perbaikan tata kelola pemerintahan (*good governance*). Hal ini selaras dengan pengamalan Sila ke-5 Pancasila."*

---

## BAB VII: REFLEKSI KEWARGANEGARAAN & KESIMPULAN

### 7.1 Refleksi Nilai-Nilai Pancasila
Proyek kewarganegaraan ini memberikan pembelajaran mendalam bahwa transparansi tata kelola pemerintahan berakar kuat pada falsafah dasar bangsa Indonesia:
- **Sila Kedua (Kemanusiaan yang Adil dan Beradab):** Menjamin pelayanan publik yang memanusiakan warga miskin, memperlakukan mereka dengan martabat tanpa diskriminasi atau stigma sosial.
- **Sila Keempat (Kerakyatan yang Dipimpin oleh Hikmat Kebijaksanaan dalam Permusyawaratan/Perwakilan):** Membuka ruang partisipasi warga dalam merencanakan, mengawasi, dan menyanggah data bantuan sosial melalui mekanisme rembuk desa dan pelaporan digital yang transparan.
- **Sila Kelima (Keadilan Sosial bagi Seluruh Rakyat Indonesia):** Memastikan bahwa anggaran bansos yang bersumber dari uang rakyat (APBN) benar-benar dinikmati oleh mereka yang paling berhak secara adil, merata, dan tepat sasaran.

### 7.2 Active Citizenship dan Pengawasan Publik
Sebagai warga negara berpendidikan, mahasiswa dan pelajar tidak boleh bersikap apatis terhadap proses penyelenggaraan negara. Mengetahui hak atas informasi (UU KIP), memahami hak atas kepastian layanan (UU Pelayanan Publik), dan berani menyampaikan laporan ketidakberesan melalui kanal resmi merupakan cerminan budaya hukum yang sehat. Demokrasi yang matang mensyaratkan adanya masyarakat sipil (*civil society*) yang kritis, konstruktif, dan berbasis data (*evidence-based advocacy*).

### 7.3 Kesimpulan Akhir
Berdasarkan audit sederhana yang dilakukan terhadap portal Kemensos RI:
1. Kemensos RI telah meletakkan fondasi digital yang progresif melalui keterbukaan dokumen berkala di PPID, portal `cekbansos.kemensos.go.id`, dan layanan Call Center Bebas Pulsa 171.
2. Tantangan terbesar saat ini terletak pada **aksesibilitas kaum marjinal (*digital divide*)**, **kecepatan penyelesaian sengketa kartu bansos**, dan **transparansi alasan pencoretan data penerima**.
3. Empat rekomendasi solusi yang digagas oleh kelompok—yakni Dashboard Open Budget Web-GIS, SMS & WhatsApp Bot Gratis, Tracking Tiket Aduan Real-Time SLA, dan Posko Digital Desa Jemput Bola—dapat menjadi rujukan konstruktif bagi pengambil kebijakan dalam memodernisasi layanan publik di Indonesia.

---

## DAFTAR PUSTAKA & DOKUMEN ACUAN

1. **Republik Indonesia.** (1945). *Undang-Undang Dasar Negara Republik Indonesia Tahun 1945*.
2. **Republik Indonesia.** (2008). *Undang-Undang No. 14 Tahun 2008 tentang Keterbukaan Informasi Publik (KIP)*. Lembaran Negara RI Tahun 2008 No. 61.
3. **Republik Indonesia.** (2009). *Undang-Undang No. 25 Tahun 2009 tentang Pelayanan Publik*. Lembaran Negara RI Tahun 2009 No. 112.
4. **Republik Indonesia.** (2011). *Undang-Undang No. 13 Tahun 2011 tentang Penanganan Fakir Miskin*. Lembaran Negara RI Tahun 2011 No. 83.
5. **Republik Indonesia.** (2022). *Undang-Undang No. 27 Tahun 2022 tentang Pelindungan Data Pribadi (UU PDP)*. Lembaran Negara RI Tahun 2022 No. 196.
6. **Komisi Informasi Pusat (KIP).** (2021). *Peraturan Komisi Informasi No. 1 Tahun 2021 tentang Standar Layanan Informasi Publik*.
7. **Badan Pemeriksa Keuangan (BPK RI).** (2023). *Laporan Hasil Pemeriksaan (LHP) atas Pengelolaan dan Penyaluran Bantuan Sosial pada Kementerian Sosial RI*.
8. **Komisi Pemberantasan Korupsi (KPK RI).** (2023). *Kajian Tata Kelola Penyaluran Bantuan Sosial dan Peningkatan Akurasi DTKS*. Deputi Pencegahan dan Monitoring KPK.
9. **Kementerian Sosial RI.** (2024). *Portal Pejabat Pengelola Informasi dan Dokumentasi (PPID)*. Tersedia pada: `https://ppid.kemensos.go.id` [Diakses November 2026].
10. **Kementerian Sosial RI.** (2024). *Portal Pengecekan Mandiri Bantuan Sosial*. Tersedia pada: `https://cekbansos.kemensos.go.id` [Diakses November 2026].
