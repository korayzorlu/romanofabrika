from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from django.contrib import messages

from django.utils import translation

from .models import Order, Status
from .forms import OrderForm

import json
from suds.client import Client
from suds.sudsobject import asdict
from datetime import date, timedelta, datetime

from .tasks import updateOrdersTask


# Create your views here.

#@user_passes_test(lambda u: u.is_superuser, login_url = "/admin")
@login_required(login_url = "user:login")
def orders(request):
    tag = "Siparişler"
    
    translation.activate('tr')
    
    orders = Order.objects.filter()
    
    context = {
                "tag" : tag,
                "orders" : orders
            }

    return render(request, "order/orders.html", context)

@login_required(login_url = "user:login")
def updateOrders(request):
    tag = "Siparişler"
    
    updateOrdersTask.delay()
    
    messages.success(request, "Siparişler Arkaplanda Güncellenecek")
    
    return redirect("orders")

@login_required(login_url = "user:login")
def updateStatus(request, id, counter):
    orders = Order.objects.filter()
    order = get_object_or_404(Order, id = id)
    
    statuses = Status.objects.filter()
    
    form = OrderForm(request.POST or None, request.FILES or None, instance = order)
    
    tag = order.order_id

    if request.method == "POST":
        if form.is_valid():
            order.products[counter]["productStatus"] = form.cleaned_data["order_status"].title
            order.save()
            
        messages.success(request, "Değişiklikler Kaydedildi...")

        return HttpResponse(status=204)

    context = { 
                "tag" : tag,
                "form" : form,
                "orders" : orders,
                "order" : order,
                "counter" : counter,
                "statuses" : statuses
            }

    return render(request, "order/statusForm.html", context)

@login_required(login_url = "user:login")
def showImage(request, id, counter):
    
    order = get_object_or_404(Order, id = id)
    
    src = order.products[counter]["productImg"]
    
    context = {
                "src" : src
            }

    return render(request, "order/imageModal.html", context)

@login_required(login_url = "user:login")
def printOrders(request):
    tag = "Üretim Tablosu"
    
    translation.activate('tr')
    
    orders = Order.objects.filter()
    
    context = {
                "tag" : tag,
                "orders" : orders
            }

    return render(request, "order/printOrders.html", context)