from django.contrib import admin
from django.urls import path
from .import views

from django.contrib.auth import views as auth_views

app_name = "order"

urlpatterns = [
    #path('orders/', views.orders, name = "orders"),
    path('update-orders/', views.updateOrders, name = "update-orders"),
]