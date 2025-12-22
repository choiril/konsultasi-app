from django.db import models
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta


# ===== TAMU MANAGER =====

class TamuQuerySet(models.QuerySet):
    """Custom queryset untuk Tamu - minimal & focused"""
    
    def with_kunjungan_count(self):
        """Annotate dengan jumlah kunjungan"""
        return self.annotate(total_kunjungan=Count('kunjungan'))
    
    def search(self, query):
        """
        Search tamu by nama, email, instansi, atau no_hp
        
        Usage:
            Tamu.objects.search("PT Example")
        """
        if not query:
            return self
        return self.filter(
            Q(nama__icontains=query) |
            Q(email__icontains=query) |
            Q(no_hp__icontains=query) |
            Q(instansi_perusahaan__icontains=query)
        )


class TamuManager(models.Manager):
    """Custom manager untuk Tamu"""
    
    def get_queryset(self):
        return TamuQuerySet(self.model, using=self._db)
    
    def with_kunjungan_count(self):
        return self.get_queryset().with_kunjungan_count()
    
    def search(self, query):
        return self.get_queryset().search(query)


# ===== PETUGAS MANAGER =====

class PetugasQuerySet(models.QuerySet):
    """Custom queryset untuk Petugas - minimal & focused"""
    
    def active(self):
        """Petugas yang aktif"""
        return self.filter(is_active=True)
    
    def inactive(self):
        """Petugas yang tidak aktif"""
        return self.filter(is_active=False)
    
    def with_stats(self):
        """
        Annotate dengan statistik dasar
        
        NOTE: Complex statistics moved to services/statistics.py
        This is just basic counts for list display
        """
        return self.annotate(
            total_layanan=Count('kunjungan'),
            layanan_selesai=Count(
                'kunjungan',
                filter=Q(kunjungan__status_selesai=True)
            )
        )


class PetugasManager(models.Manager):
    """Custom manager untuk Petugas"""
    
    def get_queryset(self):
        return PetugasQuerySet(self.model, using=self._db)
    
    def active(self):
        return self.get_queryset().active()
    
    def inactive(self):
        return self.get_queryset().inactive()
    
    def with_stats(self):
        return self.get_queryset().with_stats()


# ===== KUNJUNGAN MANAGER =====

class KunjunganQuerySet(models.QuerySet):
    """
    Custom queryset untuk Kunjungan
    
    DESIGN PRINCIPLES:
    - Only frequently used filters (3+ places)
    - Simple, chain-able methods
    - NO complex calculations (use services/)
    - NO actions/updates (use services/)
    - Focus on READING data efficiently
    """
    
    # ===== STATUS FILTERS (Core Business Logic) =====
    
    def pending(self):
        """Kunjungan yang belum selesai"""
        return self.filter(status_selesai=False)
    
    def completed(self):
        """Kunjungan yang sudah selesai"""
        return self.filter(status_selesai=True)
    
    # ===== TIME-BASED FILTERS (Frequently Used) =====
    
    def today(self):
        """Kunjungan hari ini"""
        return self.filter(tanggal_kunjungan=timezone.now().date())
    
    def this_week(self):
        """Kunjungan minggu ini"""
        today = timezone.now().date()
        start_week = today - timedelta(days=today.weekday())
        return self.filter(tanggal_kunjungan__gte=start_week)
    
    def this_month(self):
        """Kunjungan bulan ini"""
        now = timezone.now()
        return self.filter(
            tanggal_kunjungan__year=now.year,
            tanggal_kunjungan__month=now.month
        )
    
    def by_date_range(self, start_date, end_date):
        """
        Kunjungan dalam rentang tanggal
        
        Usage:
            Kunjungan.objects.by_date_range(date(2025,12,1), date(2025,12,31))
        """
        return self.filter(
            tanggal_kunjungan__gte=start_date,
            tanggal_kunjungan__lte=end_date
        )
    
    def by_month(self, year, month):
        """
        Kunjungan per bulan tertentu
        
        Usage:
            Kunjungan.objects.by_month(2025, 12)
        """
        return self.filter(
            tanggal_kunjungan__year=year,
            tanggal_kunjungan__month=month
        )
    
    # ===== KATEGORI FILTERS (Business Logic) =====
    
    def konsultasi(self):
        """
        Kunjungan kategori konsultasi
        
        TODO(HIGH): Update when is_konsultasi flag is added to KategoriLayanan
        Current: String-based check (fragile!)
        Future: filter(id_kategori__is_konsultasi=True)
        """
        return self.filter(
            id_kategori__nama_kategori__icontains='konsultasi'
        )
    
    def pendaftaran(self):
        """
        Kunjungan kategori pendaftaran/verifikasi
        
        TODO(MEDIUM): Update to use slug or flag
        """
        return self.filter(
            Q(id_kategori__nama_kategori__icontains='pendaftaran') |
            Q(id_kategori__nama_kategori__icontains='verifikasi')
        )
    
    def informasi(self):
        """
        Kunjungan kategori informasi
        
        TODO(MEDIUM): Update to use slug or flag
        """
        return self.filter(
            id_kategori__nama_kategori__icontains='informasi'
        )
    
    def by_kategori(self, kategori_id):
        """Filter by kategori ID"""
        return self.filter(id_kategori_id=kategori_id)
    
    def by_jenis(self, jenis_id):
        """Filter by jenis layanan ID"""
        return self.filter(id_jenis_id=jenis_id)
    
    # ===== TIPE FILTERS =====
    
    def offline(self):
        """
        Kunjungan tipe offline
        
        TODO(MEDIUM): Update when slug field added to TipeKunjungan
        """
        return self.filter(id_tipe__nama_tipe__iexact='offline')
    
    def online(self):
        """
        Kunjungan tipe online
        
        TODO(MEDIUM): Update when slug field added to TipeKunjungan
        """
        return self.filter(id_tipe__nama_tipe__iexact='online')
    
    def by_tipe(self, tipe_id):
        """Filter by tipe kunjungan ID"""
        return self.filter(id_tipe_id=tipe_id)
    
    # ===== PETUGAS FILTERS =====
    
    def by_petugas(self, petugas_id):
        """Kunjungan yang dilayani petugas tertentu"""
        return self.filter(id_petugas_id=petugas_id)
    
    def unassigned(self):
        """Kunjungan yang belum ada petugasnya"""
        return self.filter(id_petugas__isnull=True)
    
    def assigned(self):
        """Kunjungan yang sudah ada petugasnya"""
        return self.filter(id_petugas__isnull=False)
    
    # ===== SEARCH =====
    
    def search(self, query):
        """
        Search by nomor, nama tamu, atau instansi
        
        Usage:
            Kunjungan.objects.search("John Doe")
        """
        if not query:
            return self
        return self.filter(
            Q(nomor_kunjungan__icontains=query) |
            Q(id_tamu__nama__icontains=query) |
            Q(id_tamu__instansi_perusahaan__icontains=query) |
            Q(id_tamu__email__icontains=query)
        )
    
    # ===== OPTIMIZED QUERIES (Performance) =====
    
    def with_relations(self):
        """
        Optimize query dengan select_related
        
        CRITICAL: Always use this for list views to avoid N+1 queries
        
        Usage:
            Kunjungan.objects.pending().with_relations()
        """
        return self.select_related(
            'id_tamu',
            'id_tipe',
            'id_kategori',
            'id_jenis',
            'id_media',
            'id_sumber',
            'id_petugas'
        )
    
    def for_list_display(self):
        """
        Query optimized untuk list view
        
        Usage:
            Kunjungan.objects.for_list_display()
        """
        return self.with_relations().order_by('-tanggal_kunjungan', '-id_kunjungan')
    
    def for_admin(self):
        """
        Query optimized untuk admin interface
        
        Usage in admin.py:
            def get_queryset(self, request):
                return Kunjungan.objects.for_admin()
        """
        return self.with_relations()


