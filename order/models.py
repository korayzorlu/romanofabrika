from django.db import models

from django.utils import timezone

from datetime import datetime
import numpy as np

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
    delivery_date = models.DateField(null = True, blank = True, editable = True, verbose_name = "Teslimat Tarihi")
    customer_name = models.CharField(max_length=200, verbose_name = "Müşteri Adı")
    products = models.JSONField(verbose_name = "Ürünler")
    cargo_address = models.JSONField(verbose_name = "Teslimat")
    order_status = models.ForeignKey(Status, on_delete = models.SET_DEFAULT, default = 1, verbose_name = "Sipariş Durumu")
    total = models.FloatField(verbose_name = "Sipariş Tutarı", default = 0.00)
    
    def save(self, ** kwargs):
        d_date = np.busday_offset(str(self.order_date), 30, roll='forward')
        self.delivery_date = datetime.strptime(str(d_date), "%Y-%m-%d").date()
        return super(Order, self).save()

    def __str__(self):
        return self.customer_name
    
    