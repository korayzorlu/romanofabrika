from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from django.http.response import StreamingHttpResponse

from django.utils import timezone
from django.utils.formats import date_format
from django.utils import translation
from django.db.models import Count

from datetime import date, timedelta, datetime
import calendar

from expense.models import Expense
from order.models import Order
from loan.models import Loan
from product.models import Product

import requests

import collections, functools, operator

# Create your views here.


#@user_passes_test(lambda u: u.is_superuser, login_url = "/admin")
@login_required(login_url = "user:login")
def index(request):

    return render(request, "index/index.html")

@login_required(login_url = "user:login")
def dashboard(request):
    tag = "Kontrol Paneli"
    lineGraphTag = "Satış Grafiği (30 Gün)"
    pieGraphTag = "Satış Kategori Dağılımı (30 Gün)"
    
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
    dataOrdersCategories = []
    pieDatas = []
    
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
                #for category and for pie
                try:
                    for pro in order.products:
                        orderCategoryProduct = get_object_or_404(Product, product_id = pro["productID"])
                        print(float(pro["productTotal"]))
                        pieDatas.append({str(orderCategoryProduct.category.title) : float(pro["productTotal"])})
                except:
                    pass
        dataOrders.append(sum(dailyOrder))
    
    #çizgi grafği
    lineData = []
    for i in range(31):
        lineData.append({
            "day" : datetime.strptime(days[i], "%Y-%m-%d").date(),
            "data" : round(dataExpenses[i],2),
            "orderData" : round(dataOrders[i],2)
        })
    
    #pasta grafiği
    pieDataConf = dict(functools.reduce(operator.add, map(collections.Counter, pieDatas)))
    pieDataCategories = list(pieDataConf.keys())
    pieDataTotals = list(pieDataConf.values())
    pieData = []
    
    for i in range(len(pieDataCategories)):
        pieData.append({"category" : pieDataCategories[i], "total" : pieDataTotals[i]})
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
            try:
                orderProduct = get_object_or_404(Product, product_id = product["productID"])
                ordersProductsList.append({"id" : orderProduct.product_id})
                ordersProductsStatusList.append(product["productStatus"])
            except:
                pass
    
    bekleyenCount = ordersProductsStatusList.count("Bekliyor")
    uretimCount = ordersProductsStatusList.count("Üretimde")
    montajCount = ordersProductsStatusList.count("Montajda")
    
    productCounts = {}

    # tüm name değerlerinin sayısını hesapla
    for item in ordersProductsList:
        name = item["id"]
        if name in productCounts:
            productCounts[name] += 1
        else:
            productCounts[name] = 1

    # en çok tekrarlanan ilk 6 name değerini bul
    mostSelledProducts = []
    if len(ordersProductsList) > 0:
        for i in range(6):
            most_common_name = max(productCounts, key=productCounts.get)
            mostSelledProduct = get_object_or_404(Product, product_id = most_common_name)
            mostSelledProducts.append({"name" : mostSelledProduct.title, "count" : productCounts[most_common_name], "img" : mostSelledProduct.images[0]})
            del productCounts[most_common_name]

    
    
    
    ########################
    
    

    #headers = {"Authorization": "Bearer <>"}
    #dd = requests.get("https://api.ziraatbank.com.tr/portal/atms", headers = headers)
    #print(dd)

    context = {
                "tag" : tag,
                "lineGraphTag": lineGraphTag,
                "pieGraphTag" : pieGraphTag,
                "lineData" : lineData,
                "pieData" : pieData,
                "expensesCurrentMonthTotal" : expensesCurrentMonthTotal,
                "currentMonthName" : currentMonthName,
                "expensesLastMonthTotal" : expensesLastMonthTotal,
                "orders" : orders,
                "ordersCurrentMonthTotal" : ordersCurrentMonthTotal,
                "ordersLastMonthTotal" : ordersLastMonthTotal,
                "mostSelledProducts" : mostSelledProducts,
                "bekleyenCount" : bekleyenCount,
                "uretimCount" : uretimCount,
                "montajCount" : montajCount,
                "loans" : loans
            }

    return render(request, "dashboard/dashboard.html", context)

