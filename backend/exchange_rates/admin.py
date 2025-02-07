from django.contrib import admin
from exchange_rates.models import ExchangeRate
from buho_backend.admin import BaseAdmin

# Register your models here.
@admin.register(ExchangeRate)
class ExchangeRateAdmin(BaseAdmin):
    list_display = ['id', 'exchange_from', 'exchange_to', 'exchange_date', 'last_updated']
    search_fields = ['exchange_from', 'exchange_to']
