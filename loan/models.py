from django.db import models

from django.utils import timezone

# Create your models here.

class Bank(models.Model):
    title = models.CharField(max_length=200, verbose_name = "Banka")

    class Meta:
        verbose_name_plural = "banks"

    def __str__(self):
        return self.title

class InstallmentStatus(models.Model):
    title = models.CharField(max_length=200, verbose_name = "Taksit Durumu")

    class Meta:   
        verbose_name_plural = "installment statuses"

    def __str__(self):
        return self.title
    
class LoanStatus(models.Model):
    title = models.CharField(max_length=200, verbose_name = "Kredi Durumu")

    class Meta:   
        verbose_name_plural = "loan statuses"

    def __str__(self):
        return self.title

