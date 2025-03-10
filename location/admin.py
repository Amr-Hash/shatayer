from django.contrib import admin
from .models import Country, City, Area, Zone
from modeltranslation.admin import TranslationAdmin

# Register your models here.

@admin.register(Country)
class CountryAdmin(TranslationAdmin):
    fields = ['uuid','name']
    pass

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    pass

@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    pass
