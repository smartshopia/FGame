from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta

# Create your models here.
class User(AbstractUser):
    image = models.ImageField(upload_to='profile_pics/', default='default-profile.png')
    xp = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)
    coins = models.PositiveIntegerField(default=0)
    points = models.PositiveIntegerField(default=0)

    def gain_xp(self, amount):
        self.xp += amount
        old_level = self.level
        self.level = self.calculate_level()
        self.save()
        return self.level > old_level  # True if level increased

    def calculate_level(self):
        return (self.xp // 100) + 1

# Resources (e.g., Gold, Iron, Gems)
class Resource(models.Model):
    name = models.CharField(max_length=50)
    value = models.PositiveIntegerField(default=10)  # Sell value per unit

    def __str__(self):
        return self.name

# Tools (e.g., Wooden Pickaxe, Iron Drill)
class Tool(models.Model):
    name = models.CharField(max_length=50)
    power = models.PositiveIntegerField(default=1)  # Affects wait time / reward
    cost = models.PositiveIntegerField(default=100)  # Buy cost

    def __str__(self):
        return self.name

# User Inventory (what user owns)
class Inventory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.resource.name}: {self.quantity}"

# User Tools (what tools user owns and uses)
class UserTool(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE)
    equipped = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.tool.name} {'(Equipped)' if self.equipped else ''}"

# Mining cooldown per user
class MiningCooldown(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    next_mine_time = models.DateTimeField(default=timezone.now)

    def can_mine(self):
        return timezone.now() >= self.next_mine_time

    def set_next_time(self, seconds):
        self.next_mine_time = timezone.now() + timedelta(seconds=seconds)
        self.save()

class Achievement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    xp_reward = models.PositiveIntegerField(default=50)
    coins_reward = models.PositiveIntegerField(default=100)

    def __str__(self):
        return self.name

class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    unlocked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} unlocked {self.achievement.name}"

class LeaderboardEntry(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_xp = models.PositiveIntegerField(default=0)
    total_points = models.PositiveIntegerField(default=0)

    def update_from_user(self):
        self.total_xp = self.user.xp
        self.total_points = self.user.points
        self.save()
