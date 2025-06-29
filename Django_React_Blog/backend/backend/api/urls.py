from django.urls import path, include
from . import views as api_view

urlpatterns = [
  path('user/', include('api.views.user_urls')),
  path('post/', include('api.views.post_urls')),
  path('author/dashboard/', include('api.views.author_urls'))
]