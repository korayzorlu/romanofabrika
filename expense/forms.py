from django import forms

from .models import Expense, Company, Excel, Category, Unit

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ["title"]
        
        widgets = {
            "title" : forms.Textarea(attrs = {"class" : "form-control", "rows" : "1", "style" : "background-color: #fff;"})
        }
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["title"]
        
        widgets = {
            "title" : forms.Textarea(attrs = {"class" : "form-control", "rows" : "1", "style" : "background-color: #fff;"})
        }

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ["title"]
        
        widgets = {
            "title" : forms.Textarea(attrs = {"class" : "form-control", "rows" : "1", "style" : "background-color: #fff;"})
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
    
    # def __init__(self, *args, **kwargs):
    #     super(ExpenseForm, self).__init__(*args, **kwargs)
    #     self.fields['company'].empty_label = "Firma Seçiniz"
        
class ExcelForm(forms.ModelForm):
    class Meta:
        model = Excel
        fields = ["file"]
        
        widgets = {
            "file" : forms.FileInput(attrs = {"class" : "form-control", "accept" : ".xlsx", "style" : "background-color: #fff;"})
        }