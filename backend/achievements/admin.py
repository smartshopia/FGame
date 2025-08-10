from django.contrib import admin
from .models import AchievementDefinition, AchievementProgress

@admin.register(AchievementDefinition)
class AchievementDefinitionAdmin(admin.ModelAdmin):
    list_display = ('key', 'title', 'category', 'tier', 'threshold')

@admin.register(AchievementProgress)
class AchievementProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'achievement', 'progress', 'unlocked_at')
