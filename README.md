# 📘 Aplikasi Buku Tamu & Konsultasi

Aplikasi ini digunakan untuk mencatat **buku tamu** dan **konsultasi** (online maupun langsung) dengan alur sederhana, aman, dan mudah dikembangkan.

Proyek ini dirancang dengan prinsip:

* Tidak overengineering
* Mudah dipahami pemula
* Fokus pada alur kerja nyata instansi
* Siap dikembangkan bertahap

---

## 🎯 Tujuan Aplikasi

* Mencatat data pengunjung (tanpa login)
* Menyediakan form konsultasi online
* Memfasilitasi petugas untuk mencatat hasil konsultasi
* Menghasilkan dokumen **PDF** dan **Excel** sebagai laporan
* Menyimpan foto & tanda tangan secara efisien (format WebP)

---

## 🧱 Tech Stack

* **Backend**: Django
* **Database**: PostgreSQL
* **Frontend**: Django Template (HTML)
* **File Output**: PDF, Excel
* **Media**: WebP (foto & tanda tangan)

---

## 📂 Struktur Folder (Ringkas)

```text
project-root/
├── apps/                # Django apps (core domain)
├── config/              # settings & konfigurasi
├── templates/           # HTML templates
├── static/              # static files
├── media/               # upload files
├── docs/                # dokumentasi teknis
│   └── CODING_CHECKLIST.md
├── manage.py
└── README.md
```

---

## 🚀 Cara Menjalankan Project (Development)

1. Aktifkan virtual environment
2. Install dependency

   ```bash
   pip install -r requirements.txt
   ```
3. Jalankan migrasi

   ```bash
   python manage.py migrate
   ```
4. Buat superuser

   ```bash
   python manage.py createsuperuser
   ```
5. Jalankan server

   ```bash
   python manage.py runserver
   ```

Akses:

* Aplikasi: `http://127.0.0.1:8000/`
* Admin: `http://127.0.0.1:8000/admin/`

---

## 🗺️ Development Roadmap

Proses pengembangan dilakukan **bertahap dan terstruktur** berdasarkan:

* ERD Final
* Flowchart Final
* User Story Final

Checklist harian pengembangan dapat dilihat di:

📄 **[`docs/CODING_CHECKLIST.md`](docs/CODING_CHECKLIST.md)**

Dokumen ini menjadi panduan utama coding harian agar:

* Fokus
* Konsisten
* Mudah dilanjutkan setelah jeda

---

## 🔐 Prinsip Keamanan & Data

* Pengunjung **tidak perlu login**
* Akses internal dibatasi untuk petugas
* Data dikunci setelah status selesai
* File disimpan dengan ukuran efisien

---

## 📌 Catatan

* Proyek ini dikembangkan secara **iteratif**
* Fitur tambahan akan mengikuti kebutuhan nyata, bukan asumsi
* Dokumentasi akan diperbarui seiring perkembangan aplikasi

---

## 📄 Lisensi

Internal use / sesuai kebutuhan instansi.
