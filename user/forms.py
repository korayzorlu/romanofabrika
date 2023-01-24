from django import forms
from django.contrib import messages

from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput
from django.contrib.auth.models import AbstractUser

from .models import Employee

class LoginForm(forms.Form):
    username = forms.CharField(label = "Kullanıcı Adı", widget = forms.TextInput(attrs={'placeholder': 'Kullanıcı Adı'}))
    password = forms.CharField(label = "Parola", widget = forms.PasswordInput(attrs={'placeholder': 'Parola'}))

class RegisterForm(forms.Form):
    username = forms.CharField(max_length = 50, label = "Kullanıcı Adı", widget = forms.TextInput(attrs={'placeholder': 'Kullanıcı Adı'}))
    email = forms.EmailField(label = "E-Mail", widget = forms.TextInput(attrs={'placeholder': 'E-Posta'}))
    password = forms.CharField(min_length = 6, max_length = 20, label = "Parola", widget = forms.PasswordInput(attrs={'placeholder': 'Parola'}))
    confirm = forms.CharField(min_length = 6, max_length = 20, label = "Parolayı Doğrula", widget = forms.PasswordInput(attrs={'placeholder': 'Parola Onay'}))
    
    def clean(self):
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")

        checkusers = User.objects.all()
        checkmails = User.objects.filter(email = email)
        
        for a in checkusers:
            if str(a) == username:
                raise forms.ValidationError("Kullanıcı Adı Sistemde Kayıtlı!")

        for a in checkmails:
            if str(a.email) == email:
                raise forms.ValidationError("E-Posta İle Daha Önce Kayıt Olunmuş!")

        if password and confirm and password != confirm:
            raise forms.ValidationError("Parolalar Eşleşmiyor!")     

        values = {
                    "username" : username,
                    "email" : email,
                    "password" : password
                }
        
        return values


class ProfileEmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["image"]