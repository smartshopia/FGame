from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Company

User = get_user_model()

class CompanyModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='owner', password='pass123')
        self.company = Company.objects.create(
            owner=self.user,
            name='TestCorp',
            symbol='TST',
            shares_total=1000000,
            shares_available=500000,
            valuation=10000.00
        )

    def test_company_str(self):
        self.assertEqual(str(self.company), "TestCorp (TST)")

    def test_company_owner(self):
        self.assertEqual(self.company.owner.username, 'owner')
