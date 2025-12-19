from django.contrib import admin

# Register your models here.
from .models import (
    TipeKunjungan, KategoriLayanan,
    JenisLayanan, MediaKonsultasi,
    SumberJawaban, Tamu, Petugas,
    Kunjungan
)

@admin.register(TipeKunjungan)
class TipeKunjunganAdmin(admin.ModelAdmin):
    list_display = ("id_tipe", "nama_tipe")


@admin.register(KategoriLayanan)
class KategoriLayananAdmin(admin.ModelAdmin):
    list_display = ("id_kategori", "nama_kategori")


@admin.register(JenisLayanan)
class JenisLayananAdmin(admin.ModelAdmin):
    list_display = ("id_jenis", "nama_jenis", "kategori")
    list_filter = ("kategori",)


@admin.register(MediaKonsultasi)
class MediaKonsultasiAdmin(admin.ModelAdmin):
    list_display = ("id_media", "nama_media")


@admin.register(SumberJawaban)
class SumberJawabanAdmin(admin.ModelAdmin):
    list_display = ("id_sumber", "nama_sumber")

@admin.register(Tamu)
class TamuAdmin(admin.ModelAdmin):
    list_display = ("id_tamu", "nama", "email", "no_hp", "instansi_perusahaan")
    search_fields = ("nama", "email", "no_hp", "instansi_perusahaan")

@admin.register(Petugas)
class PetugasAdmin(admin.ModelAdmin):
    list_display = ("id_petugas", "nama_petugas", "username", "role", "is_active")
    list_filter = ("role", "is_active")
    search_fields = ("nama_petugas", "username")

@admin.register(Kunjungan)
class KunjunganAdmin(admin.ModelAdmin):
    list_display = (
        "nomor_kunjungan",
        "tanggal_kunjungan",
        "tamu",
        "kategori",
        "jenis",
        "status_selesai",
    )

    list_filter = (
        "status_selesai",
        "kategori",
        "tipe",
        "tanggal_kunjungan",
    )

    search_fields = (
        "nomor_kunjungan",
        "tamu__nama",
        "tamu__instansi_perusahaan",
    )

    readonly_fields = (
        "nomor_kunjungan",
        "tanggal_kunjungan",
    )

    ordering = ("-tanggal_kunjungan",)