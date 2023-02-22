from django.db import models

from django.utils import timezone

# Create your models here.

class Bank(models.Model):
    title = models.CharField(max_length=200, verbose_name = "Banka")

    class Meta:
        verbose_name_plural = "banks"
        ordering = ['title']

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

class Loan(models.Model):
    title = models.CharField(max_length=200, verbose_name = "Kredi İsmi")
    bank = models.ForeignKey(Bank, on_delete = models.SET_DEFAULT, default = 1, verbose_name = "Banka")
    amount = models.FloatField(verbose_name = "Kredi Tutarı", default = 0.00)
    cost = models.FloatField(verbose_name = "Masraf", default = 0.00)
    transmitted_amount = models.FloatField(null = True, blank = True, verbose_name = "Hesaba Aktarılan Tutar")
    interest = models.FloatField(verbose_name = "Faiz", default = 0.00)
    total_debt = models.FloatField(null = True, blank = True, verbose_name = "Toplam Borç")
    installment_count = models.IntegerField(verbose_name = "Taksit Sayısı", default = 1)
    installments = models.JSONField(verbose_name = "Taksitler")
    status = models.ForeignKey(LoanStatus, on_delete = models.SET_DEFAULT, default = 1, verbose_name = "Kredi Durumu")
    start_date = models.DateField(auto_now_add = False, default = timezone.now, editable = True, verbose_name = "Tarih")
    
    def save(self, ** kwargs):
        self.transmitted_amount = self.amount - self.cost
        self.total_debt = self.amount * (((self.interest * 1.2) * ((1 + (self.interest * 1.2)) ** self.installment_count) ) / (((1 + (self.interest * 1.2)) ** self.installment_count) - 1))
        return super(Loan, self).save()
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return self.title
    