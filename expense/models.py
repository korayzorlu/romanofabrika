from django.db import models

from django.utils import timezone

import datetime



# Create your models here.

class Company(models.Model):
    title = models.CharField(max_length=200, verbose_name = "Firma")
    slug = models.SlugField(unique=True)

    class Meta:
        unique_together = ('slug',)    
        verbose_name_plural = "companies"

    def __str__(self):
        return self.title
    
class Category(models.Model):
    title = models.CharField(max_length=200, verbose_name = "Kategori")

    class Meta:   
        verbose_name_plural = "categories"

    def __str__(self):
        return self.title
    
class Unit(models.Model):
    title = models.CharField(max_length=200, verbose_name = "Birim")

    def __str__(self):
        return self.title
    
class Expense(models.Model):
    company = models.ForeignKey(Company, on_delete = models.CASCADE, default = 1, verbose_name = "Firma")
    category = models.ForeignKey(Category, on_delete = models.SET_DEFAULT, default = 1, verbose_name = "Kategori")
    title = models.CharField(max_length=200, verbose_name = "Ürün/Hizmet")
    unit = models.ForeignKey(Unit, on_delete = models.SET_DEFAULT, default = 1, verbose_name = "Birim")
    created_date = models.DateField(auto_now_add = False, default = timezone.now(), editable = True, verbose_name = "Tarih")
    quantity = models.FloatField(verbose_name = "Miktar", default = 1)
    price = models.FloatField(verbose_name = "Birim Fiyat", default = 0.00)
    total = models.FloatField(null = True, blank = True)
    
    def save(self, ** kwargs):
        self.total = self.quantity * self.price
        return super(Expense, self).save()
    
    def __str__(self):
        return self.title

class Excel(models.Model):
    file = models.FileField(blank =True, null = True, verbose_name = "Excel Dosyası")