from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, ShopItem, InventoryItem

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('profile_pic', 'balance_usd', 'xp', 'level', 'total_assets_cache')}),
    )
    list_display = ('username', 'email', 'level', 'balance_usd', 'xp')

@admin.register(ShopItem)
class ShopItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'crypto_token', 'price_amount')

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'shop_item', 'quantity')
