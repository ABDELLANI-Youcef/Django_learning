from django.urls import path, include
from . import views as api_view

urlpatterns = [
  path('user/', include('api.views.users.user_urls')),
  path('post/', include('api.views.posts.post_urls')),
  path('author/dashboard/', include('api.views.dashboards.author_urls'))
]