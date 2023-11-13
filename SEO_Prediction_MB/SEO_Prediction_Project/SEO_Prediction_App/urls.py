from django.urls import path
from . import views
from .views import *
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name="home"),
    path('register/', register, name='register'), 
    path('dashboard/', dashboard, name='dashboard'),
    path('login/', login_view, name='login'), 
    path('logout/', views.logout_view, name='logout')
]
