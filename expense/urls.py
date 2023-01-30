from django.contrib import admin
from django.urls import path
from .import views

from django.contrib.auth import views as auth_views

app_name = "expense"

urlpatterns = [
    path('add-expense/', views.addExpense, name = "add-expense"),
    path('update-expense/<int:id>', views.updateExpense, name = "update-expense"),
]