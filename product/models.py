from django.db import models

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