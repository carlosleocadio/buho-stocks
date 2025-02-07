from django.contrib import admin
from markets.models import Market
from buho_backend.admin import BaseAdmin


# Register your models here.
@admin.register(Market)
class MarketAdmin(BaseAdmin):
    list_display = ["id", "name", "last_updated", "date_created"]
    search_fields = ["name"]
