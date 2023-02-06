from django.contrib import admin
from django.urls import path
from .import views

from django.contrib.auth import views as auth_views

app_name = "expense"

urlpatterns = [
    path('add-expense/', views.addExpense, name = "add-expense"),
    path('add-expense-batch/', views.addExpenseBatch, name = "add-expense-batch"),
    path('update-expense/<int:id>', views.updateExpense, name = "update-expense"),
    path('get-delete-expense/<int:id>', views.getDeleteExpense, name = "get-delete-expense"),
    path('delete-expense/<int:id>', views.deleteExpense, name = "delete-expense"),
    path('add-company/', views.addCompany, name = "add-company"),
    path('add-category/', views.addCategory, name = "add-category"),
    path('add-unit/', views.addUnit, name = "add-unit"),
    path('download-expense-excel/', views.downloadExpenseExcel, name = "download-expense-excel"),
]