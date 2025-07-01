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

@extend_schema(
  tags=['Dashboard'],
    request=api_serializer.PostSerializerPost,
    responses={
        201: OpenApiTypes.OBJECT,
        400: OpenApiTypes.OBJECT
    },
    examples=[
        OpenApiExample(
            'Example request',
            value={
                "user_id": 1,
                "title": "Sample Post",
                "image": "string",  # or actual base64 image
                "description": "Post content",
                "slug": "sample-post-xy",  # optional
                "category_id": 1,
                "post_status": "Active"
            },
            request_only=True
        ),
        OpenApiExample(
            'Success response',
            value={"message": "Post was created successfully"},
            response_only=True
        )
    ],
    description='''
    Creates a new blog post.
    Required fields: user_id, title, category_id.
    Slug will be auto-generated if not provided.
    '''
)
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

class DashboardPostEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = api_serializer.PostSerializerPost
    permission_classes = [AllowAny]

    def get_object(self): # type: ignore
      post_id = self.kwargs['post_id']
      return get_object_or_404(api_models.Post, id=post_id)

    def update(self, request, *args, **kwargs):
      instance = self.get_object()

      # Handle category update (if provided)
      if 'category_id' in request.data:
        category = get_object_or_404(api_models.Category, id=request.data['category_id'])
        instance.category = category

      # Handle other fields
      if 'title' in request.data:
        instance.title = request.data['title']

      if 'description' in request.data:
        instance.description = request.data['description']

      if 'image' in request.data and request.data['image'] != "undefined":
        instance.image = request.data['image']

      if 'post_status' in request.data:
        instance.status = request.data['post_status']

      instance.save()
      return Response({"message": 'Post was edited successfully'}, status=status.HTTP_200_OK)
