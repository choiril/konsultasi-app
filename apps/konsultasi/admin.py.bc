from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Q
from django.utils import timezone

from .models import (
    TipeKunjungan, KategoriLayanan,
    JenisLayanan, MediaKonsultasi,
    SumberJawaban, Tamu, Petugas,
    Kunjungan
)


# ===== MASTER DATA ADMIN =====

@admin.register(TipeKunjungan)
class TipeKunjunganAdmin(admin.ModelAdmin):
    list_display = ("id_tipe", "nama_tipe")
    search_fields = ("nama_tipe",)
    ordering = ("id_tipe",)


@admin.register(KategoriLayanan)
class KategoriLayananAdmin(admin.ModelAdmin):
    list_display = ("id_kategori", "nama_kategori", "jumlah_jenis")
    search_fields = ("nama_kategori",)
    ordering = ("id_kategori",)

    def jumlah_jenis(self, obj):
        return obj.jenis_layanan.count()
    jumlah_jenis.short_description = "Jumlah Jenis Layanan"


@admin.register(JenisLayanan)
class JenisLayananAdmin(admin.ModelAdmin):
    list_display = ("id_jenis", "nama_jenis", "id_kategori")
    list_filter = ("id_kategori",)
    search_fields = ("nama_jenis",)
    ordering = ("id_kategori", "id_jenis")
    autocomplete_fields = ["id_kategori"]


@admin.register(MediaKonsultasi)
class MediaKonsultasiAdmin(admin.ModelAdmin):
    list_display = ("id_media", "nama_media")
    search_fields = ("nama_media",)
    ordering = ("id_media",)


@admin.register(SumberJawaban)
class SumberJawabanAdmin(admin.ModelAdmin):
    list_display = ("id_sumber", "nama_sumber")
    search_fields = ("nama_sumber",)
    ordering = ("id_sumber",)


# ===== AKTOR ADMIN =====

@admin.register(Tamu)
class TamuAdmin(admin.ModelAdmin):
    list_display = ("id_tamu", "nama", "email", "no_hp", "instansi_perusahaan", "jumlah_kunjungan")
    search_fields = ("nama", "email", "no_hp", "instansi_perusahaan")
    list_per_page = 50
    ordering = ("-id_tamu",)

    fieldsets = (
        ("Informasi Pribadi", {
            "fields": ("nama", "email", "no_hp")
        }),
        ("Informasi Instansi", {
            "fields": ("instansi_perusahaan", "alamat")
        }),
    )

    def jumlah_kunjungan(self, obj):
        count = obj.kunjungan.count()
        return format_html(
            '<span style="font-weight: bold; color: {};">{}</span>',
            'green' if count > 0 else 'gray',
            count
        )
    jumlah_kunjungan.short_description = "Total Kunjungan"


@admin.register(Petugas)
class PetugasAdmin(admin.ModelAdmin):
    list_display = ("id_petugas", "nama_petugas", "username", "role", "status_aktif", "total_layanan")
    list_filter = ("role", "is_active")
    search_fields = ("nama_petugas", "username")
    list_per_page = 50
    ordering = ("-is_active", "nama_petugas")

    fieldsets = (
        ("Informasi Petugas", {
            "fields": ("nama_petugas", "username", "role")
        }),
        ("Status & Tanda Tangan", {
            "fields": ("is_active", "ttd_petugas")
        }),
    )

    def status_aktif(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="color: green; font-weight: bold;">● Aktif</span>'
            )
        return format_html(
            '<span style="color: red;">○ Tidak Aktif</span>'
        )
    status_aktif.short_description = "Status"

    def total_layanan(self, obj):
        count = obj.kunjungan.filter(status_selesai=True).count()
        return format_html(
            '<span style="font-weight: bold;">{}</span>',
            count
        )
    total_layanan.short_description = "Total Layanan Selesai"


# ===== KUNJUNGAN ADMIN =====

