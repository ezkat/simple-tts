from django.db import transaction
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import ConversionRequest
from .serializers import ConversionRequestSerializer



class ConversionRequestViewSet(viewsets.ModelViewSet):
    serializer_class = ConversionRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('status', )

    def get_queryset(self):
        queryset = ConversionRequest.objects.filter(user=self.request.user)
        return queryset
    
    @transaction.atomic
    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user, status=ConversionRequest.PENDING)
        return instance
    
    @transaction.atomic
    def perform_update(self, serializer):
        instance = serializer.save(user=self.request.user, status=ConversionRequest.PENDING)
        return instance
