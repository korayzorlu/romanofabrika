from django.db import models

from ckeditor.fields import RichTextField

# Create your models here.

from mptt.models import MPTTModel, TreeForeignKey

class Category(MPTTModel):
    title = models.CharField(max_length=200)
    parent = TreeForeignKey('self', blank = True, null = True, related_name = 'child', on_delete = models.CASCADE)
    category_id = models.IntegerField(verbose_name = "Kategori ID", default = 0)

    class Meta:
        #unique_together = ('parent',)    
        verbose_name_plural = "categories"   

    def __str__(self):                           
        full_path = [self.title]            
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent

        return ' > '.join(full_path[::-1])

class Product(models.Model):
    product_id = models.IntegerField(verbose_name = "Ürün ID", default = 1)
    title = models.CharField(max_length=200, verbose_name = "Ürün Başlığı")
    category = models.ForeignKey(Category, on_delete = models.CASCADE, verbose_name = "Kategori")
    categories = models.JSONField(null = True, blank = True,verbose_name = "Kategoriler")
    description = RichTextField(blank = True, verbose_name = "Ürün Açıklaması")
    images = models.JSONField(null = True, blank = True,verbose_name = "Resimler")
    special_3 = models.CharField(null = True, blank = True, max_length=200, verbose_name = "Özel Alan 3")
    special_4 = models.CharField(null = True, blank = True, max_length=200, verbose_name = "Özel Alan 4")
    special_5 = models.CharField(null = True, blank = True, max_length=200, verbose_name = "Özel Alan 5")
    variations = models.JSONField(null = True, blank = True,verbose_name = "Varyasyonlar")
    
    def __str__(self):
        return self.title
