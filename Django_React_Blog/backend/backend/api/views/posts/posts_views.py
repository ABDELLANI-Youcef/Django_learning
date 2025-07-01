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
from api import serializers as api_serializer
from api import models as api_models
from api.shared import commons


class CategoryListAPIView(commons.ListAPIView):
  serializer_class = api_serializer.CategorySerializer
  permission_classes = [AllowAny]

  def get_queryset(self): # type: ignore
    return api_models.Category.objects.all()

class PostCategoryListAPIView(commons.ListAPIView):
  def get_serializer_class(self): # type: ignore
    return api_serializer.PostSerializerPost if self.request.method == 'POST' else api_serializer.PostSerializerGet
  permission_classes = [AllowAny]

  def get_queryset(self): # type: ignore
    category_slug = self.kwargs['category_slug']
    category = api_models.Category.objects.get(slug = category_slug)
    return api_models.Post.objects.filter(category = category, status = "Active")

class PostListAPIView(commons.ListAPIView):
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

class LikePostAPIView(APIView):
  def post(self, request):
    user_id = request.data['user_id']
    post_id = request.data['post_id']

    user = api_models.User.objects.get(id = user_id)
    post = api_models.Post.objects.get(id = post_id)

    if user in post.likes.all():
      post.likes.remove(user)
      return Response({"message": "Post is disliked"}, status=status.HTTP_200_OK)
    else:
      post.likes.add(user)
      api_models.Notification.objects.create(
        user = post.user,
        post = post,
        type = 'Like'
      )
      return Response({"message": "post is liked"}, status = status.HTTP_201_CREATED)

class PostCommentAPIView(APIView):
  def post(self, request):
    post_id = request.data['post_id']
    name = request.data['name']
    email = request.data['email']
    comment = request.data['comment']

    post = api_models.Post.objects.get(id = post_id)
    api_models.Comment.objects.create(
      post = post,
      name = name,
      email = email,
      comment = comment
    )

    api_models.Notification.objects.create(
      user = post.user,
      post = post,
      type = 'Comment'
    )

    return Response({'message': "comment Sent"}, status = status.HTTP_201_CREATED)

class PostBookmarkAPIView(APIView):
  def post(self, request):
    post_id = request.data['post_id']
    user_id = request.data['user_id']

    post = api_models.Post.objects.get(id = post_id)
    user = api_models.User.objects.get(id = user_id)
    bookmark = api_models.Bookmark.objects.filter(user = user, post = post).first()

    if bookmark:
      bookmark.delete()
      return Response({"message": "Post is Un-bookmarked"}, status = status.HTTP_200_OK)
    else:
      api_models.Bookmark.objects.create(post = post, user = user)
      api_models.Notification.objects.create(
        post = post,
        user = user,
        type = "Bookmark"
      )
      return Response({"message": "Post is Bookmarked"}, status=status.HTTP_204_NO_CONTENT)