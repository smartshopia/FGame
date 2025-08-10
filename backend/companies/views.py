from rest_framework import viewsets, permissions
from .models import Company
from .serializers import CompanySerializer

class CompanyViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CompanySerializer

    def get_queryset(self):
        return Company.objects.all()

    def perform_create(self, serializer):
        # Charge registration fee or validations can be added here later
        serializer.save(owner=self.request.user)
