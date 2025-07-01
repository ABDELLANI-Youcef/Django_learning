'''
  class MyTokenObtainPairSerializer(TokenObtainPairSerializer):: This line creates a new token serializer called MyTokenObtainPairSerializer that is based on an existing one called TokenObtainPairSerializer. Think of it as customizing the way tokens work.
  @classmethod: This line indicates that the following function is a class method, which means it belongs to the class itself and not to an instance (object) of the class.
  def get_token(cls, user):: This is a function (or method) that gets called when we want to create a token for a user. The user is the person who's trying to access something on the website.
  token = super().get_token(user): Here, it's asking for a regular token from the original token serializer (the one it's based on). This regular token is like a key to enter the website.
  token['full_name'] = user.full_name, token['email'] = user.email, token['username'] = user.username: This code is customizing the token by adding extra information to it. For example, it's putting the user's full name, email, and username into the token. These are like special notes attached to the key.
  return token: Finally, the customized token is given back to the user. Now, when this token is used, it not only lets the user in but also carries their full name, email, and username as extra information, which the website can use as needed.
'''
from rest_framework import serializers

from api import models as api_models
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