from django.db import models

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
    slug = models.SlugField(unique=True)

    class Meta:
        unique_together = ('slug',)    
        verbose_name_plural = "categories"

    def __str__(self):
        return self.title
    
