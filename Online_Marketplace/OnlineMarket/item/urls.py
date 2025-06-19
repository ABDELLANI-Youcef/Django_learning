from django.urls import path
from . import views

app_name = 'item'

urlpatterns = [
  path('detail/<int:pk>', views.detail, name='item_detail'),
  path('new/', views.new, name='item_new'),
]