from django import forms

from .models import Loan, InstallmentStatus

class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ["status", "bank", "title", "option", "amount", "cost", "transmitted_amount", "interest", "total_debt", "installment_count", "installment_deferral", "start_date", "installment_status"]
        
        widgets = {
            "status" : forms.Select(attrs = {"class" : "form-control", "style" : "background-color: #fff;"}),
            "bank" : forms.Select(attrs = {"class" : "form-control", "style" : "background-color: #fff;"}),
            "title" : forms.Textarea(attrs = {"class" : "form-control", "rows" : "1", "style" : "background-color: #fff;"}),
            "option" : forms.Select(attrs = {"class" : "form-control", "style" : "background-color: #fff;"}),
            "amount" : forms.NumberInput(attrs = {"class" : "form-control", "style" : "background-color: #fff;"}),
            "cost" : forms.NumberInput(attrs = {"class" : "form-control", "style" : "background-color: #fff;"}),
            "transmitted_amount" : forms.NumberInput(attrs = {"class" : "form-control", "style" : "background-color: #fff;"}),
            "interest" : forms.NumberInput(attrs = {"class" : "form-control", "style" : "background-color: #fff;"}),
            "total_debt" : forms.NumberInput(attrs = {"class" : "form-control", "style" : "background-color: #fff;"}),
            "installment_count" : forms.NumberInput(attrs = {"class" : "form-control", "style" : "background-color: #fff;"}),
            "installment_deferral" : forms.NumberInput(attrs = {"class" : "form-control", "style" : "background-color: #fff;"}),
            "start_date" : forms.DateInput(attrs = {"class" : "form-control", "style" : "background-color: #fff;"}),
            "installment_status" : forms.Select(attrs = {"class" : "form-control", "style" : "background-color: #fff;"})
        }
    
    # def __init__(self, *args, **kwargs):
    #     super(ExpenseForm, self).__init__(*args, **kwargs)
    #     self.fields['company'].empty_label = "Firma Seçiniz"
    
class InstallmentStatusForm(forms.ModelForm):
    class Meta:
        model = Loan #burada Loan modelini seçmemeizin sebebi order'da olduğu gibi.
        fields = ["installment_status"]
        
        widgets = {
            "installment_status" : forms.Select(attrs = {"class" : "form-control", "style" : "background-color: #fff;"})
        }


