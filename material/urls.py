from django.contrib import admin
from django.urls import path
from .import views

from django.contrib.auth import views as auth_views

app_name = "material"

urlpatterns = [
    #path('materials/', views.materials, name = "materials"),
    path('add-material/', views.addMaterial, name = "add-material"),
    path('update-material/<int:id>', views.updateMaterial, name = "update-material"),
]