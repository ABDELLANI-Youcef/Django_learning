from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from api import views as api_view

urlpatterns = [
  path('user/token/', api_view.MyTokenObtainPairView.as_view()),
  path('user/token/refresh/', TokenRefreshView.as_view()),
  path('user/register/', api_view.RegisterView.as_view()),
  path('user/profile/<int:user_id>/', api_view.ProfileView.as_view()),

  # POST Endpoints
  path('post/category/list/', api_view.CategoryListAPIView.as_view()),
  path('post/category/posts/<category_slug>/', api_view.PostCategoryListAPIView.as_view()),
  path('post/list/', api_view.PostListAPIView.as_view()),
  path('post/detail/<slug>/', api_view.PostDetailAPIView.as_view()),
  path('post/post-like/', api_view.LikePostAPIView.as_view()),
  path('post/comment-post/', api_view.PostCommentAPIView.as_view()),
  path('post/bookmark-post/', api_view.PostBookmarkAPIView.as_view())
]