from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ShopItemViewSet, InventoryItemViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'shop-items', ShopItemViewSet, basename='shopitem')
router.register(r'inventory', InventoryItemViewSet, basename='inventoryitem')

urlpatterns = [
    path('', include(router.urls)),
]
