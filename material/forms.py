from django import forms

from .models import Material

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ["source", "category", "title", "unit", "quantity", "price"]
        
        widgets = {
            "source" : forms.Select(attrs = {"class" : "form-control", "style" : "background-color: #fff;"}),
            "category" : forms.Select(attrs = {"class" : "form-control", "style" : "background-color: #fff;"}),
            "title" : forms.Textarea(attrs = {"class" : "form-control", "rows" : "1", "style" : "background-color: #fff;"}),
            "unit" : forms.Select(attrs = {"class" : "form-control", "style" : "background-color: #fff;"}),
            "quantity" : forms.NumberInput(attrs = {"class" : "form-control", "style" : "background-color: #fff;"}),
            "price" : forms.NumberInput(attrs = {"class" : "form-control", "style" : "background-color: #fff;"})
        }