class KonsultasiFilter(admin.SimpleListFilter):
    """Custom filter untuk kategori konsultasi"""
    title = 'Jenis Layanan'
    parameter_name = 'jenis_layanan'

    def lookups(self, request, model_admin):
        return (
            ('konsultasi', 'Konsultasi'),
            ('pendaftaran', 'Pendaftaran/Verifikasi'),
            ('informasi', 'Informasi/Lainnya'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'konsultasi':
            return queryset.filter(id_kategori__nama_kategori__icontains='konsultasi')
        elif self.value() == 'pendaftaran':
            return queryset.filter(id_kategori__nama_kategori__icontains='pendaftaran')
        elif self.value() == 'informasi':
            return queryset.filter(id_kategori__nama_kategori__icontains='informasi')
        return queryset


@admin.register(Kunjungan)
class KunjunganAdmin(admin.ModelAdmin):
    list_display = (
        "nomor_kunjungan",
        "tanggal_kunjungan",
        "nama_tamu",
        "tipe_badge",
        "kategori_badge",
        "jenis_layanan",
        "petugas_layanan",
        "status_badge",
    )

    list_filter = (
        "status_selesai",
        "id_tipe",
        "id_kategori",
        KonsultasiFilter,
        "tanggal_kunjungan",
    )

    search_fields = (
        "nomor_kunjungan",
        "id_tamu__nama",
        "id_tamu__instansi_perusahaan",
        "id_tamu__email",
        "id_petugas__nama_petugas",
    )

    # Base readonly fields (tanggal_kunjungan akan dynamic)
    readonly_fields = (
        "nomor_kunjungan",
        "waktu_selesai",
        "preview_foto",
        "preview_ttd_tamu",
    )
    
    def get_readonly_fields(self, request, obj=None):
        """
        Dynamic readonly fields:
        - Nomor kunjungan: selalu readonly (auto-generated)
        - Tanggal kunjungan: readonly jika sudah selesai
        - Waktu selesai: selalu readonly (auto-set)
        """
        ro = list(self.readonly_fields)
        
        # Jika kunjungan sudah selesai, lock tanggal
        if obj and obj.status_selesai:
            ro.append("tanggal_kunjungan")
            ro.append("id_tamu")
            ro.append("id_tipe")
            ro.append("id_kategori")
            ro.append("id_jenis")
        
        return ro

    autocomplete_fields = [
        "id_tamu",
        "id_jenis",
        "id_petugas",
    ]

    list_per_page = 50
    date_hierarchy = "tanggal_kunjungan"
    ordering = ("-tanggal_kunjungan", "-id_kunjungan")

    # ===== FIELDSETS =====
    def get_fieldsets(self, request, obj=None):
        """Dynamic fieldsets berdasarkan kategori"""
        
        # Fieldset dasar
        fieldsets = [
            ("Informasi Kunjungan", {
                "fields": (
                    "nomor_kunjungan",
                    "tanggal_kunjungan",
                    "id_tipe",
                )
            }),
            ("Data Tamu", {
                "fields": (
                    "id_tamu",
                    "foto_tamu",
                    "preview_foto",
                    "ttd_tamu",
                    "preview_ttd_tamu",
                )
            }),
            ("Layanan", {
                "fields": (
                    "id_kategori",
                    "id_jenis",
                )
            }),
        ]

        # Jika sudah ada objek dan kategori konsultasi
        if obj and obj.is_konsultasi:
            fieldsets.append(
                ("Konsultasi", {
                    "fields": (
                        "pertanyaan",
                        "jawaban",
                        "id_media",
                        "id_sumber",
                    ),
                    "classes": ("wide",)
                })
            )
        elif obj:
            # Non-konsultasi, tidak perlu field konsultasi
            pass
        else:
            # Form baru, tampilkan semua (akan di-hide dengan JS jika perlu)
            fieldsets.append(
                ("Konsultasi (Opsional)", {
                    "fields": (
                        "pertanyaan",
                        "jawaban",
                        "id_media",
                        "id_sumber",
                    ),
                    "classes": ("collapse",)
                })
            )

        # Fieldset petugas & status
        fieldsets.append(
            ("Pelayanan", {
                "fields": (
                    "id_petugas",
                    "status_selesai",
                    "waktu_selesai",
                )
            })
        )

        return fieldsets

    # ===== CUSTOM DISPLAYS =====
    def nama_tamu(self, obj):
        return format_html(
            '<strong>{}</strong><br><small>{}</small>',
            obj.id_tamu.nama,
            obj.id_tamu.instansi_perusahaan or '-'
        )
    nama_tamu.short_description = "Tamu"

    def tipe_badge(self, obj):
        is_offline = obj.is_offline
        color = "#2196F3" if is_offline else "#FF9800"
        icon = "●" if is_offline else "○"
        return format_html(
            '<span style="color: {}; font-weight: bold;">{} {}</span>',
            color, icon, obj.id_tipe.nama_tipe
        )
    tipe_badge.short_description = "Tipe"

    def kategori_badge(self, obj):
        colors = {
            'konsultasi': '#4CAF50',
            'pendaftaran': '#2196F3',
            'verifikasi': '#2196F3',
            'informasi': '#9E9E9E',
        }
        kategori_lower = obj.id_kategori.nama_kategori.lower()
        color = next((c for k, c in colors.items() if k in kategori_lower), '#000')
        
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">{}</span>',
            color, obj.id_kategori.nama_kategori
        )
    kategori_badge.short_description = "Kategori"

    def jenis_layanan(self, obj):
        return obj.id_jenis.nama_jenis
    jenis_layanan.short_description = "Jenis"

    def petugas_layanan(self, obj):
        if obj.id_petugas:
            return format_html(
                '<span style="color: #4CAF50;">✓ {}</span>',
                obj.id_petugas.nama_petugas
            )
        return format_html('<span style="color: #999;">— Belum dilayani</span>')
    petugas_layanan.short_description = "Petugas"

    def status_badge(self, obj):
        if obj.status_selesai:
            return format_html(
                '<span style="background: #4CAF50; color: white; padding: 5px 10px; border-radius: 3px; font-weight: bold;">✓ SELESAI</span>'
            )
        return format_html(
            '<span style="background: #FF9800; color: white; padding: 5px 10px; border-radius: 3px; font-weight: bold;">⏳ MENUNGGU</span>'
        )
    status_badge.short_description = "Status"

    def preview_foto(self, obj):
        if obj.foto_tamu:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 200px; border: 1px solid #ddd; border-radius: 4px;"/>',
                obj.foto_tamu
            )
        return "-"
    preview_foto.short_description = "Preview Foto"

    def preview_ttd_tamu(self, obj):
        if obj.ttd_tamu:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 100px; border: 1px solid #ddd; border-radius: 4px;"/>',
                obj.ttd_tamu
            )
        return "-"
    preview_ttd_tamu.short_description = "Preview Tanda Tangan"

    # ===== ACTIONS =====
    actions = ['tandai_selesai', 'tandai_menunggu', 'export_laporan']

    @admin.action(description='Tandai sebagai SELESAI')
    def tandai_selesai(self, request, queryset):
        """Bulk action untuk menyelesaikan kunjungan non-konsultasi"""
        # Hanya untuk non-konsultasi yang belum selesai
        non_konsultasi = queryset.filter(
            status_selesai=False
        ).exclude(
            id_kategori__nama_kategori__icontains='konsultasi'
        )
        
        updated = non_konsultasi.update(
            status_selesai=True,
            waktu_selesai=timezone.now()
        )
        
        self.message_user(
            request,
            f"{updated} kunjungan berhasil ditandai selesai."
        )

    @admin.action(description='Tandai sebagai MENUNGGU')
    def tandai_menunggu(self, request, queryset):
        """Bulk action untuk reset status"""
        updated = queryset.update(
            status_selesai=False,
            waktu_selesai=None
        )
        
        self.message_user(
            request,
            f"{updated} kunjungan berhasil direset ke status menunggu."
        )

    @admin.action(description='Export Laporan (CSV)')
    def export_laporan(self, request, queryset):
        """Export data kunjungan ke CSV"""
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="laporan_kunjungan.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Nomor', 'Tanggal', 'Tamu', 'Instansi', 
            'Tipe', 'Kategori', 'Jenis', 'Status',
            'Petugas', 'Waktu Selesai'
        ])
        
        for obj in queryset:
            writer.writerow([
                obj.nomor_kunjungan,
                obj.tanggal_kunjungan,
                obj.id_tamu.nama,
                obj.id_tamu.instansi_perusahaan,
                obj.id_tipe.nama_tipe,
                obj.id_kategori.nama_kategori,
                obj.id_jenis.nama_jenis,
                'Selesai' if obj.status_selesai else 'Menunggu',
                obj.id_petugas.nama_petugas if obj.id_petugas else '-',
                obj.waktu_selesai.strftime('%Y-%m-%d %H:%M:%S') if obj.waktu_selesai else '-',
            ])
        
        return response

    # ===== QUERYSET OPTIMIZATION =====
    def get_queryset(self, request):
        """Optimize queries dengan select_related"""
        qs = super().get_queryset(request)
        return qs.select_related(
            'id_tamu',
            'id_tipe',
            'id_kategori',
            'id_jenis',
            'id_media',
            'id_sumber',
            'id_petugas',
        )


# ===== ADMIN SITE CUSTOMIZATION =====
admin.site.site_header = "LPSE Buku Tamu Administration"
admin.site.site_title = "LPSE Admin"
admin.site.index_title = "Manajemen Data Buku Tamu"