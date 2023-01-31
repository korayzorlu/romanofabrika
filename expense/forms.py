from django import forms

from .models import Expense, Company, Excel

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ["title", "slug"]
        
        widgets = {
            "title" : forms.Textarea(attrs = {"class" : "form-control", "rows" : "1", "style" : "background-color: #fff;"}),
            "slug" : forms.Textarea(attrs = {"class" : "form-control", "rows" : "1", "style" : "background-color: #fff;"})
        }

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ["created_date", "company", "category", "title", "unit", "quantity", "price"]
        
        widgets = {
            "created_date" : forms.DateInput(attrs = {"class" : "form-control", "style" : "background-color: #fff;"}),
            "company" : forms.Select(attrs = {"class" : "form-control", "style" : "background-color: #fff;"}),
            "category" : forms.Select(attrs = {"class" : "form-control", "style" : "background-color: #fff;"}),
            "unit" : forms.Select(attrs = {"class" : "form-control", "style" : "background-color: #fff;"}),
            "title" : forms.Textarea(attrs = {"class" : "form-control", "rows" : "1", "style" : "background-color: #fff;"}),
            "quantity" : forms.NumberInput(attrs = {"class" : "form-control", "style" : "background-color: #fff;"}),
            "price" : forms.NumberInput(attrs = {"class" : "form-control", "style" : "background-color: #fff;"})
        }
        
class ExcelForm(forms.ModelForm):
    class Meta:
        model = Excel
        fields = ["file"]