from django.contrib import admin
from django.urls import path
from .import views

from django.contrib.auth import views as auth_views

app_name = "user"

urlpatterns = [
    #path('dashboard/', views.dashboard, name = "dashboard"),
    path('register/', views.register, name = "register"),
    path('login/', views.loginUser, name = "login"),
    path('logout/', views.logoutUser, name = "logout"),
    #path('user/', include('django.contrib.auth.urls')),
]