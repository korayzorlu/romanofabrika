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
    installment_deferral = models.IntegerField(verbose_name = "Taksit Erteleme", default = 0)
    installments = models.JSONField(null = True, blank = True,verbose_name = "Taksitler")
    start_date = models.DateField(auto_now_add = False, default = timezone.now, editable = True, verbose_name = "Kredi Başlangıç Tarihi")
    next_installment = models.DateField(null = True, blank = True,verbose_name = "Taksitler")
    installment_status = models.ForeignKey(InstallmentStatus, on_delete = models.SET_DEFAULT, default = 3, verbose_name = "Taksit Durumu")
    completed_installment = models.IntegerField(verbose_name = "Tamamlanan Taksitler", default = 0)
    
    def save(self, ** kwargs):
        if self.option.id == 1:
            self.transmitted_amount = self.transmitted_amount
            self.total_debt = self.total_debt
        else:
            self.transmitted_amount = self.amount - self.cost
            self.total_debt = round(((self.amount * ((((self.interest / 100) * 1.15 * 1.05) * ((1 + ((self.interest / 100) * 1.15 * 1.05)) ** self.installment_count) ) / (((1 + ((self.interest / 100) * 1.15 * 1.05)) ** self.installment_count) - 1))) * self.installment_count) + (self.amount / 100), 2)
        return super(Loan, self).save()
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return self.title
    
    
class BCHLoan(models.Model):
    status = models.ForeignKey(LoanStatus, on_delete = models.SET_DEFAULT, default = 1, verbose_name = "Kredi Durumu")
    bank = models.ForeignKey(Bank, on_delete = models.SET_DEFAULT, default = 1, verbose_name = "Banka")
    title = models.CharField(max_length=200, verbose_name = "Kredi İsmi")
    option = models.ForeignKey(LoanOption, on_delete = models.SET_DEFAULT, default = 1, verbose_name = "Hesaplama/Giriş")
    amount = models.FloatField(verbose_name = "Anapara", default = 0.00)
    remaining_amount = models.FloatField(verbose_name = "Kalan Anapara", default = 0.00)
    cost = models.FloatField(verbose_name = "Masraf", default = 0.00)
    transmitted_amount = models.FloatField(null = True, blank = True, verbose_name = "Hesaba Aktarılan Tutar")
    interest = models.FloatField(verbose_name = "Faiz", default = 0.00)
    interest_amount = models.FloatField(verbose_name = "Faiz Tutarı", default = 0.00)
    total_debt = models.FloatField(null = True, blank = True, verbose_name = "Toplam Borç")
    start_date = models.DateField(auto_now_add = False, default = timezone.now, editable = True, verbose_name = "Kredi Başlangıç Tarihi")
    end_date = models.DateField(auto_now_add = False, default = timezone.now, editable = True, verbose_name = "Kredi Bitiş Tarihi")
    interest_payment = models.JSONField(null = True, blank = True,verbose_name = "Faiz Ödemeleri")
    amount_payment = models.JSONField(null = True, blank = True,verbose_name = "Anapara Ödemeleri")
    interest_updates = models.JSONField(null = True, blank = True,verbose_name = "Faiz Güncellemeleri")
    
    def save(self, ** kwargs):
        if self.option.id == 1:
            self.transmitted_amount = self.transmitted_amount
            self.total_debt = self.total_debt
        else:
            self.transmitted_amount = self.amount - self.cost
            self.total_debt = self.remaining_amount + self.interest_amount
        return super(BCHLoan, self).save()
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return self.title