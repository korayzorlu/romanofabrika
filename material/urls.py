from django.contrib import admin
from django.urls import path
from .import views

from django.contrib.auth import views as auth_views

app_name = "material"

urlpatterns = [
    #path('materials/', views.materials, name = "materials"),
]