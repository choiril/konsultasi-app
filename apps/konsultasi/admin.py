from django.contrib import admin

# Register your models here.
from .models import (
    TipeKunjungan, KategoriLayanan,
    JenisLayanan, MediaKonsultasi,
    SumberJawaban, Tamu, Petugas,
    Kunjungan
)

admin.site.register(TipeKunjungan)
admin.site.register(KategoriLayanan)
admin.site.register(JenisLayanan)
admin.site.register(MediaKonsultasi)
admin.site.register(SumberJawaban)

@admin.register(Tamu)
class TamuAdmin(admin.ModelAdmin):
    list_display = ("id_tamu", "nama", "email", "no_hp")
    search_fields = ("nama", "email", "no_hp")

@admin.register(Petugas)
class PetugasAdmin(admin.ModelAdmin):
    list_display = ("id_petugas", "nama_petugas", "username", "role", "is_active")
    list_filter = ("role", "is_active")

@admin.register(Kunjungan)
class KunjunganAdmin(admin.ModelAdmin):
    list_display = (
        "nomor_kunjungan",
        "tanggal_kunjungan",
        "tamu",
        "kategori",
        "status_selesai",
    )

    list_filter = (
        "status_selesai",
        "kategori",
    )

    search_fields = (
        "nomor_kunjungan",
        "tamu__nama",
    )

    readonly_fields = (
        "nomor_kunjungan",
        "tanggal_kunjungan",
    )
