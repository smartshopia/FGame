from django.db import models
from decimal import Decimal
from django.conf import settings

class CryptoToken(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)
    price_usd = models.DecimalField(max_digits=30, decimal_places=8, default=Decimal('1.0'))
    volatility = models.FloatField(default=0.02)  # base volatility

    def __str__(self):
        return self.symbol

class Resource(models.Model):
    """
    Types of resources that can be mined.
    """
    name = models.CharField(max_length=50)
    base_value_usd = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('1.0'))

    def __str__(self):
        return self.name

class Holding(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='holdings')
    asset_symbol = models.CharField(max_length=10)
    quantity = models.DecimalField(max_digits=30, decimal_places=8, default=Decimal('0'))
    avg_price = models.DecimalField(max_digits=30, decimal_places=8, default=Decimal('0'))

    class Meta:
        unique_together = ('user', 'asset_symbol')

    def __str__(self):
        return f"{self.user.username} holds {self.quantity} {self.asset_symbol}"

class Order(models.Model):
    SIDE = (('buy','buy'),('sell','sell'))
    STATUS = (('open','open'),('filled','filled'),('cancelled','cancelled'))

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    asset_symbol = models.CharField(max_length=10)
    side = models.CharField(max_length=4, choices=SIDE)
    price = models.DecimalField(max_digits=30, decimal_places=8)
    quantity = models.DecimalField(max_digits=30, decimal_places=8)
    remaining = models.DecimalField(max_digits=30, decimal_places=8)
    status = models.CharField(max_length=12, choices=STATUS, default='open')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} {self.side} {self.quantity} {self.asset_symbol} @ {self.price}"

class Trade(models.Model):
    buy_order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, related_name='buy_trades')
    sell_order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, related_name='sell_trades')
    asset_symbol = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=30, decimal_places=8)
    quantity = models.DecimalField(max_digits=30, decimal_places=8)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Trade {self.quantity} {self.asset_symbol} @ {self.price}"
