from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from crm_integration.serializers import PreSignUpSerializer
from crm_integration.models import PreSignUp


@swagger_auto_schema(
    tags=["PreSignUp"],
)
class PreSignUpApiView(viewsets.ModelViewSet):
    serializer_class = PreSignUpSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PreSignUp.objects.all()
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)