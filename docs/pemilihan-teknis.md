# Technical Decisions – Buku Tamu

Dokumen ini menjelaskan keputusan desain utama.

---

## 1. Kenapa tanggal_kunjungan pakai default=timezone.now?

- Lebih fleksibel dari `auto_now_add`
- Bisa input data backdate
- Sesuai alur manual offline
- Dikunci setelah selesai (admin level)

---

## 2. Kenapa nomor_kunjungan digenerate di model?

- Menjamin konsistensi
- Aman dari race condition
- Tidak bergantung pada admin/form
- Mudah dipakai API / public form nanti

---

## 3. Kenapa validasi di clean(), bukan admin?

- Berlaku untuk semua entry point
- Aman untuk API & import
- Single source of truth

---

## 4. Kenapa konsultasi tidak boleh bulk selesai?

- Konsultasi punya konten jawaban
- Perlu audit manual
- Menghindari data kosong

---

## 5. Kenapa kategori konsultasi dideteksi via nama?

- Menghindari hardcode ID
- Lebih fleksibel konfigurasi master data
- Aman selama freeze rules dipatuhi

---

## 6. Kenapa admin dynamic fieldsets?

- Mengurangi noise form
- Fokus sesuai flowchart
- Mengurangi human error
