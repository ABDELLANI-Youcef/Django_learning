from django.urls import path
from . import views as api_view

urlpatterns = [
  path('post/category/list/', api_view.CategoryListAPIView.as_view()),
  path('post/category/posts/<category_slug>/', api_view.PostCategoryListAPIView.as_view()),
  path('post/list/', api_view.PostListAPIView.as_view()),
  path('post/detail/<slug>/', api_view.PostDetailAPIView.as_view()),
  path('post/post-like/', api_view.LikePostAPIView.as_view()),
  path('post/comment-post/', api_view.PostCommentAPIView.as_view()),
  path('post/bookmark-post/', api_view.PostBookmarkAPIView.as_view())
]