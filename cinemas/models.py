from django.db import models

class CinemaChain(models.Model):
    name = models.CharField(max_length=512)
    code = models.IntegerField(unique=True)

class Cinema(models.Model):
    name = models.CharField(max_length=512)
    code = models.CharField(unique=True, max_length=50)
    address = models.CharField(max_length=512)
    postal_code = models.CharField(max_length=256)
    city = models.CharField(max_length=512)
    area = models.CharField(max_length=256)
    subway = models.CharField(max_length=512)
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)
    screen_count = models.IntegerField(blank=True, null=True)
    has_PRM_access = models.BooleanField(default=False)
    has_event = models.BooleanField(default=False)
    open_to_external_sales = models.BooleanField(default=False)
    chain = models.ForeignKey('CinemaChain', related_name='cinemas', blank=True, null=True)
