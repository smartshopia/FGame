from rest_framework import serializers
from .models import Company

class CompanySerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Company
        fields = ['id', 'owner', 'owner_username', 'name', 'symbol', 'shares_total', 'shares_available', 'valuation', 'created_at']
        read_only_fields = ['owner', 'created_at']
