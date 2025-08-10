from celery import shared_task
from .models import CryptoToken
import random
from decimal import Decimal

@shared_task
def update_market_prices():
    tokens = CryptoToken.objects.all()
    for token in tokens:
        change_pct = random.uniform(-token.volatility, token.volatility)
        old_price = token.price_usd
        new_price = old_price * Decimal(1 + change_pct)
        token.price_usd = max(new_price, Decimal('0.01'))
        token.save()
