from rest_framework import generics, permissions
from .models import AchievementDefinition, AchievementProgress
from .serializers import AchievementDefinitionSerializer, AchievementProgressSerializer

class AchievementDefinitionListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AchievementDefinitionSerializer
    queryset = AchievementDefinition.objects.all()

class AchievementProgressListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AchievementProgressSerializer

    def get_queryset(self):
        return AchievementProgress.objects.filter(user=self.request.user)
