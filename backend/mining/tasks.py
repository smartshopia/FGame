from celery import shared_task
from .models import MiningJob
from django.utils import timezone
from decimal import Decimal
import random

@shared_task
def complete_mining_job(job_id):
    try:
        job = MiningJob.objects.get(id=job_id)
        if job.status != MiningJob.STATUS_PENDING:
            return "Job already processed"

        job.status = MiningJob.STATUS_RUNNING
        job.save()

        # Simulate mining logic
        base_yield = job.rig.yield_base
        random_factor = Decimal(random.uniform(0.8, 1.2))
        total_yield = base_yield * random_factor * job.rig.level

        job.yield_amount = total_yield.quantize(Decimal('0.00000001'))
        job.xp_reward = int(total_yield * 100)  # example: XP proportional to yield
        job.coins_reward = job.yield_amount  # same as yield tokens

        job.status = MiningJob.STATUS_COMPLETED
        job.completed_at = timezone.now()
        job.save()

        # TODO: Update user balances, XP, inventories as needed.

        return f"Mining job {job_id} completed successfully"

    except MiningJob.DoesNotExist:
        return f"Mining job {job_id} not found"
