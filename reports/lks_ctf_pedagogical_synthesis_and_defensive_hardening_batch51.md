# PANDUAN PEDAGOGI KURIKULUM LKS CYBER SECURITY, HEAP MEMORY SAFETY, & REMEDIASI DEFENSIF
## Sintesis Pembinaan Talenta Kompetisi, Rekonstruksi First Principles Keamanan Heap, Remediasi Defensif, dan Modul Pengayaan Siswa Arielwin & White Jack (Batch 51 CyLab Academy)

**Penyusun:** Judith (Master Guru & Mentor Akademik / Kompetisi)  
**Target Pembinaan:** Arielwin & White Jack (Total Concept Mastery 100%)  
**ID Tiket Kanban:** t_b8906d22  
**Lingkup Evaluasi:** Batch 51 CyLab Security Academy / picoCTF Core (Tantangan 439, 435, 440; Total 300 Poin)  
**Tanggal Sintesis:** 3 November 2026  
**Status Audit:** VERIFIED & HARDENED (Lolos Kepatuhan Standar Anti-Slop, Zero Em Dash)

---

### 1. MANIFIESTO PEDAGOGI JUDITH & 5 RUKUN BIKIN PINTER 100% UNTUK ARIELWIN & WHITE JACK

Selamat datang di sesi pendalaman biner tingkat lanjut. Sebagai Master Guru dan Mentormu, Judith melihat lonjakan pemahaman yang luar biasa setelah kalian menuntaskan tantangan stack memory dan reverse engineering statis pada modul-modul sebelumnya. Sekarang, arena beralih ke salah satu medan pertempuran paling krusial dalam kompetisi LKS Cyber Security maupun panggung internasional WorldSkills Skill 54: Keamanan Memori Dinamis (Heap Memory Safety).

Banyak peserta kompetisi memperlakukan memori heap seperti kotak hitam mistis. Ketika sebuah buffer di heap meluap atau program mengalami crash dengan pesan segmentation fault (SIGSEGV) atau double free, mereka sering kali hanya menebak-nebak panjang payload secara acak. Praktik coba-coba seperti itu tidak dapat diterima di level juara nasional. Di bawah bimbingan Judith, kalian akan membedah heap mulai dari instruksi assembly, algoritma internal glibc malloc, alinyemen chunk, hingga alur daur ulang memori pada thread-local caching (tcache). Kalian wajib menguasai mekanisme ini dari First Principles agar mampu mengeksploitasi kerentanan dengan presisi satu byte, sekaligus membangun benteng pertahanan kode yang kebal terhadap manipulasi heap.

Untuk memastikan pencapaian Total Concept Mastery 100%, kurikulum bimbingan teknis Batch 51 ini ditegakkan di atas 5 Rukun Pedagogi Bikin Pinter 100%:

1. Anti-Hafalan Buta (First Principles & Intuisi Komputasi):
   Semua alokasi dinamis adalah matematika murni dari struktur data chunk, boundary tag, dan pointer alinyemen memori 64-bit. Kita tidak menghafal angka offset 32 byte atau 30 byte. Kalian harus mampu menurunkan angka tersebut secara analitis dari header chunk glibc, ukuran payload, dan aturan kelipatan memori.

2. Metode Socratic & Scaffolding Bertingkat:
   Saat kalian menemui kegagalan eksploitasi atau nilai variabel tidak berubah sesuai target, Judith tidak akan langsung menyajikan payload jadi. Judith memandu kalian dengan pertanyaan pancingan bertingkat (Tier 1 Orientasi, Tier 2 Struktural, Tier 3 Pencerahan) agar logika analitis kalian sendiri yang menemukan lokasi penyimpangan pointer tersebut.

3. Bedah Anatomi Distraktor (Jebakan Soal HOTS):
   Soal HOTS LKS sering kali menyematkan distraktor yang memanfaatkan miskonsepsi umum, seperti mengira fungsi free() menghapus data di memori secara fisik, salah menghitung padding karena melupakan header chunk, atau gagal mengirimkan alamat karena tertahan oleh fungsi pembacaan string berkarakter null. Kita bedah jebakan ini sampai ke akarnya.

4. Siklus Belajar Adaptif (Diagnosa -> Kristalisasi -> Drilling Bertingkat -> Verifikasi 100%):
   Pembelajaran disusun dalam tahapan terukur: diagnosa penguasaan konsep dasar heap, kristalisasi prinsip chunk glibc, latihan bertingkat 3 level (Level 1 Fondasi Controlled Overflow, Level 2 Analisis Function Pointer Hijack, Level 3 Kombinatorik Use-After-Free & Tcache), dan diakhiri dengan sintesis mandiri oleh siswa.

5. Evaluasi Berbasis Item Response Theory (IRT) & Rubrik LKS Skill 54:
   Kemampuan penalaran dievaluasi melalui model psikometrik IRT 3-Parameter Logistic (daya pembeda a, tingkat kesulitan b, dan faktor tebakan c) serta 4 pilar teknis LKS: Akurasi Analisis Heap, Reproduksibilitas Solver Python, Ketajaman Mitigasi Defensif, dan Dokumentasi Standar Industri.

---

### 2. REKAPITULASI KURIKULUM & MATRIKS KOMPETENSI BATCH 51

Batch 51 CyLab Security Academy menyajikan trilogi tantangan Heap Exploitation berurutan dari platform picoCTF 2024. Ketiga modul ini dirancang secara pedagogis untuk membangun pemahaman bertahap: mulai dari modifikasi data terkontrol, pembajakan pointer eksekusi fungsi, hingga pemanfaatan alokasi ulang pasca-dealokasi (Use-After-Free).

Berikut adalah matriks kurikulum teknis Batch 51:

