"""
Reports Service untuk Kunjungan

Handles:
- Daily reports
- Monthly reports
- Export to CSV/PDF
"""

from datetime import date
from django.db.models import Count
from django.utils import timezone


class KunjunganReports:
    """
    Service class untuk report generation
    
    Usage:
        from apps.konsultasi.services import KunjunganReports
        
        reports = KunjunganReports()
        data = reports.daily_report(date.today())
    """
    
    def daily_report(self, report_date=None):
        """
        Generate laporan harian
        
        Args:
            report_date: date object (default: today)
        
        Returns:
            dict: Laporan harian lengkap
        """
        from apps.konsultasi.models import Kunjungan
        
        if report_date is None:
            report_date = timezone.now().date()
        
        qs = Kunjungan.objects.filter(
            tanggal_kunjungan=report_date
        ).with_relations()
        
        return {
            'date': report_date,
            'total': qs.count(),
            'pending': qs.pending().count(),
            'completed': qs.completed().count(),
            'konsultasi': qs.konsultasi().count(),
            'offline': qs.offline().count(),
            'online': qs.online().count(),
            'by_kategori': list(
                qs.values('id_kategori__nama_kategori')
                .annotate(total=Count('id_kunjungan'))
            ),
            'by_petugas': list(
                qs.completed().values('id_petugas__nama_petugas')
                .annotate(total=Count('id_kunjungan'))
            ),
        }
    
    def monthly_report(self, year=None, month=None):
        """
        Generate laporan bulanan
        
        Args:
            year: int (default: current year)
            month: int (default: current month)
        
        Returns:
            dict: Laporan bulanan lengkap
        """
        from apps.konsultasi.models import Kunjungan
        
        now = timezone.now()
        year = year or now.year
        month = month or now.month
        
        qs = Kunjungan.objects.by_month(year, month).with_relations()
        
        return {
            'year': year,
            'month': month,
            'total': qs.count(),
            'completed': qs.completed().count(),
            'pending': qs.pending().count(),
            'konsultasi': qs.konsultasi().count(),
            'daily_breakdown': list(
                qs.values('tanggal_kunjungan')
                .annotate(total=Count('id_kunjungan'))
                .order_by('tanggal_kunjungan')
            ),
            'by_kategori': list(
                qs.values('id_kategori__nama_kategori')
                .annotate(total=Count('id_kunjungan'))
                .order_by('-total')
            ),
        }
    
    def export_to_csv_data(self, queryset):
        """
        Prepare data untuk CSV export
        
        Args:
            queryset: QuerySet of Kunjungan
        
        Returns:
            list: List of dicts untuk CSV writer
        """
        data = []
        for obj in queryset.with_relations():
            data.append({
                'Nomor': obj.nomor_kunjungan,
                'Tanggal': obj.tanggal_kunjungan,
                'Tamu': obj.id_tamu.nama,
                'Instansi': obj.id_tamu.instansi_perusahaan,
                'Tipe': obj.id_tipe.nama_tipe,
                'Kategori': obj.id_kategori.nama_kategori,
                'Jenis': obj.id_jenis.nama_jenis,
                'Status': 'Selesai' if obj.status_selesai else 'Menunggu',
                'Petugas': obj.id_petugas.nama_petugas if obj.id_petugas else '-',
                'Waktu Selesai': obj.waktu_selesai.strftime('%Y-%m-%d %H:%M:%S') if obj.waktu_selesai else '-',
            })
        
        return data