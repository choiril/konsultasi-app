# 🗓️ CODING CHECKLIST

Checklist ini digunakan sebagai **panduan kerja harian** selama pengembangan aplikasi **Buku Tamu & Konsultasi**.

Dokumen ini **bukan dokumentasi teknis detail**, melainkan **peta kerja praktis** agar:

* Tidak bingung harus mengerjakan apa setiap hari
* Terhindar dari overengineering
* Mudah melanjutkan coding setelah jeda

Estimasi waktu: **±1–2 jam per hari**

---

## DAY 1 — Setup, Model, & Database Foundation (Combined)

**Target:** Fondasi aplikasi siap tanpa refactor besar

### A. Environment & Project Health

* [-] Aktifkan virtual environment
* [-] Jalankan `python manage.py runserver` tanpa error
* [ ] Pastikan koneksi PostgreSQL aktif
* [ ] Pastikan `STATIC_ROOT` & `MEDIA_ROOT` terbaca
* [ ] Buat superuser
* [ ] Login ke Django Admin

### B. Implementasi Model Core (sesuai ERD Final)

* [ ] Buat model BukuTamu
* [ ] Buat model Konsultasi
* [ ] Buat model HasilKonsultasi
* [ ] Buat model Lampiran (foto, ttd, pdf)
* [ ] Definisikan ForeignKey sesuai ERD Final
* [ ] Pastikan field nullable sesuai flow
* [ ] Tambahkan `__str__()` pada setiap model

### C. Migrasi & Validasi Database

* [ ] Jalankan `makemigrations`
* [ ] Jalankan `migrate`
* [ ] Test create data via Django shell
* [ ] Validasi relasi ForeignKey

**Output:**

* ✅ Struktur data final
* ✅ Database siap dipakai
* ✅ Admin panel dapat diakses

---

## DAY 4 — Admin Panel Minimal

**Target:** Data bisa dikelola tanpa UI custom

* [ ] Register semua model di admin
* [ ] Atur `list_display`
* [ ] Atur `search_fields`
* [ ] Atur filter status

**Output:**

* ✅ Petugas dapat mengelola data via Admin

---

## DAY 5 — Flow Pengunjung (Buku Tamu)

**Target:** Pengunjung tanpa login bisa input data

* [ ] Buat view form buku tamu
* [ ] Validasi input
* [ ] Simpan data ke database
* [ ] Redirect ke halaman sukses
* [ ] Template HTML sederhana

**Output:**

* ✅ Data buku tamu tersimpan di DB

---

## DAY 6 — Flow Konsultasi Online

**Target:** Konsultasi tercatat dan terhubung

* [ ] Buat form konsultasi
* [ ] Hubungkan ke Buku Tamu
* [ ] Set status awal otomatis
* [ ] Validasi submit
* [ ] Halaman konfirmasi

**Output:**

* ✅ Konsultasi tercatat
* ✅ Status awal konsisten

---

## DAY 7 — Dashboard Internal (Read-Only)

**Target:** Petugas bisa membaca data

* [ ] List data konsultasi
* [ ] Filter berdasarkan status
* [ ] Halaman detail konsultasi
* [ ] Navigasi sederhana

**Output:**

* ✅ Petugas dapat memantau antrian konsultasi

---

## DAY 8 — Input Hasil Konsultasi

**Target:** Inti proses bisnis berjalan

* [ ] Form input hasil konsultasi
* [ ] Simpan sebagai kertas kerja
* [ ] Update status konsultasi
* [ ] Validasi hanya bisa submit sekali

**Output:**

* ✅ Hasil konsultasi tersimpan
* ✅ Status otomatis berubah

---

## DAY 9 — Status Rules & Locking Data

**Target:** Data aman & konsisten

* [ ] Definisikan enum/status final
* [ ] Validasi transisi status
* [ ] Lock data setelah status selesai
* [ ] Cegah double input / edit

**Output:**

* ✅ Integritas data terjaga

---

## DAY 10 — Template Cetak PDF

**Target:** Hasil konsultasi bisa dicetak

* [ ] Buat template HTML khusus cetak
* [ ] Styling minimal & rapi
* [ ] Generate PDF
* [ ] Simpan file PDF

**Output:**

* ✅ PDF hasil konsultasi tersedia

---

## DAY 11 — Export Excel Laporan

**Target:** Laporan siap dipakai instansi

* [ ] Buat query laporan
* [ ] Mapping kolom Excel
* [ ] Download file Excel
* [ ] Test dengan data dummy

**Output:**

* ✅ Excel rapi & konsisten

---

## DAY 12 — Upload Foto & Tanda Tangan (WebP)

**Target:** Penyimpanan efisien

* [ ] Upload foto / tanda tangan
* [ ] Convert file ke format WebP
* [ ] Simpan metadata
* [ ] Tampilkan preview

**Output:**

* ✅ File ringan & hemat storage

---

## DAY 13 — Validasi, Error Handling & UX

**Target:** Aman untuk user awam

* [ ] Validasi form lengkap
* [ ] Pesan error ramah pengguna
* [ ] Handle 404 & 403
* [ ] Feedback sukses / gagal

**Output:**

* ✅ UX jelas & minim error membingungkan

---

## DAY 14 — Permission & Final UAT

**Target:** Siap deploy ke production

* [ ] Pisahkan public vs internal page
* [ ] Staff-only access
* [ ] UAT berdasarkan User Story Final
* [ ] Simulasi alur penuh end-to-end

**Output:**

* ✅ Aplikasi siap deploy

---

## 🚦 Step-Point Rule (Aturan Berhenti Aman)

Gunakan aturan ini untuk mencegah overengineering dan kelelahan saat coding.

### 🟥 WAJIB BERHENTI jika:

* `runserver` error lebih dari **15 menit** tanpa progres
* Migrasi gagal dan butuh reset skema
* Mulai ingin menambah field di luar ERD Final
* Mulai memikirkan fitur UI sebelum flow dasar jalan

### 🟨 BOLEH LANJUT dengan hati-hati jika:

* Hanya merapikan penamaan field
* Menambahkan `help_text` atau `verbose_name`
* Refactor kecil tanpa mengubah struktur data

### 🟩 BOLEH LANJUT NORMAL jika:

* Checklist hari tersebut hampir selesai
* Perubahan tidak mempengaruhi migrasi
* Hanya menambah validasi ringan

### 🎯 Prinsip Utama

> "Jika fondasi sudah stabil, berhenti. Jangan poles pondasi."

---

## 📌 Catatan Penggunaan

* Checklist ini **boleh disesuaikan** jika ada perubahan kebutuhan
* Jika satu hari terlewat, **lanjutkan dari hari terakhir**, tidak perlu mengulang
* Fokus pada **fungsi berjalan**, bukan kesempurnaan kode
