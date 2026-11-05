# CyLab Batch 60: Omnirush Automated Execution & Solver Verification Report

**Lead Orchestrator:** David (Leader / Agent Nyawit)  
**Execution Engine:** Omnirush CLI Automated Test Harness & Verification Suite  
**Repository Target:** `lionelsabdani36-ai/cylab-ctf-writeups` (Commit `8b145e8`)  
**Date:** 2026-11-05  

---

## 1. Executive Summary & AI Team Alignment

Dalam eksekusi CyLab Batch 60, seluruh instrumen pengujian solver dan pipeline verifikasi otomatis telah dijalankan dan divalidasi 100% PASS (3/3 target terselesaikan, terkompilasi, dan teruji stabil):

- **Charlie (trend-hunter):** Reconnaissance dan identifikasi 3 target berbobot tinggi pada kategori Reverse Engineering (POSIX IPC concurrency dan ARMv8-A AArch64 tracing).
- **Athena (security-engineer):** Audit akar kerentanan konkurensi mmap MAP_SHARED, signed integer overflow, serta semantik instruksi branch carry ARMv8-A.
- **Alex (fullstack-dev):** Deployment skrip solver python standalone dan dokumentasi writeup teknis berstandar kompetisi LKS Nasional & NIST SP 800-115.
- **David & Omnirush (default):** Orkestrasi harness pengujian otomatis, verifikasi py_compile, differential logic check, dan validasi runtime output.
- **Julius (qa-engineer):** Verifikasi live flag submission HTTP 201 (`correct: true`) via REST API CyLab dan git repository sync parity.
- **Judith (guru):** Sintesis kurikulum bimbingan teknis persiapan LKS Cyber Security bidang Reverse Engineering dan Defensive Mitigation.

---

## 2. Test Harness Results Matrix

| No | ID | Nama Tantangan | Event / Kategori | py_compile | Standalone Exec | Output Flag (Verified) | Status |
|:---|:---|:---------------|:-----------------|:-----------|:----------------|:-----------------------|:-------|
| 1 | 24 | Forky | picoCTF 2019 / Rev Eng | PASS | PASS | `academy{-721750240}` | **100% PASS** |
| 2 | 150 | ARMssembly 2 | picoCTF 2021 / Rev Eng | PASS | PASS | `academy{e815ef32}` | **100% PASS** |
| 3 | 106 | ARMssembly 3 | picoCTF 2021 / Rev Eng | PASS | PASS | `academy{00000024}` | **100% PASS** |

---

## 3. Technical Verification & Invariant Analysis

### A. Challenge 24: Forky (Shared Memory Concurrency)
- **Path:** `scripts/solve_24_forky.py`
- **Mechanism:** Program mengalokasikan memori bersama 4-byte dengan `mmap(..., MAP_SHARED | MAP_ANONYMOUS, ...)`. Nilai awal `0x3b9aca00` (1,000,000,000). Eksekusi `fork()` sebanyak 4 kali membentuk pohon proses berukuran $2^4 = 16$ proses. Masing-masing proses menambahkan konstanta `0x499602d2` (1,234,567,890).
- **Formula:** `(1000000000 + 16 * 1234567890) & 0xffffffff = 3573217056 (0xd4fd7f20)`.
- **Signed Integer Representation:** Nilai direpresentasikan sebagai 32-bit signed integer register EAX, menghasilkan nilai desimal `-721750240`.
- **Harness Output:** `academy{-721750240}` terbukti identik dengan token validasi server.

### B. Challenge 150: ARMssembly 2 (ARMv8-A Loop Accumulation)
- **Path:** `scripts/solve_150_armssembly_2.py`
- **Mechanism:** Simulasi prosedur AArch64 `func1`. Argument `w0 = 2729572966` disimpan pada `[sp, 12]`. Loop `.L3` menambahkan konstanta 3 ke akumulator `[sp, 24]` sebanyak nilai `w0` kali, dengan kondisi terminasi `cmp w1, w0; bcc .L3` (unsigned comparison).
- **Formula:** `(2729572966 * 3) & 0xffffffff = 3893751602 (0xe815ef32)`.
- **Formatting:** Format hex 32-bit lowercase 8 karakter: `e815ef32`.
- **Harness Output:** `academy{e815ef32}` lolos verifikasi komputasi.

### C. Challenge 106: ARMssembly 3 (ARMv8-A Hamming Weight / Popcount)
- **Path:** `scripts/solve_106_armssembly_3.py`
- **Mechanism:** Prosedur `func1` menerima argumen `w0 = 605030239` (`0b100100000100000000011101011111`). Algoritma memeriksa LSB (`and w0, w0, 1`), memanggil `func2` (menambah 3) setiap bit bernilai 1, lalu menggeser logis ke kanan (`lsr w0, w0, 1`).
- **Formula:** `popcount(605030239) = 12`. Akumulator akhir: $12 \times 3 = 36$ (`0x24`).
- **Formatting:** Format hex 32-bit lowercase 8 karakter: `00000024`.
- **Harness Output:** `academy{00000024}` lolos verifikasi komputasi.

---

## 4. Repository Synchronization & Deliverables

- **Git Commit:** `8b145e855aa383e070967917d4b3f2b2f38dcfcc`
- **Commit Message:** `Batch 60 (3/3): 24 Forky, 150 ARMssembly 2, 106 ARMssembly 3 + solvers/writeups/README`
- **Remote Status:** Synchronized with `origin/main` (working tree clean)
- **README Status:** Total Solved ter-update ke 318 / 525 (Platform Live Solved: 395 / 525)
- **Test Artifacts:**
  - `/home/lionelsabdani36/.hermes/kanban/workspaces/t_c5085f8b/test_batch60_harness.py`
  - `/home/lionelsabdani36/.hermes/kanban/workspaces/t_c5085f8b/batch60_verification_report.json`
  - `/home/lionelsabdani36/.hermes/kanban/workspaces/t_c5085f8b/OMNIRUSH_AUTOMATED_EXECUTION_BATCH60.md`
