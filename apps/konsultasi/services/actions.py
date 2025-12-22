"""
Business Actions untuk Kunjungan

Handles:
- Complete kunjungan (with business rules)
- Auto-set media tatap muka
- Bulk operations
- Status changes
"""

from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError


class KunjunganService:
    """
    Service class untuk business operations pada Kunjungan
    
    Usage:
        from apps.konsultasi.services import KunjunganService
        
        service = KunjunganService()
        service.complete_konsultasi(kunjungan, petugas, data)
    """
    
    @transaction.atomic
    def complete_konsultasi(self, kunjungan, petugas, jawaban, id_media=None, id_sumber=None):
        """
        Complete konsultasi dengan business rules
        
        Business Rules:
        1. Jika offline -> auto-set media "Tatap Muka"
        2. Validasi jawaban, media, sumber wajib diisi
        3. Set petugas & waktu selesai
        
        Args:
            kunjungan: Kunjungan instance
            petugas: Petugas instance
            jawaban: str - jawaban konsultasi
            id_media: MediaKonsultasi instance (optional for offline)
            id_sumber: SumberJawaban instance
        
        Returns:
            Kunjungan instance yang sudah completed
        
        Raises:
            ValidationError: Jika data tidak valid
        """
        # Import di dalam method untuk avoid circular import
        from apps.konsultasi.models import MediaKonsultasi
        
        # Validasi: harus konsultasi
        if not kunjungan.is_konsultasi:
            raise ValidationError("Kunjungan ini bukan kategori konsultasi")
        
        # Validasi: belum selesai
        if kunjungan.status_selesai:
            raise ValidationError("Kunjungan sudah selesai")
        
        # Business Rule: Set jawaban
        if not jawaban:
            raise ValidationError("Jawaban wajib diisi untuk konsultasi")
        kunjungan.jawaban = jawaban
        
        # Business Rule: Auto-set media "Tatap Muka" untuk offline
        if kunjungan.is_offline and not id_media:
            try:
                # TODO(HIGH): Replace string lookup with slug/constant
                tatap_muka = MediaKonsultasi.objects.get(
                    nama_media__iexact='tatap muka'
                )
                id_media = tatap_muka
            except MediaKonsultasi.DoesNotExist:
                raise ValidationError(
                    "Media 'Tatap Muka' tidak ditemukan di database. "
                    "Silakan pilih media secara manual."
                )
        
        # Validasi: media wajib diisi
        if not id_media:
            raise ValidationError("Media konsultasi wajib dipilih")
        kunjungan.id_media = id_media
        
        # Validasi: sumber wajib diisi
        if not id_sumber:
            raise ValidationError("Sumber jawaban wajib dipilih")
        kunjungan.id_sumber = id_sumber
        
        # Set petugas dan status selesai
        kunjungan.id_petugas = petugas
        kunjungan.status_selesai = True
        
        # Save (waktu_selesai auto-set by model)
        kunjungan.save()
        
        return kunjungan
    
    @transaction.atomic
    def complete_non_konsultasi(self, kunjungan, petugas):
        """
        Complete kunjungan non-konsultasi
        
        Business Rules:
        - Hanya set status & petugas
        - Tidak perlu jawaban/media/sumber
        
        Args:
            kunjungan: Kunjungan instance
            petugas: Petugas instance
        
        Returns:
            Kunjungan instance yang sudah completed
        """
        # Validasi: bukan konsultasi
        if kunjungan.is_konsultasi:
            raise ValidationError(
                "Gunakan complete_konsultasi() untuk kategori konsultasi"
            )
        
        # Validasi: belum selesai
        if kunjungan.status_selesai:
            raise ValidationError("Kunjungan sudah selesai")
        
        # Set petugas dan status
        kunjungan.id_petugas = petugas
        kunjungan.status_selesai = True
        kunjungan.save()
        
        return kunjungan
    
    @transaction.atomic
    def bulk_complete_non_konsultasi(self, queryset, petugas):
        """
        Bulk complete untuk non-konsultasi
        
        Business Rules:
        - Hanya untuk non-konsultasi
        - Set status & petugas
        - Skip validation untuk performa
        
        Args:
            queryset: QuerySet of Kunjungan
            petugas: Petugas instance
        
        Returns:
            int: Jumlah kunjungan yang di-update
        """
        # Filter hanya non-konsultasi yang pending
        valid_queryset = queryset.exclude(
            id_kategori__nama_kategori__icontains='konsultasi'
        ).filter(status_selesai=False)
        
        # Bulk update (skip validation untuk performa)
        updated = valid_queryset.update(
            id_petugas=petugas,
            status_selesai=True,
            waktu_selesai=timezone.now()
        )
        
        return updated
    
    @transaction.atomic
    def reset_to_pending(self, kunjungan):
        """
        Reset kunjungan ke status pending
        
        Business Rules:
        - Clear status_selesai & waktu_selesai
        - Keep other data intact
        
        Args:
            kunjungan: Kunjungan instance
        
        Returns:
            Kunjungan instance
        """
        kunjungan.status_selesai = False
        kunjungan.waktu_selesai = None
        kunjungan.save(skip_validation=True)
        
        return kunjungan