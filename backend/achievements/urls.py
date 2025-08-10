from django.urls import path
from . import views

urlpatterns = [
    path('', views.AchievementDefinitionListView.as_view(), name='achievement-definitions'),
    path('progress/', views.AchievementProgressListView.as_view(), name='achievement-progress'),
]
