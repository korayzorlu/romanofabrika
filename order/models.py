from django.db import models

# Create your models here.

class Order(models.Model):
    shop = models.ForeignKey("auth.User", on_delete = models.CASCADE, verbose_name = "Mağaza")
    title = models.CharField(max_length=200, verbose_name = "Marka İsmi")
    slug = models.SlugField(unique=True)

    class Meta:
        unique_together = ('slug',)    
        verbose_name_plural = "brands"

    def __str__(self):
        return self.title