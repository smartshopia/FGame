from django.db import models
from django.conf import settings
from decimal import Decimal
import uuid

User = settings.AUTH_USER_MODEL

class OwnedRig(models.Model):
    """
    A rig instance owned by a user.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rigs')
    name = models.CharField(max_length=100)
    level = models.PositiveIntegerField(default=1)
    passive_rate = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0.000001'))  # token units/sec
    mine_duration = models.PositiveIntegerField(default=30)  # seconds per manual mine
    yield_base = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0.001'))  # base token reward per mine
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.name} (L{self.level})"

class MiningJob(models.Model):
    """
    Tracks a single manual mining run started by a user.
    """
    STATUS_PENDING = 'pending'
    STATUS_RUNNING = 'running'
    STATUS_COMPLETED = 'completed'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_RUNNING, 'Running'),
        (STATUS_COMPLETED, 'Completed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mining_jobs')
    rig = models.ForeignKey(OwnedRig, on_delete=models.CASCADE, related_name='jobs')
    resource = models.ForeignKey('market.Resource', on_delete=models.CASCADE)  # requires market.Resource model
    started_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    yield_amount = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0.0'))
    xp_reward = models.PositiveIntegerField(default=0)
    coins_reward = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0.0'))
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.user.username} - job {self.id} ({self.status})"
