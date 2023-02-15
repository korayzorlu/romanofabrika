from django.db import models

from django.utils import timezone

# Create your models here.

class Status(models.Model):
    title = models.CharField(max_length=200, verbose_name = "Sipariş Durumu")

    class Meta:   
        verbose_name_plural = "statuses"

    def __str__(self):
        return self.title

class Order(models.Model):
    order_id = models.IntegerField(verbose_name = "Sipariş ID", default = 1)
    order_date = models.DateField(auto_now_add = False, default = timezone.now, editable = True, verbose_name = "Sipariş Tarihi")
    customer_name = models.CharField(max_length=200, verbose_name = "Müşteri Adı")
    products = models.JSONField(verbose_name = "Ürünler")
    order_status = models.ForeignKey(Status, on_delete = models.SET_DEFAULT, default = 1, verbose_name = "Sipariş Durumu")
    total = models.FloatField(verbose_name = "Sipariş Tutarı", default = 0.00)

    def __str__(self):
        return self.customer_name