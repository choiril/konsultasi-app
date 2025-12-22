from django.db import models, transaction
from django.utils import timezone
from django.core.exceptions import ValidationError


MONTH_PREFIX = {
    1: "JAN", 2: "FEB", 3: "MAR", 4: "APR",
    5: "MEI", 6: "JUN", 7: "JUL", 8: "AGU",
    9: "SEP", 10: "OKT", 11: "NOV", 12: "DES",
}


# ===== MASTER DATA =====

class TipeKunjungan(models.Model):
    """
    Tipe kunjungan: Offline, Online
    """
    id_tipe = models.SmallIntegerField(primary_key=True)
    nama_tipe = models.CharField(max_length=50)

    class Meta:
        db_table = "tipe_kunjungan"
        verbose_name = "Tipe Kunjungan"
        verbose_name_plural = "Tipe Kunjungan"

    def __str__(self):
        return self.nama_tipe


class KategoriLayanan(models.Model):
    """
    Kategori: Pendaftaran/Verifikasi, Konsultasi, Informasi/Lainnya
    """
    id_kategori = models.SmallIntegerField(primary_key=True)
    nama_kategori = models.CharField(max_length=100)

    class Meta:
        db_table = "kategori_layanan"
        verbose_name = "Kategori Layanan"
        verbose_name_plural = "Kategori Layanan"

    def __str__(self):
        return self.nama_kategori


class JenisLayanan(models.Model):
    """
    Jenis layanan: SPSE, E-Katalog, SiRUP, dll
    """
    id_jenis = models.SmallIntegerField(primary_key=True)
    id_kategori = models.ForeignKey(
        KategoriLayanan,
        on_delete=models.PROTECT,
        db_column='id_kategori',
        related_name="jenis_layanan"
    )
    nama_jenis = models.CharField(max_length=100)

    class Meta:
        db_table = "jenis_layanan"
        verbose_name = "Jenis Layanan"
        verbose_name_plural = "Jenis Layanan"
        indexes = [
            models.Index(fields=['id_kategori']),
        ]

    def __str__(self):
        return f"{self.nama_jenis} ({self.id_kategori.nama_kategori})"


class MediaKonsultasi(models.Model):
    """
    Media: Tatap Muka, WA, Email, Telp, Zoom
    """
    id_media = models.SmallIntegerField(primary_key=True)
    nama_media = models.CharField(max_length=50)

    class Meta:
        db_table = "media_konsultasi"
        verbose_name = "Media Konsultasi"
        verbose_name_plural = "Media Konsultasi"

    def __str__(self):
        return self.nama_media


class SumberJawaban(models.Model):
    """
    Sumber: Perpres, Manual SPSE, FAQ, Praktik Lapangan, dll
    """
    id_sumber = models.SmallIntegerField(primary_key=True)
    nama_sumber = models.CharField(max_length=100)

    class Meta:
        db_table = "sumber_jawaban"
        verbose_name = "Sumber Jawaban"
        verbose_name_plural = "Sumber Jawaban"

    def __str__(self):
        return self.nama_sumber


# ===== AKTOR =====

class Tamu(models.Model):
    id_tamu = models.BigAutoField(primary_key=True)
    nama = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, blank=True)
    no_hp = models.CharField(max_length=15, blank=True)
    instansi_perusahaan = models.CharField(max_length=150, blank=True)
    alamat = models.TextField(blank=True)

    class Meta:
        db_table = "tamu"
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
    ttd_petugas = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = "petugas"
        verbose_name = "Petugas"
        verbose_name_plural = "Petugas"
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return self.nama_petugas


# ===== MODEL INTI =====

