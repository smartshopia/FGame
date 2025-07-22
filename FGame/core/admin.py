from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.

admin.site.site_header = "FGame Admin"
admin.site.site_title = "FGame Admin Portal"
admin.site.index_title = "Welcome to FGame Admin Portal"
admin.site.register(User, UserAdmin)

admin.site.register(Resource)
admin.site.register(Tool)
admin.site.register(Inventory)
admin.site.register(UserTool)
admin.site.register(MiningCooldown)