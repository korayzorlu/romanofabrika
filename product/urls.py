from django.contrib import admin
from django.urls import path
from .import views

from django.contrib.auth import views as auth_views

app_name = "product"

urlpatterns = [
    #path('products/', views.products, name = "products"),
    path('update-categories/', views.updateCategories, name = "update-categories"),
]