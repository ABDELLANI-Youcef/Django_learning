from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.utils.text import slugify
from shortuuid.django_fields import ShortUUIDField
from .user_models import *
import shortuuid

class Category(models.Model):
  title = models.CharField(max_length=100)
  image = models.ImageField(upload_to='image', null=True, blank=True)
  slug = models.SlugField(unique=True, null=True, blank=True)

  def __str__(self):
    return self.title

  def save(self, *args, **kwargs):
    if self.slug == "" or self.slug == None:
      self.slug = slugify(self.title)
    super(Category, self).save(*args, **kwargs)

  class Meta:
      verbose_name_plural = 'Category'

  def post_count(self):
    return Post.objects.filter(category = self).count()

class Post(models.Model):
  STATUS = (
    ("Active", "Active"),
    ("Draft" , "Draft"),
    ("Disabled", "Disabled")
  )

  user = models.ForeignKey(User, on_delete=models.CASCADE)
  profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
  category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
  title = models.CharField(max_length=100)
  description = models.TextField(null=True, blank=True)
  tags = models.CharField(max_length=100, null=True)
  image = models.ImageField(upload_to='image', null=True, blank=True)
  status = models.CharField(choices=STATUS, max_length=100, default="Active")
  view = models.IntegerField(default=0)
  likes = models.ManyToManyField(User, blank=True, related_name='likes_user')
  slug = models.SlugField(unique=True, null=True, blank=True)
  date = models.DateTimeField(auto_now_add=True)

  class Meta:
    verbose_name_plural = "Post"

  def __str__(self):
    return self.title

  def save(self, *args, **kwargs):
    if self.slug == "" or self.slug == None:
      self.slug = slugify(self.title) + " " + shortuuid.uuid()[0:2]
    super(Post, self).save(*args, **kwargs)

  def comments(self):
      return Comment.objects.filter(post=self).order_by("-id")

class Comment(models.Model):
  post = models.ForeignKey(Post, on_delete=models.CASCADE)
  name = models.CharField(max_length=100)
  email = models.EmailField(max_length=100)
  comment = models.TextField()
  reply = models.TextField(null=True, blank=True)
  date = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering = ["-date"]
    verbose_name_plural = "Comment"

  def __str__(self):
    return f"{self.post.title} - {self.name}"

class Bookmark(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  post = models.ForeignKey(Post, on_delete=models.CASCADE)
  date = models.DateTimeField(auto_now_add=True)

  class Meta:
    verbose_name_plural = "Bookmark"

  def __str__(self):
    return f"{self.post.title} - {self.user.username}"

class Notification(models.Model):
  NOTI_TYPE = (
    ("LIKE", "LIKE"),
    ("Comment", "Comment"),
    ("Bookmark", "Bookmark")
  )

  user = models.ForeignKey(User, on_delete=models.CASCADE)
  post = models.ForeignKey(Post, on_delete=models.CASCADE)
  date = models.DateTimeField(auto_now_add=True)
  type = models.CharField(choices=NOTI_TYPE, max_length=100)
  seen = models.BooleanField(default=False)

  class Meta:
    ordering = ["-date"]
    verbose_name_plural = "Notification"

  def __str__(self):
    if self.post:
      return f"{self.post.title} - {self.type}"
    else:
      return "Notification"