from django.contrib import admin
from django.urls import path
from .import views

from django.contrib.auth import views as auth_views

app_name = "material"

urlpatterns = [
    #path('materials/', views.materials, name = "materials"),
    path('add-material/', views.addMaterial, name = "add-material"),
    path('update-material/<int:id>', views.updateMaterial, name = "update-material"),
    path('get-delete-material/<int:id>', views.getDeleteMaterial, name = "get-delete-material"),
    path('delete-material/<int:id>', views.deleteMaterial, name = "delete-material"),
    path('add-source/', views.addSource, name = "add-source"),
    path('add-category/', views.addCategory, name = "add-category"),
    path('add-unit/', views.addUnit, name = "add-unit"),
]