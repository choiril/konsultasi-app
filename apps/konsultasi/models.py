from django.db import models
from django.utils import timezone

# Create your models here.
# membuat prefix bulan
MONTH_PREFIX = {
    1: "JAN",
    2: "FEB",
    3: "MAR",
    4: "APR",
    5: "MEI",
    6: "JUN",
    7: "JUL",
    8: "AGU",
    9: "SEP",
    10: "OKT",
    11: "NOV",
    12: "DES",
}

class TipeKunjungan(models.Model):
    id_tipe = models.SmallIntegerField(primary_key=True)
    nama_tipe = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Tipe Kunjungan"
        verbose_name_plural = "Tipe Kunjungan"

    def __str__(self):
        return self.nama_tipe


class KategoriLayanan(models.Model):
    id_kategori = models.SmallIntegerField(primary_key=True)
    nama_kategori = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Kategori Layanan"
        verbose_name_plural = "Kategori Layanan"

    def __str__(self):
        return self.nama_kategori


class JenisLayanan(models.Model):
    id_jenis = models.SmallIntegerField(primary_key=True)
    kategori = models.ForeignKey(
        KategoriLayanan,
        on_delete=models.PROTECT
    )
    nama_jenis = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Jenis Layanan"
        verbose_name_plural = "Jenis Layanan"

    def __str__(self):
        return self.nama_jenis


class MediaKonsultasi(models.Model):
    id_media = models.SmallIntegerField(primary_key=True)
    nama_media = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Media Konsultasi"
        verbose_name_plural = "Media Konsultasi"

    def __str__(self):
        return self.nama_media


class SumberJawaban(models.Model):
    id_sumber = models.SmallIntegerField(primary_key=True)
    nama_sumber = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Sumber Jawaban"
        verbose_name_plural = "Sumber Jawaban"

    def __str__(self):
        return self.nama_sumber

class Tamu(models.Model):
    id_tamu = models.BigAutoField(primary_key=True)
    nama = models.CharField(max_length=100)
    email = models.EmailField()
    no_hp = models.CharField(max_length=20)
    instansi_perusahaan = models.CharField(max_length=150)
    alamat = models.TextField()

    class Meta:
        verbose_name = "Tamu"
        verbose_name_plural = "Tamu"

    def __str__(self):
        return self.nama


class Petugas(models.Model):
    id_petugas = models.BigAutoField(primary_key=True)
    nama_petugas = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    role = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    ttd_petugas = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Petugas"
        verbose_name_plural = "Petugas"

    def __str__(self):
        return self.nama_petugas

class Kunjungan(models.Model):
    id_kunjungan = models.BigAutoField(primary_key=True)

    nomor_kunjungan = models.CharField(
        max_length=20,
        blank=True,
        editable=False
    )

    tanggal_kunjungan = models.DateField(
        default=timezone.now
    )

    tamu = models.ForeignKey(Tamu, on_delete=models.PROTECT)
    tipe = models.ForeignKey(TipeKunjungan, on_delete=models.PROTECT)
    kategori = models.ForeignKey(KategoriLayanan, on_delete=models.PROTECT)
    jenis = models.ForeignKey(JenisLayanan, on_delete=models.PROTECT)

    pertanyaan = models.TextField()
    jawaban = models.TextField(blank=True)

    media = models.ForeignKey(
        MediaKonsultasi,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    sumber = models.ForeignKey(
        SumberJawaban,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    foto_tamu = models.CharField(max_length=255)
    ttd_tamu = models.CharField(max_length=255)

    petugas = models.ForeignKey(
        Petugas,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    status_selesai = models.BooleanField(default=False)
    waktu_selesai = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Kunjungan"
        verbose_name_plural = "Kunjungan"
        ordering = ["-id_kunjungan"]
        constraints = [
            models.UniqueConstraint(
                fields=["tanggal_kunjungan", "nomor_kunjungan"],
                name="unique_nomor_kunjungan_per_tanggal"
            )
        ]

    def save(self, *args, **kwargs):
        if not self.nomor_kunjungan:
            tanggal = self.tanggal_kunjungan or timezone.now().date()
            bulan = tanggal.month
            tahun = tanggal.year

            prefix = MONTH_PREFIX.get(bulan, "XXX")

            last = (
                Kunjungan.objects
                .filter(
                    tanggal_kunjungan__year=tahun,
                    tanggal_kunjungan__month=bulan,
                    nomor_kunjungan__startswith=prefix
                )
                .order_by("id_kunjungan")
                .last()
            )

            last_number = 0
            if last and last.nomor_kunjungan:
                last_number = int(last.nomor_kunjungan.replace(prefix, ""))

            self.nomor_kunjungan = f"{prefix}{last_number + 1:04d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nomor_kunjungan} - {self.tamu.nama}"
