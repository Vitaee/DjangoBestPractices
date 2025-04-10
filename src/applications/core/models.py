from django.contrib.gis.db import models
from simple_history.models import HistoricalRecords
from django.conf import settings


class Magaza(models.Model):
    ad = models.CharField(verbose_name="Mağaza Adı", null=True, blank=True, max_length=125)
    enlem = models.FloatField(verbose_name="Mağaza Enlem", null=True, blank=True)
    boylam = models.FloatField(verbose_name="Mağaza Boylam", null=True, blank=True)
    logo = models.TextField(verbose_name="Mağaza Logo", null=True, blank=True, max_length=455)
    location = models.PointField(verbose_name="Mağaza Konumu", null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='magazas', null=True, verbose_name="Mağaza Sahibi")
    active = models.BooleanField(default=True, verbose_name="Aktif")
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name="Güncellenme Tarihi")
    history = HistoricalRecords()
    
    class Meta:
        verbose_name = "Mağaza"
        verbose_name_plural = "Mağazalar"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['owner', 'active']),
            models.Index(fields=['ad']),
        ]
    
    def __str__(self):
        return self.ad or f"Mağaza {self.id}"


