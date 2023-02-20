from django.contrib import admin
from django.urls import path
from .import views

from django.contrib.auth import views as auth_views

app_name = "order"

urlpatterns = [
    #path('orders/', views.orders, name = "orders"),
    path('update-orders/', views.updateOrders, name = "update-orders"),
    path('update-status/<int:id>/<int:counter>', views.updateStatus, name = "update-status"),
    path('show-image/<int:id>/<int:counter>', views.showImage, name = "show-image"),
    path('print-orders/', views.printOrders, name = "print-orders"),
]