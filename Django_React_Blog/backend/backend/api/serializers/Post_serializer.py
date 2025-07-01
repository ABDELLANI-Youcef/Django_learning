
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework_simplejwt.tokens import Token

from api import models as api_models

class CategorySerializer(serializers.ModelSerializer):
  def get_post_count(self, category):
    return category.posts.count()
  class Meta:
    model = api_models.Category
    fields= ["id", "title", "image", "slug", "post_count"]

class CommentSerializerPost(serializers.ModelSerializer):
  class Meta:
    model= api_models.Comment
    fields = "__all__"
    depth = 0

class CommentSerializerGet(serializers.ModelSerializer):
  class Meta:
    model= api_models.Comment
    fields = "__all__"
    depth = 3

class PostSerializerPost(serializers.ModelSerializer):
  class Meta:
    model= api_models.Post
    fields = "__all__"
    depth = 0

class PostSerializerGet(serializers.ModelSerializer):
  class Meta:
    model= api_models.Post
    fields = "__all__"
    depth = 3