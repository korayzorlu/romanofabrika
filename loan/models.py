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
    
class LoanOption(models.Model):
    title = models.CharField(max_length=200, verbose_name = "Hesaplama")

    class Meta:   
        verbose_name_plural = "loan options"

    def __str__(self):
        return self.title

class Loan(models.Model):
    status = models.ForeignKey(LoanStatus, on_delete = models.SET_DEFAULT, default = 1, verbose_name = "Kredi Durumu")
    bank = models.ForeignKey(Bank, on_delete = models.SET_DEFAULT, default = 1, verbose_name = "Banka")
    title = models.CharField(max_length=200, verbose_name = "Kredi İsmi")
    option = models.ForeignKey(LoanOption, on_delete = models.SET_DEFAULT, default = 1, verbose_name = "Hesaplama/Giriş")
    amount = models.FloatField(verbose_name = "Kredi Tutarı", default = 0.00)
    cost = models.FloatField(verbose_name = "Masraf", default = 0.00)
    transmitted_amount = models.FloatField(null = True, blank = True, verbose_name = "Hesaba Aktarılan Tutar")
    interest = models.FloatField(verbose_name = "Faiz", default = 0.00)
    total_debt = models.FloatField(null = True, blank = True, verbose_name = "Toplam Borç")
    installment_count = models.IntegerField(verbose_name = "Taksit Sayısı", default = 1)
    installments = models.JSONField(null = True, blank = True,verbose_name = "Taksitler")
    start_date = models.DateField(auto_now_add = False, default = timezone.now, editable = True, verbose_name = "Kredi Başlangıç Tarihi")
    
    def save(self, ** kwargs):
        if self.option.id == 1:
            self.transmitted_amount = self.transmitted_amount
            self.total_debt = self.total_debt
        else:
            self.transmitted_amount = self.amount - self.cost
            self.total_debt = ((self.amount * ((((self.interest / 100) * 1.15 * 1.05) * ((1 + ((self.interest / 100) * 1.15 * 1.05)) ** self.installment_count) ) / (((1 + ((self.interest / 100) * 1.15 * 1.05)) ** self.installment_count) - 1))) * self.installment_count) + (self.amount / 100)
        return super(Loan, self).save()
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return self.title
    