class Kunjungan(models.Model):
    """
    Model utama kunjungan tamu LPSE
    
    Flow:
    1. Tamu registrasi -> generate nomor -> status: menunggu
    2. Petugas melayani:
       - Konsultasi: isi jawaban + media + sumber
       - Non-konsultasi: langsung selesai
    3. Status selesai -> cetak lembar
    """
    id_kunjungan = models.BigAutoField(primary_key=True)

    nomor_kunjungan = models.CharField(
        max_length=20,
        blank=True,
        editable=False,
        db_index=True,
        help_text="Auto-generated: BULAN9999 (contoh: DES0001)"
    )

    tanggal_kunjungan = models.DateField(
        default=timezone.now,
        help_text="Default hari ini, bisa diganti"
    )

    # === RELASI UTAMA ===
    id_tamu = models.ForeignKey(
        Tamu,
        on_delete=models.PROTECT,
        db_column='id_tamu',
        related_name="kunjungan"
    )

    id_tipe = models.ForeignKey(
        TipeKunjungan,
        on_delete=models.PROTECT,
        db_column='id_tipe',
        related_name="kunjungan"
    )

    id_kategori = models.ForeignKey(
        KategoriLayanan,
        on_delete=models.PROTECT,
        db_column='id_kategori',
        related_name="kunjungan"
    )

    id_jenis = models.ForeignKey(
        JenisLayanan,
        on_delete=models.PROTECT,
        db_column='id_jenis',
        related_name="kunjungan"
    )

    # === KONTEN ===
    pertanyaan = models.TextField(
        blank=True,
        help_text="Wajib untuk kategori konsultasi"
    )

    jawaban = models.TextField(
        blank=True,
        help_text="Diisi petugas untuk konsultasi"
    )

    # === RELASI KONSULTASI ===
    id_media = models.ForeignKey(
        MediaKonsultasi,
        on_delete=models.PROTECT,
        db_column='id_media',
        null=True,
        blank=True,
        related_name="kunjungan",
        help_text="Wajib untuk konsultasi"
    )

    id_sumber = models.ForeignKey(
        SumberJawaban,
        on_delete=models.PROTECT,
        db_column='id_sumber',
        null=True,
        blank=True,
        related_name="kunjungan",
        help_text="Wajib untuk konsultasi"
    )

    # === DOKUMENTASI ===
    foto_tamu = models.CharField(max_length=255, blank=True)
    ttd_tamu = models.CharField(max_length=255, blank=True)

    # === PETUGAS ===
    id_petugas = models.ForeignKey(
        Petugas,
        on_delete=models.SET_NULL,
        db_column='id_petugas',
        null=True,
        blank=True,
        related_name="kunjungan"
    )

    # === STATUS ===
    status_selesai = models.BooleanField(default=False)
    waktu_selesai = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "kunjungan"
        verbose_name = "Kunjungan"
        verbose_name_plural = "Kunjungan"
        ordering = ["-id_kunjungan"]
        indexes = [
            models.Index(fields=['tanggal_kunjungan']),
            models.Index(fields=['status_selesai']),
            models.Index(fields=['-id_kunjungan']),
            models.Index(fields=['id_tipe']),
            models.Index(fields=['id_kategori']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["tanggal_kunjungan", "nomor_kunjungan"],
                name="unique_nomor_kunjungan_per_tanggal"
            )
        ]

    # ===== HELPER PROPERTIES =====
    @property
    def is_konsultasi(self):
        """Cek apakah kategori adalah konsultasi"""
        if self.id_kategori:
            return 'konsultasi' in self.id_kategori.nama_kategori.lower()
        return False

    @property
    def is_offline(self):
        """Cek apakah tipe kunjungan offline"""
        if self.id_tipe:
            return self.id_tipe.nama_tipe.lower() == 'offline'
        return False

    # ===== VALIDASI =====
    def clean(self):
        """
        Validasi business logic sesuai flowchart
        """
        # 1. Validasi jenis layanan harus sesuai kategori
        if self.id_jenis and self.id_kategori:
            if self.id_jenis.id_kategori_id != self.id_kategori_id:
                raise ValidationError({
                    'id_jenis': 'Jenis layanan tidak sesuai dengan kategori yang dipilih.'
                })

        # 2. Validasi konsultasi wajib ada pertanyaan
        if self.is_konsultasi and not self.pertanyaan:
            raise ValidationError({
                'pertanyaan': 'Pertanyaan wajib diisi untuk kategori konsultasi.'
            })

        # 3. Validasi konsultasi selesai wajib lengkap
        if self.status_selesai and self.is_konsultasi:
            errors = {}

            if not self.jawaban:
                errors['jawaban'] = 'Jawaban wajib diisi untuk menyelesaikan konsultasi.'

            if not self.id_media_id:
                errors['id_media'] = 'Media konsultasi wajib dipilih.'

            if not self.id_sumber_id:
                errors['id_sumber'] = 'Sumber jawaban wajib dipilih.'

            if errors:
                raise ValidationError(errors)

    # ===== SAVE =====
    @transaction.atomic
    def save(self, *args, **kwargs):
        """
        Override save untuk:
        1. Auto-generate nomor kunjungan
        2. Auto-set media tatap muka untuk offline konsultasi
        3. Auto-set waktu selesai
        """
        # 1. Generate nomor kunjungan
        if not self.nomor_kunjungan:
            tanggal = self.tanggal_kunjungan or timezone.now().date()
            prefix = MONTH_PREFIX.get(tanggal.month, "XXX")

            last = (
                Kunjungan.objects
                .select_for_update()
                .filter(
                    tanggal_kunjungan__year=tanggal.year,
                    tanggal_kunjungan__month=tanggal.month,
                    nomor_kunjungan__startswith=prefix
                )
                .order_by("-id_kunjungan")
                .first()
            )

            last_number = 0
            if last and last.nomor_kunjungan:
                try:
                    last_number = int(last.nomor_kunjungan.replace(prefix, ""))
                except (ValueError, TypeError):
                    last_number = 0

            self.nomor_kunjungan = f"{prefix}{last_number + 1:04d}"

        # 2. Auto-set media "Tatap Muka" untuk offline konsultasi
        if self.is_offline and self.is_konsultasi and self.status_selesai:
            if not self.id_media_id:
                try:
                    tatap_muka = MediaKonsultasi.objects.get(
                        nama_media__iexact='tatap muka'
                    )
                    self.id_media = tatap_muka
                except MediaKonsultasi.DoesNotExist:
                    pass

        # 3. Auto-set waktu selesai
        if self.status_selesai and not self.waktu_selesai:
            self.waktu_selesai = timezone.now()

        # Validasi sebelum save
        self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nomor_kunjungan} - {self.id_tamu.nama}"