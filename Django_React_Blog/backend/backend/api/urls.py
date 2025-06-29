from django.urls import path, include
from . import views as api_view

urlpatterns = [
  path('user/', include('api.views.user_urls')),
  path('post/', include('api.views.post_urls')),
  path('author/dashboard/stats/<user_id>', api_view.DashboardStatsView.as_view())
]