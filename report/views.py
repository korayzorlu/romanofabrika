from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from django.utils import timezone
from django.utils.formats import date_format
from django.utils import translation
from django.db.models import Count

from datetime import date, timedelta, datetime
import calendar

from order.models import Order
from expense.models import Expense

# Create your views here.

@login_required(login_url = "user:login")
def reports(request):
    tag = "Raporlar"
    lineGraphTag = "Satış Grafiği (30 Gün)"
    
    expenses = Expense.objects.filter().order_by("-created_date")
    orders = Order.objects.filter().order_by("-order_date")
    
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
    
    context = {
                "tag" : tag,
                "lineGraphTag" : lineGraphTag,
                "lineData"  : lineData
    }

    return render(request, "report/reports.html", context)