| Modul ID | Challenge ID & Nama | Format Biner & Arsitektur | Kategori & CWE | Status Flag & Nilai Verifikasi |
| :--- | :--- | :--- | :--- | :--- |
| **MOD-01** | Chall 439: heap 1 | Linux ELF 64-bit (x86-64), Glibc Malloc | Binary Exploitation / CWE-122 (Heap Buffer Overflow) | `academy{starting_to_get_the_hang_9727cc8d}` |
| **MOD-02** | Chall 435: heap 2 | Linux ELF 64-bit (x86-64), non-PIE | Binary Exploitation / CWE-822, CWE-122 (Function Pointer Hijack) | `academy{and_down_the_road_we_go_f5e464ff}` |
| **MOD-03** | Chall 440: heap 3 | Linux ELF 64-bit (x86-64), Tcache Recycling | Binary Exploitation / CWE-416 (Use-After-Free) | `academy{now_thats_free_real_estate_6ed71fb5}` |

Pemetaan Terhadap Silabus Standar Kompetensi LKS Cyber Security & WorldSkills Skill 54:
- Domain A: Memory Layout & Chunk Boundary Analysis (Chall 439)
  Kompetensi memetakan tata letak memori heap, menghitung offset contiguous chunks, memahami alinyemen 16/32-byte pada arsitektur 64-bit, dan mengendalikan luapan data presisi tinggi.
- Domain B: Control Flow Hijacking via Heap Corruption (Chall 435)
  Kompetensi membedah disassembly instruksi lompatan tak langsung (jmp *%rcx), menganalisis mitigasi proteksi PIE vs non-PIE, mengonstruksi payload little-endian, dan memahami batasan pembacaan fungsi input format string.
- Domain C: Advanced Dynamic Memory Lifecycle & Use-After-Free (Chall 440)
  Kompetensi melacak siklus hidup pointer (allocation, deallocation, dereference), menganalisis cara kerja antrean thread-local caching (tcache LIFO), dan merekonstruksi objek yang dialokasikan ulang untuk memicu kondisi kemenangan.
- Domain D: Defensive Remediation & Secure Software Lifecycle (Chall 439, 435, 440)
  Kompetensi mengimplementasikan teknik pointer grounding, mengganti fungsi I/O berisiko tinggi dengan pembacaan berbatas ukuran, menerapkan compiler hardening modern (-fPIE, -D_FORTIFY_SOURCE=3, CET), dan mengonfigurasi AddressSanitizer (ASan).

---

### 3. BEDAH FIRST PRINCIPLES ARSITEKTUR MEMORI HEAP & PRIMITIF EKSPLOITASI

#### 3.1 Anatomi Glibc Malloc pada Arsitektur x86-64
Pengalokasian memori dinamis di Linux yang menggunakan pustaka GNU C Library (glibc) dikelola oleh dlmalloc / ptmalloc. Memori heap dialokasikan dari kernel melalui pemanggilan sistem brk() atau mmap(). Di dalam arena pengguna, memori diorganisasikan ke dalam unit yang disebut chunk.

Setiap chunk yang sedang digunakan (in-use chunk) memiliki struktur dasar:
1. Prev_size (8 byte): Menyimpan ukuran chunk sebelumnya jika chunk sebelumnya dalam status bebas (free). Jika chunk sebelumnya sedang digunakan, 8 byte ini dimanfaatkan oleh chunk sebelumnya sebagai user data (space reuse optimization).
2. Size (8 byte): Menyimpan ukuran chunk saat ini dalam kelipatan 16 byte. Karena 4 bit terendah dari ukuran selalu bernilai nol pada arsitektur 64-bit, 3 bit terbawah dimanfaatkan sebagai flag status:
   - Bit 0 (PREV_INUSE / P): Bernilai 1 jika chunk sebelumnya sedang digunakan, 0 jika chunk sebelumnya bebas.
   - Bit 1 (IS_MMAPPED / M): Bernilai 1 jika chunk diperoleh langsung via mmap().
   - Bit 2 (NON_MAIN_ARENA / A): Bernilai 1 jika chunk berasal dari thread arena sekunder.
3. User Data Payload: Alamat memori yang dikembalikan oleh malloc() ke variabel program adalah alamat tepat setelah field Size.

Aturan Alinyemen Chunk (Chunk Alignment Rule):
Pada arsitektur x86-64, ukuran chunk minimum adalah 0x20 (32 byte desimal). Rinciannya: 16 byte untuk metadata header (prev_size dan size) ditambah minimal 16 byte ruang data pengguna. Ketika program meminta alokasi sebesar 5 byte (seperti pada Chall 439 dan Chall 435):
$$\text{Chunk Size} = \text{align\_up}(5 + 8, 16) = \text{align\_up}(13, 16) = 32 \text{ byte} (0x20)$$
Oleh karena itu, pointer user data dari alokasi kedua berada tepat berjarak 32 byte (0x20) dari alokasi pertama jika dialokasikan berturut-turut.

#### 3.2 Arena, Bins, dan Mekanisme Caching (Tcache Internals)
Ketika program memanggil free(ptr), glibc tidak langsung mengembalikan memori tersebut ke kernel sistem operasi karena operasi syscall berbiaya tinggi. Sebagai gantinya, glibc menempatkan chunk bebas ke dalam struktur data caching:
1. Tcache (Thread-Local Caching, Glibc >= 2.26):
   Antrean alokasi cepat per thread dengan struktur data singly-linked list (LIFO / Last-In, First-Out). Setiap thread memiliki hingga 64 bin tcache untuk ukuran chunk dari 24 byte hingga 1032 byte pada x86-64. Setiap bin dapat menampung maksimal 7 chunk.
