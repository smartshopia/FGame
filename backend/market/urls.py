from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CryptoTokenViewSet, HoldingViewSet, OrderViewSet, TradeViewSet

router = DefaultRouter()
router.register(r'tokens', CryptoTokenViewSet, basename='token')
router.register(r'holdings', HoldingViewSet, basename='holding')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'trades', TradeViewSet, basename='trade')

urlpatterns = [
    path('', include(router.urls)),
]
