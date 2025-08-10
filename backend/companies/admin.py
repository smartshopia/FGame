from django.contrib import admin
from .models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'symbol', 'owner', 'valuation', 'shares_total', 'shares_available', 'created_at']
    search_fields = ['name', 'symbol', 'owner__username']
