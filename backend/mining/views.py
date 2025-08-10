from rest_framework import viewsets, permissions
from .models import OwnedRig, MiningJob
from .serializers import OwnedRigSerializer, MiningJobSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from .tasks import complete_mining_job

class OwnedRigViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OwnedRigSerializer

    def get_queryset(self):
        return OwnedRig.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class MiningJobViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MiningJobSerializer

    def get_queryset(self):
        return MiningJob.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        mining_job = serializer.save(user=self.request.user, status='pending')
        # Start async mining task
        complete_mining_job.delay(mining_job.id)
