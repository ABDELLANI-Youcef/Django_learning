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
from rest_framework import status
from rest_framework.decorators import api_view, APIView, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from datetime import datetime

# Others
import json
import random

# Custom Imports
from api import serializer as api_serializer
from api import models as api_models

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

class CategoryListAPIView(generics.ListCreateAPIView):
  serializer_class = api_serializer.CategorySerializer
  permission_classes = [AllowAny]

  def get_queryset(self): # type: ignore
    return api_models.Category.objects.all()

class PostCategoryListAPIView(generics.ListCreateAPIView):
  def get_serializer_class(self): # type: ignore
    return api_serializer.PostSerializerPost if self.request.method == 'POST' else api_serializer.PostSerializerGet
  permission_classes = [AllowAny]

  def get_queryset(self): # type: ignore
    category_slug = self.kwargs['category_slug']
    category = api_models.Category.objects.get(slug = category_slug)
    return api_models.Post.objects.filter(category = category, status = "Active")

class PostListAPIView(generics.ListCreateAPIView):
  serializer_class = api_serializer.PostSerializerGet
  permission_classes = [AllowAny]
  def get_queryset(self):  # type: ignore
    posts = api_models.Post.objects.filter(status = 'Active')
    return posts

class PostDetailAPIView(generics.RetrieveAPIView):
    serializer_class = api_serializer.PostSerializerGet
    permission_classes = [AllowAny]
    lookup_field = 'slug'

    def get_queryset(self):# type: ignore
        return api_models.Post.objects.filter(status="Active")

    def get_object(self):
        obj = super().get_object()
        obj.view += 1
        obj.save()
        return obj