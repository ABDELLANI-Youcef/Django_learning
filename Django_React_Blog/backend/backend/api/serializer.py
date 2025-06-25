'''
  class MyTokenObtainPairSerializer(TokenObtainPairSerializer):: This line creates a new token serializer called MyTokenObtainPairSerializer that is based on an existing one called TokenObtainPairSerializer. Think of it as customizing the way tokens work.
  @classmethod: This line indicates that the following function is a class method, which means it belongs to the class itself and not to an instance (object) of the class.
  def get_token(cls, user):: This is a function (or method) that gets called when we want to create a token for a user. The user is the person who's trying to access something on the website.
  token = super().get_token(user): Here, it's asking for a regular token from the original token serializer (the one it's based on). This regular token is like a key to enter the website.
  token['full_name'] = user.full_name, token['email'] = user.email, token['username'] = user.username: This code is customizing the token by adding extra information to it. For example, it's putting the user's full name, email, and username into the token. These are like special notes attached to the key.
  return token: Finally, the customized token is given back to the user. Now, when this token is used, it not only lets the user in but also carries their full name, email, and username as extra information, which the website can use as needed.
'''

from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework_simplejwt.tokens import Token

from api import models as api_models

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
  @classmethod
  def get_token(cls, user):
    token = super().get_token(user)
    token['full_name'] = user.full_name
    token['email']= user.email
    token['username'] = user.username

    return token

class RegisterSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True, required = True, validators=[validate_password])
  password2 = serializers.CharField(write_only=True, required = True)

  class Meta:
    model: api_models.User
    fields = ['full_name', 'email', 'password', 'password2']

  def validate(self, attrs):
    if attrs['password'] != attrs['password2']:
      raise serializers.ValidationError({'password': "password fields didn't match"})
    return attrs

  def create(self, validated_data):
    user = api_models.User.objects.create(
      full_name = validated_data['full_name'],
      email = validated_data['email']
    )

    email_username , mobile = user.email.split('@')
    user.username = email_username
    user.set_password(validated_data['password'])
    user.save()
    return user

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = api_models.User
    fields = "__all__"

class ProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model= api_models.Profile
    fields = "__all__"

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

class BookmarkSerializerPost(serializers.ModelSerializer):
  class Meta:
    model= api_models.Bookmark
    fields = "__all__"
    depth = 0

class BookmarkSerializerGet(serializers.ModelSerializer):
  class Meta:
    model= api_models.Bookmark
    fields = "__all__"
    depth = 3

class NotificationSerializerPost(serializers.ModelSerializer):
  class Meta:
    model= api_models.Notification
    fields = "__all__"
    depth = 0

class NotificationSerializerGet(serializers.ModelSerializer):
  class Meta:
    model= api_models.Notification
    fields = "__all__"
    depth = 3

class AuthorSerializer(serializers.Serializer):
  views = serializers.IntegerField(default=0)
  posts = serializers.IntegerField(default=0)
  likes = serializers.IntegerField(default=0)
  bookmark = serializers.IntegerField(default=0)