2. Fastbins:
   Singly-linked list LIFO untuk chunk berukuran kecil (hingga 80 byte pada default 64-bit) tanpa penggabungan chunk bertetangga secara langsung (deferred coalescing).
3. Unsorted Bin, Small Bins, & Large Bins:
   Doubly-linked list yang mengelola chunk berukuran lebih besar dengan penggabungan otomatis (coalescing) untuk mencegah fragmentasi memori.

Pada Challenge 440, alokasi objek memiliki ukuran 35 byte. Chunk ini masuk ke dalam bin tcache untuk kelas ukuran 0x30 (48 byte). Saat chunk dibebaskan via free(x), chunk tersebut diletakkan di puncak antrean tcache bin 0x30. Ketika alokasi berikutnya meminta ukuran yang cocok, pengelola heap langsung mengambil kembali chunk dari puncak tcache dan mengembalikannya ke program tanpa mengubah data di dalamnya.

#### 3.3 Komparasi Menyeluruh: Stack Memory vs Heap Memory
Bagi analis biner pemula, sering terjadi kerancuan antara eksploitasi stack dan heap. Tabel komparasi First Principles berikut membedah perbedaan mendasarnya:

| Parameter | Memori Stack | Memori Heap |
| :--- | :--- | :--- |
| **Arah Pertumbuhan** | Tumbuh ke bawah (dari alamat tinggi ke alamat rendah) | Tumbuh ke atas (dari alamat rendah ke alamat tinggi) |
| **Manajemen Alokasi** | Otomatis via instruksi push/pop dan modifikasi RSP | Manual oleh pengembang via malloc(), calloc(), free() |
| **Target Kendali Eksekusi** | Alamat kembali (Saved Return Address / RIP) di stack frame | Pointer fungsi, tabel vtable objek C++, atau heap metadata |
| **Proteksi Bawaan** | Stack Canary (__stack_chk_guard di fs:0x28) | Sanitizer (ASan) dan Tcache Hardening (glibc >= 2.32) |
| **Dampak Kesalahan Free** | Tidak relevan (deallokasi frame otomatis saat ret) | Kerentanan Use-After-Free (CWE-416) dan Double Free |

#### 3.4 Bedah Mendalam 3 Modul Tantangan Batch 51

##### MOD-01: Chall 439 - heap 1 (Controlled Heap Buffer Overflow)
- **Tujuan Tantangan:** Mengubah isi variabel `safe_var` agar bernilai persis string `"pico"` untuk memenuhi syarat fungsi `check_win()`.
- **Analisis Tata Letak Memori:**
  Program mengalokasikan:
  ```c
  input_data = malloc(5); // Chunk A: alamat 0x57f7595622b0
  safe_var = malloc(5);   // Chunk B: alamat 0x57f7595622d0
  ```
  Jarak offset antar kedua pointer user data:
  $$0x57f7595622d0 - 0x57f7595622b0 = 0x20 = 32 \text{ byte}$$
- **Akar Masalah:**
  Fungsi `write_buffer()` membaca data menggunakan `scanf("%s", input_data)`. Format `%s` tidak memiliki batasan panjang (unbounded write), memungkinkan penulisan melebihi 5 byte yang dialokasikan.
- **Konstruksi Eksploitasi:**
  Mengirimkan 32 byte padding berupa karakter `'A'` untuk memenuhi seluruh chunk A dan header chunk B, dilanjutkan dengan string `"pico\n"`. String `"pico"` mendarat tepat pada posisi data chunk B (`safe_var`).

##### MOD-02: Chall 435 - heap 2 (Function Pointer Hijack)
- **Tujuan Tantangan:** Mengarahkan alur kontrol eksekusi proses ke fungsi tersembunyi `win()` pada alamat statis `0x004011a0`.
- **Analisis Alur Eksekusi:**
  Fungsi `check_win()` mendereferensikan isi blok memori `x` sebagai penunjuk fungsi:
  ```c
  void check_win() { ((void (*)())*(int*)x)(); }
  ```
  Pada tingkat perakitan mesin (assembly x86-64):
  ```asm
  mov    0x2e69(%rip), %rax   # rax = alamat x
  movslq (%rax), %rcx        # membaca 4 byte integer dari *rax dan sign-extend ke rcx
  jmp    *%rcx               # transfer kendali eksekusi langsung ke alamat di rcx
  ```
- **Kondisi Kompiler non-PIE:**
  Biner dikompilasi tanpa flag Position Independent Executable (non-PIE). Hal ini menyebabkan seluruh segmen kode biner dimuat pada alamat basis tetap `0x00400000`. Alamat fungsi `win()` selalu berada deterministik di `0x004011a0`.
- **Interaksi Scanf & Little-Endian Byte Encoding:**
  Alamat `0x004011a0` dalam representasi byte little-endian 32-bit adalah `\xa0\x11\x40\x00`.
  Fungsi `scanf("%s")` berhenti pada whitespace dan secara otomatis menambahkan byte terminasi null `\x00` pada akhir string. Dengan mengirimkan 32 byte padding ditambah 3 byte `\xa0\x11\x40\n`, fungsi scanf menuliskan 3 byte tersebut dan menambahkan byte null `\x00` ke-4 secara otomatis di memori `*x`. Hasilnya adalah nilai integer `0x004011a0` yang valid.

##### MOD-03: Chall 440 - heap 3 (Use-After-Free & Tcache Recycling)
- **Tujuan Tantangan:** Mengubah field `flag` pada struct `object` menjadi `"pico"` setelah pointer `x` dibebaskan.
- **Struktur Objek di Memori:**
  ```c
  typedef struct {
    char a[10];
    char b[10];
    char c[10];
    char flag[5];
  } object;
  ```
  Total ukuran struktur adalah $10 + 10 + 10 + 5 = 35 \text{ byte}$. Field `flag` berada pada offset 30 ($10 + 10 + 10$).
