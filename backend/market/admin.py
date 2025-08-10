from django.contrib import admin
from .models import CryptoToken, Holding, Order, Trade

admin.site.register(CryptoToken)
admin.site.register(Holding)
admin.site.register(Order)
admin.site.register(Trade)
