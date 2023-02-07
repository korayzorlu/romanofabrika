from django import forms

from .models import Material, Source, Category, Unit

class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
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