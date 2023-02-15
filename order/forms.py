from django import forms

from .models import Order

from splitjson.widgets import SplitJSONWidget

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["order_status"]
        
        widgets = {
            "order_status" : forms.Select(attrs = {"class" : "form-control", "style" : "background-color: #fff;"})
        }

