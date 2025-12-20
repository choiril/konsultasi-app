# Freeze Rules – Sistem Buku Tamu

Dokumen ini menetapkan aturan bisnis dan teknis yang **DIBEKUKAN** setelah Day 4.
Perubahan terhadap poin-poin di bawah wajib melalui evaluasi desain ulang.

---

## A. Struktur Data (MODEL)

1. Struktur tabel dan relasi **mengacu pada ERD final**.
2. Tidak boleh menambah ForeignKey baru tanpa update ERD & flowchart.
3. Semua master data (Tipe, Kategori, Jenis, Media, Sumber) bersifat **static reference**.

---

## B. Aturan Kunjungan

### 1. Tanggal & Nomor Kunjungan
- `tanggal_kunjungan`:
  - Default = hari ini (`timezone.now`)
  - **Boleh diubah** sebelum status selesai
  - **Dikunci** setelah status selesai
- `nomor_kunjungan`:
  - Auto-generated
  - Tidak dapat diedit manual
  - Unik per bulan & tanggal

---

### 2. Status Kunjungan
- Default: `status_selesai = False`
- Status hanya berubah menjadi `True` jika:
  - Non-konsultasi → boleh bulk
  - Konsultasi → **wajib lewat form detail**

---

## C. Aturan Konsultasi

1. Kategori mengandung kata **"konsultasi"** dianggap konsultasi.
2. Konsultasi **WAJIB**:
   - Pertanyaan
   - Jawaban (saat selesai)
   - Media konsultasi
   - Sumber jawaban
3. Konsultasi **offline**:
   - Media otomatis = *Tatap Muka*
4. Konsultasi **tidak boleh diselesaikan via bulk action**.

---

## D. Hak Edit Admin

1. Setelah `status_selesai = True`, field berikut dikunci:
   - Tamu
   - Tipe kunjungan
   - Kategori
   - Jenis layanan
   - Tanggal kunjungan
2. Waktu selesai **selalu auto-set**, tidak bisa diedit.

---

## E. Data Integrity

1. Jenis layanan harus sesuai kategori.
2. Validasi dijalankan di level model (`clean()`).
3. Semua save Kunjungan dijalankan dalam transaksi (`transaction.atomic`).

---

## F. Larangan Perubahan Setelah Freeze

🚫 Menambah:
- Status baru
- Kategori ganda
- Alur paralel
- Soft delete
- Multi-petugas per kunjungan

Tanpa desain ulang menyeluruh.
