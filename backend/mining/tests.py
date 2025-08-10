from django.test import TestCase
from .models import OwnedRig, MiningJob
from django.contrib.auth import get_user_model
from decimal import Decimal
from market.models import Resource

User = get_user_model()

class MiningModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='pass')
        self.resource = Resource.objects.create(name='Bitcoin', base_value_usd=Decimal('20000'))
        self.rig = OwnedRig.objects.create(user=self.user, name='Basic Rig', level=1)

    def test_mining_job_creation(self):
        job = MiningJob.objects.create(user=self.user, rig=self.rig, resource=self.resource)
        self.assertEqual(job.status, 'pending')
        self.assertEqual(job.user, self.user)
        self.assertEqual(str(job), f"{self.user.username} - job {job.id} ({job.status})")
