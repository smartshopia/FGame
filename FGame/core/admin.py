from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.

admin.site.site_header = "FGame Admin"
admin.site.site_title = "FGame Admin Portal"
admin.site.index_title = "Welcome to FGame Admin Portal"
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'

class CustomUserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm

    # Add your fields here
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Game Stats', {
            'fields': ('xp', 'level', 'coins', 'points', 'image'),
        }),
    )

    # Optional: make them searchable and sortable
    list_display = ('username', 'email', 'xp', 'level', 'coins', 'points', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'email')

admin.site.register(User, CustomUserAdmin)

admin.site.register(Resource)
admin.site.register(Tool)
admin.site.register(Inventory)
admin.site.register(UserTool)
admin.site.register(MiningCooldown)