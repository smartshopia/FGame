from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('home')

urlpatterns = [
    path('', home, name='home'),
    path('mine/', mine_view, name='mine'),
    path('inventory/', inventory_view, name='inventory'),
    path('equip/<int:tool_id>/', equip_tool, name='equip_tool'),
    path('shop/', shop_view, name='shop'),
    path('leaderboard/', leaderboard_view, name='leaderboard'),
    # Auth
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup, name='signup'),
]
