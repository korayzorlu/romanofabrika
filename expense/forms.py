from django import forms

from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ["company", "category", "title", "unit", "quantity", "price"]
        
        widgets = {
            "source" : forms.Select(attrs = {"class" : "form-control", "style" : "background-color: #fff;"}),
            "category" : forms.Select(attrs = {"class" : "form-control", "style" : "background-color: #fff;"}),
            "unit" : forms.Select(attrs = {"class" : "form-control", "style" : "background-color: #fff;"})
        }