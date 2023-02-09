from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from django.utils import timezone
from django.utils.formats import date_format
from django.utils import translation

from datetime import date, timedelta, datetime
import calendar

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
    
    translation.activate('tr')
    
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
            "day" : datetime.strptime(days[i], "%Y-%m-%d").date(),
            "data" : round(dataExpenses[i],2)
        })
    ########################
    
    ######Monthly Total######
    #expenseTotal30 = round(sum(dataExpenses),2)
    expenseListCurrentMonth = []
    
    currentMonth = datetime.today().month
    currentMonthName = date_format(datetime.today(), "F")
    
    for i in range(len(lineData)):
        dataMonth = lineData[i]["day"].month
        if dataMonth == currentMonth:
            expenseListCurrentMonth.append(lineData[i]["data"])
    
    expensesCurrentMonthTotal = sum(expenseListCurrentMonth)
    
    lastMonthStart= "2023-" + str(currentMonth - 1) + "-01"
    lastMonthEnd = "2023-" + str(currentMonth - 1) + "-" + str(calendar.monthrange(currentMonth - 1, 1)[1])
    expensesLastMont = Expense.objects.filter(created_date__range = (lastMonthStart, lastMonthEnd)).order_by("-created_date")
    expensesLastMonthList = []
    for exp in expensesLastMont:
        expensesLastMonthList.append(exp.total)
    expensesLastMonthTotal = sum(expensesLastMonthList)
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
                "expensesCurrentMonthTotal" : expensesCurrentMonthTotal,
                "currentMonthName" : currentMonthName,
                "expensesLastMonthTotal" : expensesLastMonthTotal
            }

    return render(request, "dashboard/dashboard.html", context)