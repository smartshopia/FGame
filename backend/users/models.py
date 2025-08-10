from django.contrib.auth.models import AbstractUser
from django.db import models
from decimal import Decimal
from django.conf import settings
from market.models import CryptoToken

def user_profile_pic_path(instance, filename):
    return f'profile_pics/user_{instance.id}/{filename}'

class User(AbstractUser):
    profile_pic = models.ImageField(upload_to=user_profile_pic_path, blank=True, null=True)
    balance_usd = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('5000.00'))
    xp = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)
    total_assets_cache = models.DecimalField(max_digits=30, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return self.username

class ShopItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    crypto_token = models.ForeignKey(
        CryptoToken,
        on_delete=models.CASCADE,
        related_name="shop_items"
    )
    price_amount = models.DecimalField(max_digits=30, decimal_places=8, default=Decimal('0.0'))

    def __str__(self):
        return f"{self.name} ({self.price_amount} {self.crypto_token.symbol})"

class InventoryItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="inventory_items")
    shop_item = models.ForeignKey(ShopItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('user', 'shop_item')

    def __str__(self):
        return f"{self.user} - {self.shop_item.name} x{self.quantity}"
