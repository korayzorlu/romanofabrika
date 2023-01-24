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

from datetime import date, timedelta


# Create your views here.
@login_required(login_url = "user:login")
def dashboard(request):
    tag = "Kontrol Paneli"


    #Line Graph
    days = []

    for i in range(30):
        days.append((date.today()-timedelta(days=i)).isoformat())

    days.reverse()
    
    sales = [3,4,3,6,5,8,4,14,12,8,9,6,16,9,10,8,7,8,8,9,12,11,13,13,12,7,17,18,19,19]

    lineData = []

    for i in range(30):
        lineData.append({
            "day" : days[i],
            "sale" : sales[i]
        })
    
    #Pie Graph
    pieData = [
        {"shop" : "Trendyol", "sale" : 12},
        {"shop" : "Hepsiburada", "sale" : 30},
        {"shop" : "N11", "sale" : 20},
        {"shop" : "Gittigidiyor", "sale" : 7},
        {"shop" : "Çiçeksepeti", "sale" : 5},
        {"shop" : "Amazon", "sale" : 9}
    ]

    context = {
                "tag" : tag,
                "lineData" : lineData,
                "pieData" : pieData
            }

    return render(request, "dashboard/dashboard.html", context)

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
        user_membership = UserMembership.objects.create(user = newUser, membership = demo_membership)
        user_membership.save()
        user_subscription = Subscription()
        user_subscription.user_membership = user_membership
        user_subscription.save()
        
        newemployee = Employee.objects.create(user = newUser)
        newemployee.save()
        newUser.employee.membership = str(user_membership.membership.membership_type)
        newUser.employee.save()
        login(request, newUser)
        messages.info(request, "Başarıyla kayıt oldunuz...")
        """
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
        return redirect("index")

    if request.user.is_authenticated:
        return redirect("index")

    

    return render(request, "authentication/login.html", context)

@login_required
def logoutUser(request):
    logout(request)
    messages.success(request, "Başarıyla Çıkış Yaptınız")

    return redirect("user:login")


