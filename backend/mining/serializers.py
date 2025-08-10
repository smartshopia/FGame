from rest_framework import serializers
from .models import OwnedRig, MiningJob

class OwnedRigSerializer(serializers.ModelSerializer):
    class Meta:
        model = OwnedRig
        fields = ['id', 'user', 'name', 'level', 'passive_rate', 'mine_duration', 'yield_base', 'created_at']
        read_only_fields = ['user', 'created_at']

class MiningJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = MiningJob
        fields = ['id', 'user', 'rig', 'resource', 'started_at', 'status', 'yield_amount', 'xp_reward', 'coins_reward', 'completed_at']
        read_only_fields = ['user', 'started_at', 'status', 'yield_amount', 'xp_reward', 'coins_reward', 'completed_at']
