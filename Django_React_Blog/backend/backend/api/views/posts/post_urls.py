from django.urls import path
from . import posts_views as api_view

urlpatterns = [
  path('category/list/', api_view.CategoryListAPIView.as_view()),
  path('category/posts/<category_slug>/', api_view.PostCategoryListAPIView.as_view()),
  path('list/', api_view.PostListAPIView.as_view()),
  path('detail/<slug>/', api_view.PostDetailAPIView.as_view()),
  path('post-like/', api_view.LikePostAPIView.as_view()),
  path('comment-post/', api_view.PostCommentAPIView.as_view()),
  path('bookmark-post/', api_view.PostBookmarkAPIView.as_view())
]