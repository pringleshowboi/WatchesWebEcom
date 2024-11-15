from django.contrib import admin
from .models import Watch

@admin.register(Watch)
class WatchAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'price', 'in_stock', 'created_at')
    search_fields = ('name', 'brand')
    list_filter = ('brand', 'in_stock')
