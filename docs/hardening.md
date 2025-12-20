# Hardening Notes – Day 4

Berikut penguatan kecil yang dilakukan tanpa mengubah struktur data.

---

## A. Model Level

✔ Semua model memiliki `__str__()` informatif  
✔ Semua FK penting menggunakan `PROTECT`  
✔ Validasi bisnis di `clean()`  
✔ Penomoran kunjungan aman dari race condition (`select_for_update`)  

---

## B. Admin Level

✔ Readonly fields dinamis setelah selesai  
✔ Konsultasi tidak bisa diselesaikan via bulk  
✔ Query dioptimalkan dengan `select_related`  
✔ Tampilan admin informatif (badge, status, preview)

---

## C. Performance Safety

✔ Index pada:
- tanggal_kunjungan
- status_selesai
- kategori
- tipe
✔ Tidak ada query N+1 di list admin
✔ Search fields dibatasi field pendek

---

## D. Human Error Prevention

✔ Nomor kunjungan tidak bisa diedit  
✔ Tanggal terkunci setelah selesai  
✔ Konsultasi incomplete tidak bisa disave  
✔ Media otomatis untuk offline konsultasi

---

## E. Deferred Hardening (Day 6+)

⏳ Audit trail
⏳ Permission berbasis role Django
⏳ Public form rate limiting
