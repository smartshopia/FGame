from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import AchievementDefinition, AchievementProgress

User = get_user_model()

class AchievementTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='pass123')
        self.achievement = AchievementDefinition.objects.create(
            key='test_achievement',
            title='Test Achievement',
            description='Complete test achievement',
            threshold=100,
            category='mining',
            tier='bronze'
        )

    def test_progress_creation_and_str(self):
        progress = AchievementProgress.objects.create(user=self.user, achievement=self.achievement, progress=50)
        self.assertEqual(str(progress), f"{self.user.username} - {self.achievement.title} (50)")
        self.assertEqual(progress.progress, 50)
