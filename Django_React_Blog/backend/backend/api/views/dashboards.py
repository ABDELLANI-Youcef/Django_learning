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

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
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

class DashboardStatsView(ListAPIView):
  serializer_class = api_serializer.AuthorSerializer
  permission_classes = [AllowAny]
  def get_queryset(self): # type: ignore
    user_id = self.kwargs['user_id']
    user = get_object_or_404(api_models.User, id = user_id)

    views = api_models.Post.objects.filter(user = user).aggregate(view = Sum("view"))['view'] or 0
    posts = api_models.Post.objects.filter(user = user).count()
    likes = api_models.Post.objects.filter(user = user).aggregate(total_likes = Sum('likes'))['total_likes'] or 0
    bookmark = api_models.Bookmark.objects.filter(post__user = user).count()
    return [{
      'views': views,
      'posts': posts,
      'likes': likes,
      'bookmark': bookmark
    }]

  def list(self, request, *args, **kwargs):
    queryset = self.get_queryset()
    serializer = self.get_serializer(queryset, many = True)
    return Response(serializer.data)

class DashboardPostListsView(ListAPIView):
  serializer_class = api_serializer.PostSerializerGet
  permission_classes = [AllowAny]

  def get_queryset(self): # type: ignore
    user_id = self.kwargs["user_id"]
    user = api_models.User.objects.get(id = user_id)
    return api_models.Post.objects.filter(user = user).order_by('-id')

class DashboardCommentListView(ListAPIView):
  serializer_class = api_serializer.CommentSerializerGet
  permission_classes = [AllowAny]

  def get_queryset(self): # type: ignore
    user_id = self.kwargs["user_id"]
    user = api_models.User.objects.get(id = user_id)
    return api_models.Comment.objects.filter(post__user = user)

class DashboardNotificationsListView(ListAPIView):
  serializer_class = api_serializer.NotificationSerializerGet
  permission_classes = [AllowAny]

  def get_queryset(self): # type: ignore
    user_id = self.kwargs['user_id']
    user = api_models.User.objects.get(id = user_id)
    return api_models.Notification.objects.filter(user = user, seen = False)

class DashboardMarkNotiSeenAPIView(APIView):
  def post(self, request):
    noti_id = request.data["noti_id"]
    noti = api_models.Notification.objects.get(id = noti_id)
    noti.seen = True

    noti.save()

    return Response({'message': "Noti marked as seen"}, status= status.HTTP_200_OK)

class DashboardReplyCommentAPIView(APIView):
  def post(self,request):
    comment_id = request.data['comment_id']
    comment = api_models.Comment.objects.get(id = comment_id)
    reply = request.data['reply']

    comment.reply = reply
    comment.save()
    return Response({"message": "Comment was replied"}, status= status.HTTP_201_CREATED)

class DashboardPostCreateAPIView(generics.CreateAPIView):
  serializer_class = api_serializer.PostSerializerPost
  permission_classes = [AllowAny]

  def create(self, request, *args, **kwargs): # type: ignore
    user_id = request.data.get("user_id")
    title = request.data.get("title")
    image = request.data.get("image")
    description = request.data.get("description")
    slug = request.data.get("slug")
    category_id = request.data.get("category_id")
    post_status = request.data.get("post_status")

    user =  get_object_or_404(api_models.User, id = user_id)
    category = get_object_or_404(api_models.Category, id = category_id)

    api_models.Post.objects.create(
      user = user,
      category = category,
      title = title,
      image = image,
      description = description,
      slug = slug,
      status = post_status
    )

    return Response({"message": "Post was created successfully"}, status= status.HTTP_201_CREATED)