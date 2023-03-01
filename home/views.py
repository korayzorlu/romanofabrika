from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from django.utils import timezone
from django.utils.formats import date_format
from django.utils import translation
from django.db.models import Count

from datetime import date, timedelta, datetime
import calendar

from expense.models import Expense
from order.models import Order
from loan.models import Loan

import requests

# Create your views here.

#@user_passes_test(lambda u: u.is_superuser, login_url = "/admin")
@login_required(login_url = "user:login")
def index(request):

    return render(request, "index/index.html")

@login_required(login_url = "user:login")
def dashboard(request):
    tag = "Kontrol Paneli"
    lineGraphTag = "Satış Grafiği (30 Gün)"
    
    expenses = Expense.objects.filter().order_by("-created_date")
    orders = Order.objects.filter().order_by("-order_date")
    loans = Loan.objects.filter().order_by("next_installment")
    
    translation.activate('tr')
    
    #####Line Graph#####
    days = []

    for i in range(31):
        days.append((timezone.now().date()-timedelta(days=i)).isoformat())

    days.reverse()
 
    dataExpenses = []
    dataOrders = []
    
    for day in days:
        dailyExpense = []
        dailyOrder = []
        for expense in expenses:
            if str(expense.created_date) == str(day):
                dailyExpense.append(float(expense.total))
            else:
                dailyExpense.append(0)
        dataExpenses.append(sum(dailyExpense))
        for order in orders:
            if str(order.order_date) == str(day):
                dailyOrder.append(float(order.total))
        dataOrders.append(sum(dailyOrder))
    
    lineData = []

    for i in range(31):
        lineData.append({
            "day" : datetime.strptime(days[i], "%Y-%m-%d").date(),
            "data" : round(dataExpenses[i],2),
            "orderData" : round(dataOrders[i],2)
        })
    ########################

    ######Monthly Total######
    #expenseTotal30 = round(sum(dataExpenses),2)
    expenseListCurrentMonth = []
    orderListCurrentMonth = []
    
    currentMonth = datetime.today().month
    currentMonthName = date_format(datetime.today(), "F")
    
    for i in range(len(lineData)):
        dataMonth = lineData[i]["day"].month
        if dataMonth == currentMonth:
            expenseListCurrentMonth.append(lineData[i]["data"])
            orderListCurrentMonth.append(lineData[i]["orderData"])
    
    expensesCurrentMonthTotal = round(sum(expenseListCurrentMonth),2)
    ordersCurrentMonthTotal = round(sum(orderListCurrentMonth),2)
    
    lastMonthStart= "2023-" + str(currentMonth - 1) + "-01"
    lastMonthEnd = "2023-" + str(currentMonth - 1) + "-" + str(calendar.monthrange(2023, currentMonth - 1)[1])
    expensesLastMont = Expense.objects.filter(created_date__range = (lastMonthStart, lastMonthEnd)).order_by("-created_date")
    ordersLastMonth = Order.objects.filter(order_date__range = (lastMonthStart, lastMonthEnd)).order_by("-order_date")
    expensesLastMonthList = []
    ordersLastMonthList = []
    for exp in expensesLastMont:
        expensesLastMonthList.append(exp.total)
    expensesLastMonthTotal = round(sum(expensesLastMonthList),2)
    for ord in ordersLastMonth:
        ordersLastMonthList.append(ord.total)
    ordersLastMonthTotal = round(sum(ordersLastMonthList),2)
    ########################
    
    #####En Çok Satan Ürün#####
    ordersProductsList = []
    ordersProductsStatusList = [] #ürün durumlarının sayısını da burada alabiliriz
    for order in orders:
        for product in order.products:
            ordersProductsList.append({"name" : product["productName"], "img" : product["productImg"], "price" : product["productPrice"]})
            ordersProductsStatusList.append(product["productStatus"])
    
    bekleyenCount = ordersProductsStatusList.count("Bekliyor")
    uretimCount = ordersProductsStatusList.count("Üretimde")
    montajCount = ordersProductsStatusList.count("Montajda")
    
    def most_frequent(List):
        #1
        counter = 0
        num1 = List[0]
        
        for i in List:
            curr_frequency = List.count(i)
            if(curr_frequency> counter):
                counter = curr_frequency
                num1 = i

        #2
        List = list(filter((num1).__ne__, List))
        counter = 0
        num2 = List[0]
        
        for i in List:
            curr_frequency = List.count(i)
            if(curr_frequency> counter):
                counter = curr_frequency
                num2 = i
                
        #3
        List = list(filter((num2).__ne__, List))
        counter = 0
        num3 = List[0]
        
        for i in List:
            curr_frequency = List.count(i)
            if(curr_frequency> counter):
                counter = curr_frequency
                num3 = i
                
        #4
        List = list(filter((num3).__ne__, List))
        counter = 0
        num4 = List[0]
        
        for i in List:
            curr_frequency = List.count(i)
            if(curr_frequency> counter):
                counter = curr_frequency
                num4 = i
                
        #5
        List = list(filter((num4).__ne__, List))
        counter = 0
        num5 = List[0]
        
        for i in List:
            curr_frequency = List.count(i)
            if(curr_frequency> counter):
                counter = curr_frequency
                num5 = i
                
        #6
        List = list(filter((num5).__ne__, List))
        counter = 0
        num6 = List[0]
        
        for i in List:
            curr_frequency = List.count(i)
            if(curr_frequency> counter):
                counter = curr_frequency
                num6 = i
        
        return num1, num2, num3, num4, num5, num6
    if len(ordersProductsList) > 0:
        mostSelledProduct = most_frequent(ordersProductsList)
    else:
        mostSelledProduct = []
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

    #headers = {"Authorization": "Bearer <>"}
    #dd = requests.get("https://api.ziraatbank.com.tr/portal/atms", headers = headers)
    #print(dd)

    context = {
                "tag" : tag,
                "lineGraphTag": lineGraphTag,
                "lineData" : lineData,
                "pieData" : pieData,
                "expensesCurrentMonthTotal" : expensesCurrentMonthTotal,
                "currentMonthName" : currentMonthName,
                "expensesLastMonthTotal" : expensesLastMonthTotal,
                "orders" : orders,
                "ordersCurrentMonthTotal" : ordersCurrentMonthTotal,
                "ordersLastMonthTotal" : ordersLastMonthTotal,
                "mostSelledProduct" : mostSelledProduct,
                "bekleyenCount" : bekleyenCount,
                "uretimCount" : uretimCount,
                "montajCount" : montajCount,
                "loans" : loans
            }

    return render(request, "dashboard/dashboard.html", context)