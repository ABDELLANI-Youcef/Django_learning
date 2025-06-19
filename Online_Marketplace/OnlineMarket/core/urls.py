from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

from .forms import LoginForm

urlpatterns = [
    path('', views.index, name='home'),
    path('contact/', views.contact, name='contact'),
    path('signup/', views.sigup, name='signup'),
    path('login/', auth_views.LoginView.as_view(authentication_form=LoginForm, template_name='core/login.html'), name='login'),
]
