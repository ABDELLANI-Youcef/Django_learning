from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.db.models import Sum
# Restframework
from rest_framework import status, mixins, generics
from rest_framework.decorators import api_view, APIView, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from datetime import datetime

# Others
import json
import random

# Custom Imports
from api import serializer as api_serializer
from api import models as api_models

class ListAPIView(mixins.ListModelMixin, generics.GenericAPIView):
  """
  Concrete view for listing a queryset.
  """
  def get(self, request, *args, **kwargs):
    return self.list(request, *args, **kwargs)

class MyTokenObtainPairView(TokenObtainPairView):
  serializer_class = api_serializer.MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
  queryset = api_models.User.objects.all()
  permission_classes = [AllowAny]
  serializer_class = api_serializer.RegisterSerializer

class ProfileView(generics.RetrieveUpdateAPIView):
  permission_classes = [AllowAny]
  serializer_class = api_serializer.ProfileSerializer

  def get_object(self): # type: ignore
    user_id = self.kwargs['user_id']
    user = get_object_or_404(api_models.User, id=user_id)
    profile = get_object_or_404(api_models.Profile, user=user)
    return profile
