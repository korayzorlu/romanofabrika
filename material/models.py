from django.db import models

# Create your models here.

class Source(models.Model):
    title = models.CharField(max_length=200, verbose_name = "Kaynak")
    slug = models.SlugField(unique=True)

    class Meta:
        unique_together = ('slug',)    
        verbose_name_plural = "sources"

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

class Material(models.Model):
    source = models.ForeignKey(Source, on_delete = models.CASCADE, default = 2, verbose_name = "Kaynak")
    category = models.ForeignKey(Category, on_delete = models.CASCADE, default = 1, verbose_name = "Kategori")
    title = models.CharField(max_length=200, verbose_name = "Malzeme İsmi")
    unit = models.ForeignKey(Unit, on_delete = models.SET_DEFAULT, default = 1, verbose_name = "Birim")
    quantity = models.FloatField(verbose_name = "Miktar", default = 1)
    price = models.FloatField(verbose_name = "Birim Fiyat", default = 0.00)
    
    def __str__(self):
        return self.title