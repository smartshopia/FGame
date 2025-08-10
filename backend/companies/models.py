from django.db import models
from django.conf import settings
from decimal import Decimal

class Company(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='companies')
    name = models.CharField(max_length=200)
    symbol = models.CharField(max_length=10, unique=True)
    shares_total = models.BigIntegerField(default=1_000_000)
    shares_available = models.BigIntegerField(default=500_000)
    valuation = models.DecimalField(max_digits=30, decimal_places=2, default=Decimal('10000.00'))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.symbol})"
