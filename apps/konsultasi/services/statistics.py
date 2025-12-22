from django.db.models import Count, Q, Avg
from django.utils import timezone

from apps.konsultasi.models import Kunjungan


class KunjunganStatistics:
    """
    Service class untuk statistics dan aggregations
    
    Usage:
        from bukutamu.services import KunjunganStatistics
        
        stats = KunjunganStatistics()
        data = stats.get_dashboard_stats()
    """
    
    def get_dashboard_stats(self):
        """
        Get statistik untuk dashboard
        
        Returns:
            dict: Dictionary berisi statistik umum
        
        Usage:
            stats = KunjunganStatistics()
            data = stats.get_dashboard_stats()
        """
        qs = Kunjungan.objects.all()
        
        return {
            'total': qs.count(),
            'pending': qs.pending().count(),
            'completed': qs.completed().count(),
            'konsultasi': qs.konsultasi().count(),
            'offline': qs.offline().count(),
            'online': qs.online().count(),
            'today': qs.today().count(),
            'this_week': qs.this_week().count(),
            'this_month': qs.this_month().count(),
        }
    
    def get_konsultasi_stats(self):
        """
        Statistik khusus konsultasi
        
        Returns:
            dict: Statistik konsultasi detail
        """
        konsultasi_qs = Kunjungan.objects.konsultasi().completed()
        
        return {
            'total_konsultasi': konsultasi_qs.count(),
            'offline_konsultasi': konsultasi_qs.offline().count(),
            'online_konsultasi': konsultasi_qs.online().count(),
            'by_media': list(
                konsultasi_qs.values('id_media__nama_media')
                .annotate(total=Count('id_kunjungan'))
                .order_by('-total')
            ),
            'by_sumber': list(
                konsultasi_qs.values('id_sumber__nama_sumber')
                .annotate(total=Count('id_kunjungan'))
                .order_by('-total')
            ),
        }
    
    def get_petugas_workload(self):
        """
        Workload per petugas
        
        Returns:
            list: List of dict dengan workload per petugas
        """
        return list(
            Kunjungan.objects.values(
                'id_petugas__nama_petugas'
            ).annotate(
                total_layanan=Count('id_kunjungan'),
                selesai=Count(
                    'id_kunjungan',
                    filter=Q(status_selesai=True)
                ),
                pending=Count(
                    'id_kunjungan',
                    filter=Q(status_selesai=False)
                )
            ).order_by('-total_layanan')
        )