from django.contrib import admin
from django.urls import path
from .import views

from django.contrib.auth import views as auth_views

app_name = "loan"

urlpatterns = [
    path('add-loan/', views.addLoan, name = "add-loan"),
    path('update-loan/<int:id>', views.updateLoan, name = "update-loan"),
    path('update-installment-status/<int:id>', views.updateInstallmentStatus, name = "update-installment-status"),
    path('get-delete-loan/<int:id>', views.getDeleteLoan, name = "get-delete-loan"),
    path('delete-loan/<int:id>', views.deleteLoan, name = "delete-loan"),
]