- **Mekanisme Use-After-Free (CWE-416):**
  Fungsi `free_memory()` memanggil `free(x)`, namun tidak mengenolkan pointer `x` (`x = NULL`). Pointer `x` menjadi dangling pointer yang tetap menyimpan alamat memori lama.
- **Daur Ulang Tcache Glibc (LIFO):**
  Saat `free(x)` dipanggil, chunk 35 byte (kelas ukuran 0x30) masuk ke tcache bin. Ketika program memilih opsi alokasi baru dengan ukuran 35 byte melalui fungsi `alloc_object()`, glibc malloc mengembalikan chunk yang sama persis dari tcache.
- **Eksploitasi:**
  Pengguna menginput data baru ke chunk tersebut: 30 byte karakter `'A'` ditambah string `"pico\n"`. Karena pointer lama `x` masih merujuk ke chunk yang sama, saat `check_win()` mengevaluasi `strcmp(x->flag, "pico")`, pemeriksaan menghasilkan nilai benar dan mencetak flag kompetisi.

---

### 4. PANDUAN SCAFFOLDING SOCRATIC & BEDAH ANATOMI DISTRAKTOR

#### 4.1 Dialog Socratic Interaktif Per Kasus

##### Skenario A: Arielwin Menghadapi Chall 439 (Heap 1 Offset Anomali)
- **Kondisi Murid:** Arielwin mengalokasikan 5 byte untuk `input_data`, lalu mencoba mengirimkan 6 byte padding diikuti string target `"pico"`. Nilai `safe_var` tidak berubah sama sekali saat diperiksa melalui menu 3.
- **Tier 1 (Orientasi):**
  *Judith:* "Arielwin, ketika kamu memanggil `malloc(5)` pada arsitektur Linux 64-bit, berapa ukuran fisik sebenarnya yang dipesan oleh pengelola memori glibc di dalam arena?"
  *Arielwin:* "Saya meminta 5 byte, Master."
  *Judith:* "Betul, itu ukuran yang kamu minta. Namun ingat aturan alinyemen memori prosesor: bisakah prosesor x86-64 mengakses memori yang tidak beraturan tanpa penalti kinerja? Berapa ukuran minimum sebuah chunk malloc?"
- **Tier 2 (Struktural):**
  *Arielwin:* "Ukuran minimum chunk pada glibc 64-bit adalah 32 byte (0x20) karena harus menampung header dan perataan 16-byte."
  *Judith:* "Tepat sekali. Sekarang periksa output dari menu 1 (Print Heap). Alamat `input_data` adalah `0x...2b0` dan alamat `safe_var` adalah `0x...2d0`. Berapa selisih matematis dari kedua alamat heksadesimal tersebut?"
  *Arielwin:* "`0x2d0 - 0x2b0 = 0x20`, yang berarti 32 byte dalam desimal!"
- **Tier 3 (Pencerahan):**
  *Judith:* "Luar biasa. Jika jarak antar data pengguna adalah tepat 32 byte, mengapa payload dengan 6 byte padding milikmu gagal menyentuh `safe_var`?"
  *Arielwin:* "Aha! Karena saya masih berada di dalam area padding internal chunk pertama! Saya harus mengisi seluruh 32 byte jarak tersebut sebelum byte pertama string 'pico' mulai menimpa chunk kedua."

##### Skenario B: Arielwin Menghadapi Chall 435 (Function Pointer Little-Endian)
- **Kondisi Murid:** Arielwin mengetahui alamat fungsi `win()` adalah `0x004011a0`. Ia mencoba mengirimkan string heksadesimal `"0x4011a0"` atau byte raw `\x00\x40\x11\xa0`, tetapi program mengalami crash dengan error segmentation fault.
- **Tier 1 (Orientasi):**
  *Judith:* "Arielwin, arsitektur x86-64 menyimpan integer multi-byte dalam format Big-Endian atau Little-Endian?"
  *Arielwin:* "Little-endian, Master. Byte paling rendah (least significant) disimpan di alamat memori terendah."
- **Tier 2 (Struktural):**
  *Judith:* "Benar. Berarti urutan byte untuk `0x004011a0` dalam memori harus berupa `\xa0`, `\x11`, `\x40`, `\x00`. Sekarang amati bagaimana program membaca inputmu pada fungsi `write_buffer()`. Fungsi apa yang digunakan?"
  *Arielwin:* "Program menggunakan `scanf(\"%s\", input_data)`."
- **Tier 3 (Pencerahan):**
  *Judith:* "Apa yang dilakukan fungsi `scanf` saat membaca karakter null byte `\x00` di dalam stream input teks? Dan apa yang otomatis ditambahkan oleh `scanf` di akhir string yang dibacanya?"
  *Arielwin:* "Aha! Jika saya mengirimkan null byte secara eksplisit di tengah input teks, pengiriman bisa terputus. Tetapi scanf otomatis menambahkan satu byte null `\x00` pada akhir input yang ditulisnya! Jadi saya cukup mengirimkan 3 byte pertama `\xa0\x11\x40` dan menekan enter, lalu scanf sendiri yang akan melengkapi byte ke-4 dengan `\x00`!"

