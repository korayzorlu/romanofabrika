from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from datetime import date, timedelta

from expense.models import Expense

# Create your views here.

#@user_passes_test(lambda u: u.is_superuser, login_url = "/admin")
@login_required(login_url = "user:login")
def index(request):

    return render(request, "index/index.html")

@login_required(login_url = "user:login")
def dashboard(request):
    tag = "Kontrol Paneli"
    
    expenses = Expense.objects.filter().order_by("-created_date")
    expensesList = []
    for i in range(31):
        expensesList.append(float(expenses[i].total))

    expenseTotal30 = sum(expensesList)

    #Line Graph
    days = []

    for i in range(31):
        days.append((date.today()-timedelta(days=i)).isoformat())

    days.reverse()
    
    sales = [1,3,4,3,6,5,8,4,14,12,8,9,6,16,9,10,8,7,8,8,9,12,11,13,13,12,7,17,18,19,19]

    lineData = []

    for i in range(31):
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
                "pieData" : pieData,
                "expenseTotal30" : expenseTotal30
            }

    return render(request, "dashboard/dashboard.html", context)