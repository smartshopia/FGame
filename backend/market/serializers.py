from rest_framework import serializers
from .models import CryptoToken, Holding, Order, Trade

class CryptoTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoToken
        fields = ['id', 'symbol', 'name', 'price_usd', 'volatility']

class HoldingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Holding
        fields = ['id', 'user', 'asset_symbol', 'quantity', 'avg_price']
        read_only_fields = ['user']

class OrderSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Order
        fields = ['id', 'user', 'user_username', 'asset_symbol', 'side', 'price', 'quantity', 'remaining', 'status', 'created_at']
        read_only_fields = ['user', 'remaining', 'status', 'created_at']

class TradeSerializer(serializers.ModelSerializer):
    buy_order_id = serializers.ReadOnlyField(source='buy_order.id')
    sell_order_id = serializers.ReadOnlyField(source='sell_order.id')

    class Meta:
        model = Trade
        fields = ['id', 'buy_order_id', 'sell_order_id', 'asset_symbol', 'price', 'quantity', 'timestamp']