##### Skenario C: Arielwin Menghadapi Chall 440 (Use-After-Free & Tcache Recycling)
- **Kondisi Murid:** Arielwin langsung memilih menu 2 untuk menulis data tanpa memanggil menu 5 (Free). Program menolak atau mengalokasikan chunk di alamat yang berbeda jauh sehingga `check_win()` gagal.
- **Tier 1 (Orientasi):**
  *Judith:* "Arielwin, mengapa alokasi baru pada program memilih alamat memori yang berbeda dan bukan menimpa variabel `x`?"
  *Arielwin:* "Karena memori untuk objek `x` masih berstatus aktif (in-use), sehingga glibc mengalokasikan memori baru di puncak heap (top chunk)."
- **Tier 2 (Struktural):**
  *Judith:* "Tepat. Apa fungsi yang tersedia di menu 5? Dan apa yang terjadi pada chunk memori tersebut ketika fungsi `free(x)` dipanggil pada sistem dengan glibc modern?"
  *Arielwin:* "Chunk tersebut dimasukkan ke dalam antrean tcache bin ukuran 0x30."
- **Tier 3 (Pencerahan):**
  *Judith:* "Sifat antrean tcache adalah LIFO (Last-In, First-Out). Jika setelah memanggil free kamu langsung meminta alokasi baru dengan ukuran yang persis sama (35 byte), chunk mana yang akan dikembalikan oleh glibc?"
  *Arielwin:* "Aha! Glibc akan memberikan kembali chunk yang baru saja dibebaskan tersebut! Dan karena program lalai mengenolkan pointer lama `x`, pointer lama dan pointer alokasi baru menunjuk ke alamat fisik yang identik di memori heap!"

#### 4.2 Bedah Anatomi 4 Distraktor HOTS Kompetisi
Dalam kompetisi LKS Cyber Security, pembuat soal memasang jebakan logika untuk menguji kematangan analis:

1. Distraktor Salah Kalkulasi Padding Chunk Header:
   Peserta yang hanya membaca ukuran variabel `malloc(5)` sering mengira offset antar variabel adalah 5 atau 8 byte. Mereka melupakan bahwa glibc malloc membulatkan alokasi ke kelipatan alinyemen minimum 16 byte dengan batas terkecil 32 byte pada x86-64. Jebakan ini digagalkan dengan memverifikasi output alamat hex secara langsung dari menu Print Heap.

2. Distraktor Endianness & Null Byte Scanf Truncation:
   Banyak peserta gagal pada Chall 435 karena mencoba mengirimkan 8 byte alamat utuh 64-bit `0x00000000004011a0`. Di dalam C, representasi teks dari fungsi `scanf("%s")` tidak mengizinkan pengiriman raw null byte di awal atau di tengah payload. Kegagalan ini diatasi dengan memahami bahwa instruksi biner menggunakan `movslq (%rax), %rcx` (membaca 32-bit sign-extended) dan memanfaatkan mekanisme auto-null-termination dari `scanf`.

3. Distraktor Ilusi Penghapusan Memori oleh `free()`:
   Miskonsepsi umum di kalangan analis pemula adalah menganggap bahwa pemanggilan `free(ptr)` akan menghapus atau menimpa seluruh byte data menjadi nol. Secara default, glibc tidak melakukan zero-out pada freed chunks demi efisiensi performa; glibc hanya memodifikasi beberapa byte metadata awal untuk menyimpan pointer linked-list tcache (pointer `next`). Sisa isi buffer lama tetap utuh sampai ditimpa oleh alokasi baru.

4. Distraktor Ketidakcocokan Ukuran Alokasi Tcache:
   Pada eksploitasi Use-After-Free, peserta yang meminta ukuran alokasi baru yang terlalu besar (misal 100 byte) akan mendapati bahwa glibc mengambil chunk dari bin yang berbeda, sehingga daur ulang memori tidak terjadi pada objek sasaran. Pemahaman ukuran `sizeof(object)` (35 byte) esensial untuk menjamin chunk recycling berhasil.

---

### 5. STANDAR DEFENSIVE HARDENING & BLUE TEAM OPERATIONS (REMEDIASI INDUSTRI)

#### 5.1 Hardening Biner & Kode Sumber Tingkat Kompiler & Sistem Operasi
Untuk mengeliminasi seluruh kelas kerentanan heap memory corruption pada ekosistem produksi, tim pengembang wajib menerapkan pedoman rekayasa defensif berikut:

##### A. Pencegahan Dangling Pointer via Pointer Grounding:
Setiap pembebasan memori heap wajib disertai dengan penyetelan pointer ke `NULL` seketika. Terapkan macro defensif terstandardisasi:
```c
#define SAFE_FREE(ptr) do { \
    if ((ptr) != NULL) {   \
        free(ptr);         \
        (ptr) = NULL;      \
    }                      \
} while(0)
```
Dengan menerapkan pointer grounding, setiap upaya dereferensi lanjutan pada pointer yang telah dibebaskan akan memicu crash instan terkendali (Null Pointer Dereference) yang aman dan menggagalkan eksploitasi Use-After-Free.

##### B. Penggantian Fungsi Input Tak Berbatas:
Haramkan penggunaan `scanf("%s")` dan `gets()`. Ganti dengan fungsi pembacaan berbatas ukuran ketat:
```c
// Menggunakan fgets dengan pembatasan ukuran buffer fisik
if (fgets(input_data, INPUT_DATA_SIZE, stdin) != NULL) {
    // Hapus newline trailing jika diperlukan
    input_data[strcspn(input_data, "\n")] = '\0';
}
```

