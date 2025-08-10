from django.db import models
from django.conf import settings
from decimal import Decimal

class AchievementDefinition(models.Model):
    key = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    threshold = models.DecimalField(max_digits=30, decimal_places=8, default=Decimal('0'))
    category = models.CharField(max_length=50, default='general')
    tier = models.CharField(max_length=20, default='bronze')  # e.g., bronze, silver, gold

    def __str__(self):
        return self.title


class AchievementProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='achievement_progress')
    achievement = models.ForeignKey(AchievementDefinition, on_delete=models.CASCADE)
    progress = models.DecimalField(max_digits=30, decimal_places=8, default=Decimal('0'))
    unlocked_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'achievement')

    def __str__(self):
        return f"{self.user.username} - {self.achievement.title} ({self.progress})"
