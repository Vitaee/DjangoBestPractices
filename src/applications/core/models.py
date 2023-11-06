from django.contrib.gis.db import models
from simple_history.models import HistoricalRecords


class Magaza(models.Model):
    ad = models.CharField(verbose_name="Mağaza Adı", null=True, blank=True, max_length=125)
    enlem = models.FloatField(verbose_name="Mağaza Enlem", null=True, blank=True)
    boylam = models.FloatField(verbose_name="Mağaza Boylam", null=True, blank=True)
    logo = models.TextField(verbose_name="Mağaza Logo", null=True, blank=True, max_length=455)
    location = models.PointField(verbose_name="Mağaza Konumu", null=True, blank=True)
    history = HistoricalRecords()