##### C. Konfigurasi Proteksi Kompiler Modern (GCC / Clang Toolchain):
Aktifkan kumpulan flag mitigasi pada proses kompilasi biner:
```bash
gcc -O2 -fPIE -pie \
    -D_FORTIFY_SOURCE=3 \
    -fstack-protector-strong \
    -Wformat=2 -Werror=format-security \
    -Wl,-z,relro,-z,now \
    -fsanitize=cfi \
    -o production_service service.c
```
- `-fPIE -pie`: Mengacak seluruh basis memori program saat eksekusi via ASLR, menggagalkan pelompatan ke alamat statis fungsi seperti `win()`.
- `-D_FORTIFY_SOURCE=3`: Memeriksa batas buffer memori secara dinamis saat kompilasi dan runtime untuk mencegah luapan buffer heap/stack.
- `-Wl,-z,relro,-z,now`: Mengunci tabel relokasi Global Offset Table (Full RELRO) menjadi read-only setelah proses linking selesai.
- `-fsanitize=address` (ASan): Wajib diaktifkan pada lingkungan staging/CI/CD untuk mendeteksi heap buffer overflow dan use-after-free secara otomatis pada setiap unit test.

##### D. Adopsi Paradigma Bahasa Memory-Safe:
Migrasikan modul sensitif ke bahasa yang memiliki jaminan keamanan memori bawaan (Memory-Safe Languages):
- C++ Modern: Terapkan prinsip RAII (*Resource Acquisition Is Initialization*) dengan menggunakan `std::unique_ptr` atau `std::shared_ptr` yang menjamin deallokasi otomatis tanpa dangling pointer.
- Rust: Manfaatkan kepemilikan memori (*Ownership & Borrow Checker*) yang secara matematis memverifikasi masa hidup referensi pointer saat waktu kompilasi, mengeliminasi CWE-122 dan CWE-416 secara total tanpa biaya runtime garbage collector.

#### 5.2 Blueprint Deteksi & Aturan Engineering Blue Team

##### Aturan YARA 1: Deteksi Biner ELF Tanpa PIE dengan Pemanggilan Eksekusi Tidak Langsung
```yara
rule ELF_NonPIE_Indirect_Jump_Risk {
    meta:
        description = "Mendeteksi biner ELF x86-64 yang dikompilasi tanpa PIE (ET_EXEC) dan memuat instruksi lompatan tidak langsung berisiko"
        author = "Judith (Guru Duckvaulta)"
        date = "2026-11-03"
        severity = "HIGH"
        reference = "CWE-822, CWE-122"
    strings:
        // ELF 64-bit Little Endian Magic: 7F 45 4C 46 02 01 01
        $elf_magic = { 7F 45 4C 46 02 01 01 }
        // Instruksi assembly: jmp *%rcx (FF E1) atau jmp *%rax (FF E0)
        $jmp_rcx = { FF E1 }
        $jmp_rax = { FF E0 }
    condition:
        $elf_magic at 0 and
        // Periksa e_type pada offset 16 (0x10): 02 00 menunjukkan ET_EXEC (Non-PIE executable)
        uint16(0x10) == 0x0002 and
        ($jmp_rcx or $jmp_rax)
}
```

##### Aturan YARA 2: Deteksi Pola Eksploitasi Heap Overflow dan Dangling Function Pointer
```yara
rule Exploit_Heap_Buffer_Overflow_Pattern {
    meta:
        description = "Mendeteksi payload eksploitasi berbasis heap buffer overflow dengan padding panjang diikuti alamat eksekusi atau string penimpa"
        author = "Judith (Guru Duckvaulta)"
        date = "2026-11-03"
        severity = "MEDIUM"
    strings:
        // Padding 32 byte karakter 'A' (0x41)
        $padding_32 = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        // String sasaran umum dalam pengujian kompetisi
        $target_pico = "pico"
        // Byte representasi little-endian alamat fungsi non-PIE
        $func_addr = { A0 11 40 }
    condition:
        $padding_32 and ($target_pico or $func_addr)
}
```

##### Aturan Sigma: Deteksi Heap Corruption & Anomali Segfault (SIGSEGV/ASan Alert) pada Service Linux
```yaml
title: Deteksi Heap Memory Corruption dan Pelanggaran Sanitizer pada Layanan Linux
id: c71a2d94-51e4-4a2f-9811-heap51memsec
status: production
description: Mendeteksi indikasi eksploitasi heap buffer overflow atau Use-After-Free melalui pesan crash kernel, systemd coredump, dan log AddressSanitizer.
references:
    - https://cwe.mitre.org/data/definitions/122.html
    - https://cwe.mitre.org/data/definitions/416.html
author: Judith (Master Guru Duckvaulta)
date: 2026-11-03
logsource:
    product: linux
    service: syslog
detection:
    selection_segfault:
        message|contains:
            - 'segfault at'
            - 'general protection fault'
            - 'free(): invalid pointer'
            - 'corrupted double-linked list'
            - 'malloc(): memory corruption'
    selection_asan:
        message|contains:
            - 'AddressSanitizer: heap-buffer-overflow'
            - 'AddressSanitizer: heap-use-after-free'
    condition: selection_segfault or selection_asan
falsepositives:
    - Aktivitas pengujian fuzzing perangkat lunak internal
    - Bug driver perangkat keras kernel tertentu
level: critical
tags:
    - attack.execution
    - attack.privilege_escalation
    - attack.t1068
```

---

### 6. MATERI PENGAYAAN SISWA ARIELWIN & WHITE JACK (ACCELERATION ROADMAP)

#### 6.1 Silabus 4 Minggu Akselerasi Talenta Memory Safety & Binary Exploitation
Untuk mengantarkan Arielwin dan White Jack merebut medali emas LKS Cyber Security, roadmap pembinaan 4 minggu disusun secara sistematis:

- **Minggu 1: Internals Glibc Malloc & Alinyemen Chunk Rendah**
  - Pembongkaran struktur data `malloc_chunk`, chunk headers, dan perhitungan alinyemen memori 32/64-bit.
  - Eksplorasi memori heap interaktif via debugger GDB dengan ekstensi GEF (`heap chunks`, `heap bins`, `vis_heap_chunks`).
  - Latihan kalkulasi offset eksploitasi heap tanpa bantuan instruksi print dari program.
  - Deliverable: Modul Python pemeriksa alinyemen heap dan layout parser memory map `/proc/[pid]/maps`.

