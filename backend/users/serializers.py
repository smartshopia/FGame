from rest_framework import serializers
from .models import User, ShopItem, InventoryItem

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile_pic', 'balance_usd', 'xp', 'level', 'total_assets_cache']

class ShopItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopItem
        fields = ['id', 'name', 'description', 'crypto_token', 'price_amount']

class InventoryItemSerializer(serializers.ModelSerializer):
    shop_item = ShopItemSerializer(read_only=True)

    class Meta:
        model = InventoryItem
        fields = ['id', 'shop_item', 'quantity']
