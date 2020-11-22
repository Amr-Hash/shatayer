from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid

# Create your models here.

class Country(models.Model):
    uuid = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

class City(models.Model):
    uuid = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

class Area(models.Model):
    uuid = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    lat = models.FloatField(validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)])
    lon = models.FloatField(validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)])
    
    def __str__(self):
        return self.name
    
    # class Meta:
    #     unique_together = [['name','city']]
    
class Zone(models.Model):
    uuid = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=200)
    area = models.ForeignKey(Area, on_delete=models.PROTECT)
    lat = models.FloatField(validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)])
    lon = models.FloatField(validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)])
    
    def __str__(self):
        return self.name
    
    # class Meta:
    #     unique_together = [['name','area']]