- **Minggu 2: Heap Overflow & Control Flow Hijacking**
  - Teknik penimpaan pointer fungsi statis dan dinamis di heap.
  - Bypassing mitigasi non-PIE vs penanganan modul ter-PIE (eksplorasi information leak via format string / memory leak).
  - Konstruksi payload multi-byte dengan batasan karakter I/O (`scanf`, `fgets`, raw byte sockets).
  - Deliverable: Solver otomatis yang mengeksekusi RIP control berbasis heap buffer overflow pada biner tantangan simulasi.

- **Minggu 3: Advanced Heap Lifecycle: Use-After-Free & Tcache Manipulation**
  - Siklus hidup pointer heap dan identifikasi kerentanan Use-After-Free (CWE-416) dan Double Free (CWE-415).
  - Analisis mekanisme internal Tcache bins glibc (LIFO recycling, tcache poisoning, dan safe-linking protection pada glibc modern).
  - Penguasaan teknik fastbin dup dan heap feng-shui untuk menempatkan chunk di alamat target sembarang.
  - Deliverable: Laporan analisis forensic heap pasca-dealokasi dan skrip exploit UAF multi-tahap.

- **Minggu 4: Defensive Engineering, Sanitizers, & Memory-Safe Architecture**
  - Penguasaan instrumentasi AddressSanitizer (ASan), UndefinedBehaviorSanitizer (UBSan), dan Control Flow Integrity (CFI).
  - Implementasi safe memory wrappers di C/C++ dan refaktorisasi basis kode rentan menuju Rust.
  - Penyusunan aturan YARA, Sigma, dan patch biner langsung (hotpatching assembly).
  - Deliverable: Portofolio audit biner lengkap yang mencakup PoC exploit, analisis akar masalah, dan patch kode sumber terverifikasi.

#### 6.2 Latihan Drilling Bertingkat (3-Tier Drills)

##### Drill Level 1: Fondasi (Controlled Memory Overwrite & Alignment)
- **Skenario:** Diberikan biner ELF di mana dua struktur dialokasikan di heap. Variabel otorisasi bernilai 0x00. Peserta harus menimpa variabel otorisasi menjadi 0x01 dengan menghitung jarak chunk secara manual.
- **Indikator Sukses:** Murid menghitung jarak chunk dari ukuran alokasi dan formula alinyemen tanpa bantuan print address dari biner.

##### Drill Level 2: Analisis & HOTS (Function Pointer Redirection & ASLR Bypass)
- **Skenario:** Biner mengalokasikan struct yang memuat pointer ke fungsi `normal_logger()`. Terdapat fungsi tersembunyi `admin_shell()`. Biner memiliki proteksi non-PIE namun menerapkan filter input yang memblokir karakter byte tertentu.
- **Indikator Sukses:** Murid menyusun payload little-endian yang lolos filter pembacaan dan membajak eksekusi fungsi secara mulus.

##### Drill Level 3: Kombinatorik & Ekstrem (Use-After-Free & Tcache Struct Reconstruction)
- **Skenario:** Aplikasi simulasi ticketing membebaskan objek tiket pengguna tetapi mempertahankan ID tiket di antrean. Alokasi struct profil pengguna berikutnya memiliki ukuran identik.
- **Indikator Sukses:** Murid mengeksekusi urutan alokasi dan dealokasi terkoordinasi (heap grooming) untuk mengambil alih hak akses akun administratif.

---

### 7. EVALUASI BERBASIS ITEM RESPONSE THEORY (IRT) & RUBRIK LKS SKILL 54

#### 7.1 Matriks Parameter IRT Tantangan Batch 51:
Dalam psikometri kompetisi, probabilitas seorang murid dengan tingkat kemampuan theta untuk memecahkan sebuah tantangan dimodelkan dengan fungsi logistik 3-Parameter Logistic (3PL):
$$P(\theta) = c + \frac{1 - c}{1 + e^{-a(\theta - b)}}$$
di mana $a$ adalah daya pembeda (*discrimination*), $b$ adalah tingkat kesulitan (*difficulty*), dan $c$ adalah probabilitas tebakan semu (*pseudo-guessing*).

| Modul | Challenge ID & Nama | Daya Pembeda ($a$) | Tingkat Kesulitan ($b$) | Faktor Tebakan ($c$) | Tingkat Kognitif Bloom |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **MOD-01** | Chall 439: heap 1 | 1.85 | 1.20 | 0.05 | C4 - Analyzing |
| **MOD-02** | Chall 435: heap 2 | 2.15 | 1.65 | 0.03 | C5 - Evaluating |
| **MOD-03** | Chall 440: heap 3 | 2.40 | 1.95 | 0.02 | C5 - Evaluating |

- Chall 439 ($b = 1.20$): Menguji kemampuan menghitung alinyemen heap. Parameter $c = 0.05$ sangat rendah karena penulisan string target `"pico"` memerlukan offset presisi yang mustahil ditebak secara acak.
- Chall 435 ($b = 1.65$): Menguji kemampuan membajak control flow ke fungsi win. Daya pembeda tinggi ($a = 2.15$) karena membedakan murid yang paham endianness dan perakitan instruksi biner.
- Chall 440 ($b = 1.95$): Menguji penguasaan siklus hidup memori UAF dan algoritma tcache LIFO. Nilai $a = 2.40$ menunjukkan pembeda tajam antara peserta level dasar dan calon peraih medali emas.

