from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import user_views as api_view

urlpatterns = [
  path('token/', api_view.MyTokenObtainPairView.as_view()),
  path('token/refresh/', TokenRefreshView.as_view()),
  path('register/', api_view.RegisterView.as_view()),
  path('profile/<int:user_id>/', api_view.ProfileView.as_view())
  ]