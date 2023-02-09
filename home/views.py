from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from django.utils import timezone

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
    
    #####Line Graph#####
    days = []

    for i in range(31):
        days.append((timezone.now().date()-timedelta(days=i)).isoformat())

    days.reverse()
    
    dataExpenses = []
    
    for day in days:
        dailyExpense = []
        for expense in expenses:
            if str(expense.created_date) == str(day):
                dailyExpense.append(float(expense.total))
            else:
                dailyExpense.append(0)
        dataExpenses.append(sum(dailyExpense))
    
    lineData = []

    for i in range(31):
        lineData.append({
            "day" : days[i],
            "data" : round(dataExpenses[i],2)
        })
        
    expenseTotal30 = round(sum(dataExpenses),2)
    ########################
    
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