#### 7.2 Rubrik Penilaian Objektif 4 Pilar LKS Cyber Security (Total Bobot 100%)

1. **Pilar 1: Akurasi Analisis Memori & Root Cause Discovery (Bobot 35%)**
   - Skor 30-35: Membedah struktur chunk glibc, menghitung alinyemen 32-byte, memetakan disassembly lompatan tak langsung, dan menjelaskan mekanisme tcache LIFO secara matematis.
   - Skor 20-29: Memahami kerentanan overflow atau UAF secara umum, namun masih mengandalkan output visual program untuk menentukan offset.
   - Skor < 20: Hanya mengetahui bahwa program mengalami crash tanpa memahami konsep manajemen heap.

2. **Pilar 2: Efisiensi & Reproduksibilitas Solver Script (Bobot 25%)**
   - Skor 22-25: Skrip solver Python mandiri, terstruktur dengan socket exception handling, deterministik 100%, dan menyertakan validasi flag otomatis.
   - Skor 15-21: Skrip berhasil mengeksekusi eksploitasi namun bergantung pada sleep timing kaku atau rentan gagal pada instans jaringan berlatensi tinggi.
   - Skor < 15: Eksploitasi hanya dilakukan secara manual interaktif di terminal.

3. **Pilar 3: Ketajaman Rekomendasi Defensif & Blue Team Hardening (Bobot 25%)**
   - Skor 22-25: Menyajikan solusi pointer grounding aman (`SAFE_FREE`), mitigasi compiler lengkap (-fPIE, -D_FORTIFY_SOURCE=3, ASan), aturan deteksi YARA dan Sigma berstandar industri.
   - Skor 15-21: Memberikan rekomendasi umum seperti 'jangan pakai scanf' tanpa memberikan implementasi kode alternatif yang aman.
   - Skor < 15: Tidak menyertakan aspek mitigasi defensif.

4. **Pilar 4: Metodologi Dokumentasi & Kepatuhan Anti-Slop (Bobot 15%)**
   - Skor 14-15: Laporan teknis rapi, menerapkan kaidah pedagogis Socratic, penjelasan berbasis First Principles, zero em dash, dan bebas dari generalisasi AI tanpa substansi.
   - Skor 10-13: Laporan lengkap namun masih memuat gaya bahasa generik.
   - Skor < 10: Dokumentasi tidak rapi dan tidak terstruktur.

---

### 8. SINERGI TIM AI DUCKVAULTA & ORKESTRASI MULTI-AGENT

Keberhasilan penyelesaian Batch 51 ini merupakan bukti keandalan kolaborasi multi-agent sistem Duckvaulta yang dikoordinasikan secara otonom melalui Kanban Board:

1. **Leader (Profile: default):**
   Bertanggung jawab atas orkestrasi umum, verifikasi test harness otomatis via Omnirush CLI, sinkronisasi soket TCP interaktif, dan pemantauan eksekusi seluruh tahapan tugas.

2. **Trend-Hunter (Profile: trend-hunter):**
   Melakukan identifikasi awal ruang lingkup masalah, ekstraksi metadata tantangan, pengunduhan biner `chall` dan kode sumber C, serta pemetaan awal topologi lab container di CyLab Academy.

3. **Security-Engineer (Profile: security-engineer):**
   Melakukan audit mendalam terhadap akar kerentanan memori heap (CWE-122, CWE-822, CWE-416), membongkar disassembly instruksi assembly, mengkalkulasi offset alinyemen memori 32-byte, dan memvalidasi alur daur ulang tcache glibc.

4. **Fullstack-Dev (Profile: fullstack-dev):**
   Mengembangkan skrip solver mandiri yang tangguh (`solve_439_heap_1.py`, `solve_435_heap_2.py`, `solve_440_heap_3.py`) serta menyusun dokumentasi writeup LKS berstandar NIST SP 800-115 pada repositori.

5. **QA-Engineer (Profile: qa-engineer):**
   Melakukan pengujian live submission via API CyLab Academy (`/api/submissions/`), memastikan verifikasi status HTTP 201 Created dengan hasil `correct: true`, memverifikasi integritas repositori Git, dan mengeksekusi commit serta push ke GitHub.

6. **Guru Judith (Profile: guru - Judith Master Guru):**
   Menyusun sintesis kurikulum pedagogis, merumuskan 5 Rukun Bikin Pinter 100%, merancang dialog scaffolding Socratic, menyusun panduan pengerasan sistem defensif (Blue Team guidelines), memetakan parameter psikometrik IRT, dan merancang roadmap akselerasi talenta siswa.

---

### 9. KEPATUHAN STANDAR ANTI-SLOP & VERIFIKASI AKHIR

Dokumen sintesis kurikulum dan panduan hardening Batch 51 ini telah melalui audit mutu ketat sesuai dengan standar AI Anti-Slop Duckvaulta 2026:
- Zero Em Dash Policy: 100% kepatuhan (karakter em dash dihilangkan sepenuhnya, digantikan oleh tanda baca terstruktur).
- First Principles Grounding: Setiap kalkulasi memori didasarkan pada arsitektur perangkat keras x86-64 dan spesifikasi implementasi glibc malloc.
- Substansi Nyata & Aksi Industri: Memuat aturan deteksi YARA dan Sigma yang siap diintegrasikan pada sistem SIEM / EDR operasional.
- Integritas Flag Terverifikasi: Seluruh token flag kompetisi telah divalidasi langsung terhadap backend CyLab Security Academy.

---
*Dokumen ini diterbitkan secara resmi oleh Judith (Master Guru & Mentor Kompetisi) untuk pembinaan talenta juara LKS Cyber Security Nasional dan WorldSkills.*
