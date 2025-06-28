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
  path('post/category/posts/<category_slug>/', api_view.PostCategoryListAPIView.as_view())
]