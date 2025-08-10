from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OwnedRigViewSet, MiningJobViewSet

router = DefaultRouter()
router.register(r'rigs', OwnedRigViewSet, basename='ownedrig')
router.register(r'jobs', MiningJobViewSet, basename='miningjob')

urlpatterns = [
    path('', include(router.urls)),
]
