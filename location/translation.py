from modeltranslation.translator import register, TranslationOptions
from .models import Country, City, Area, Zone

@register(Country)
class CountryTranslationOptions(TranslationOptions):
    fields = ('name', )
    required_languages = ('en', 'ar')

@register(City)
class CityTranslationOptions(TranslationOptions):
    fields = ('name', )
    required_languages = ('en', 'ar')

@register(Area)
class AreaTranslationOptions(TranslationOptions):
    fields = ('name', )
    required_languages = ('en', 'ar')

@register(Zone)
class ZoneTranslationOptions(TranslationOptions):
    fields = ('name', )
    required_languages = ('en', 'ar')
