from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import ShopItem, InventoryItem
from market.models import CryptoToken
from decimal import Decimal

User = get_user_model()

class UserModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.crypto = CryptoToken.objects.create(symbol='BTC', name='Bitcoin', price_usd=Decimal('20000'))
        self.shop_item = ShopItem.objects.create(name='Basic Rig', crypto_token=self.crypto, price_amount=Decimal('100'))

    def test_inventory_item_creation(self):
        inventory_item = InventoryItem.objects.create(user=self.user, shop_item=self.shop_item, quantity=2)
        self.assertEqual(str(inventory_item), f"{self.user} - {self.shop_item.name} x2")
