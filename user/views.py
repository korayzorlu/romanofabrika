import profile
from django.shortcuts import render, redirect, get_object_or_404

from .forms import RegisterForm, LoginForm, ProfileEmployeeForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Employee

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django import template
from django.core.mail import EmailMultiAlternatives




# Create your views here.


def register(request):
    form = RegisterForm(request.POST or None)

    if form.is_valid():
        """
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        newUser = User(username = username, email = email)
        newUser.set_password(password)
        newUser.save()
        
        newemployee = Employee.objects.create(user = newUser)
        newemployee.save()
        login(request, newUser)
        """
        #messages.info(request, "Başarıyla kayıt oldunuz...")
        messages.info(request, "Kayıtlar Şuan Kapalı...")
        
        return redirect("index")

    if request.user.is_authenticated:
        return redirect("index")

    context = {
                "form" : form
            }
    return render(request, "authentication/register.html", context)

    """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            newUser = User(username = username)
            newUser.set_password(password)
            newUser.save()
            login(request, newUser)
            return redirect("index")
        context = {
                    "form" : form
                }
        return render(request, "register.html", context)
    else:
        form = RegisterForm()
        context = {
                    "form" : form
                }
        return render(request, "register.html", context)
    """
def loginUser(request):
    form = LoginForm(request.POST or None)
    formRegister = RegisterForm(request.POST or None)

    context = {
                "form" : form,
                "formRegister" : formRegister
            }
    
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(username = username, password = password)

        if user is None:
            messages.info(request, "Kullancıı Adı veya Parola Hatalı!")
            return render(request, "authentication/login.html", context)

        messages.success(request, "Başarıyla giriş yaptınız...")
        login(request, user)
        return redirect("dashboard")

    if request.user.is_authenticated:
        return redirect("index")

    

    return render(request, "authentication/login.html", context)

@login_required
def logoutUser(request):
    logout(request)
    messages.success(request, "Başarıyla Çıkış Yaptınız")

    return redirect("user:login")


