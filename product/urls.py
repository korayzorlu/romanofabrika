from django.contrib import admin
from django.urls import path
from .import views

from django.contrib.auth import views as auth_views

app_name = "product"

urlpatterns = [
    #path('products/', views.products, name = "products"),
    path('update-products/', views.updateProducts, name = "update-products"),
    path('update-categories/', views.updateCategories, name = "update-categories"),
    path('show-image/<int:id>/', views.showImage, name = "show-image"),
]