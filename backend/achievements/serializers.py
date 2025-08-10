from rest_framework import serializers
from .models import AchievementDefinition, AchievementProgress

class AchievementDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AchievementDefinition
        fields = ['id', 'key', 'title', 'description', 'threshold', 'category', 'tier']

class AchievementProgressSerializer(serializers.ModelSerializer):
    achievement = AchievementDefinitionSerializer(read_only=True)

    class Meta:
        model = AchievementProgress
        fields = ['id', 'achievement', 'progress', 'unlocked_at']
