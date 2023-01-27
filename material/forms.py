from django import forms

from .models import Source, Material

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ["source", "type", "title", "quantity_type", "quantity", "price"]
        
        widgets = {
            "source" : forms.Select(attrs = {"class" : "form-control", "style" : "background-color: #fff;"}),
            "type" : forms.Select(attrs = {"class" : "form-control", "style" : "background-color: #fff;"}),
            "quantity_type" : forms.Select(attrs = {"class" : "form-control", "style" : "background-color: #fff;"})
        }