class KunjunganManager(models.Manager):
    """
    Custom manager untuk Kunjungan
    
    NOTE: Complex operations moved to services/:
    - statistics() -> services/statistics.py
    - reports() -> services/reports.py
    - bulk actions -> services/actions.py
    
    This manager only handles query/filter logic (READ operations)
    """
    
    def get_queryset(self):
        return KunjunganQuerySet(self.model, using=self._db)
    
    # ===== STATUS =====
    
    def pending(self):
        """Belum selesai"""
        return self.get_queryset().pending()
    
    def completed(self):
        """Sudah selesai"""
        return self.get_queryset().completed()
    
    # ===== TIME-BASED =====
    
    def today(self):
        """Hari ini"""
        return self.get_queryset().today()
    
    def this_week(self):
        """Minggu ini"""
        return self.get_queryset().this_week()
    
    def this_month(self):
        """Bulan ini"""
        return self.get_queryset().this_month()
    
    def by_date_range(self, start_date, end_date):
        """Range tanggal"""
        return self.get_queryset().by_date_range(start_date, end_date)
    
    def by_month(self, year, month):
        """Per bulan"""
        return self.get_queryset().by_month(year, month)
    
    # ===== KATEGORI =====
    
    def konsultasi(self):
        """Kategori konsultasi"""
        return self.get_queryset().konsultasi()
    
    def pendaftaran(self):
        """Kategori pendaftaran"""
        return self.get_queryset().pendaftaran()
    
    def informasi(self):
        """Kategori informasi"""
        return self.get_queryset().informasi()
    
    def by_kategori(self, kategori_id):
        """By kategori ID"""
        return self.get_queryset().by_kategori(kategori_id)
    
    def by_jenis(self, jenis_id):
        """By jenis ID"""
        return self.get_queryset().by_jenis(jenis_id)
    
    # ===== TIPE =====
    
    def offline(self):
        """Tipe offline"""
        return self.get_queryset().offline()
    
    def online(self):
        """Tipe online"""
        return self.get_queryset().online()
    
    def by_tipe(self, tipe_id):
        """By tipe ID"""
        return self.get_queryset().by_tipe(tipe_id)
    
    # ===== PETUGAS =====
    
    def by_petugas(self, petugas_id):
        """By petugas ID"""
        return self.get_queryset().by_petugas(petugas_id)
    
    def unassigned(self):
        """Belum ada petugas"""
        return self.get_queryset().unassigned()
    
    def assigned(self):
        """Sudah ada petugas"""
        return self.get_queryset().assigned()
    
    # ===== SEARCH =====
    
    def search(self, query):
        """Search by nomor/nama/instansi"""
        return self.get_queryset().search(query)
    
    # ===== OPTIMIZED =====
    
    def with_relations(self):
        """With select_related"""
        return self.get_queryset().with_relations()
    
    def for_list_display(self):
        """For list views"""
        return self.get_queryset().for_list_display()
    
    def for_admin(self):
        """For admin interface"""
        return self.get_queryset().for_admin()