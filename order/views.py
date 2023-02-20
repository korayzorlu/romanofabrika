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
    client = Client("https://www.romanodizayn.com/Servis/SiparisServis.svc?wsdl",location="https://www.romanodizayn.com/Servis/SiparisServis.svc")
    
    siparisEntegrasyon = {"AlanDeger" : "", "Deger" : "", "EntegrasyonKodu" : "", "EntegrasyonParamsAktif" : True, "TabloAlan" : "", "Tanim" : ""}
    siparisFiltre={"EntegrasyonAktarildi" : -1,
                   "EntegrasyonParams" : siparisEntegrasyon,
                   "IptalEdilmisUrunler" : True,
                   "FaturaNo" : "",
                   "OdemeDurumu" : 1,
                   "OdemeTipi" : -1,
                   "SiparisDurumu" : -1,
                   "SiparisID" : -1,
                   "SiparisKaynagi" : "TicimaxWeb",
                   "SiparisKodu" : "",
                   "SiparisTarihiBas" : datetime(2022, 9, 1),
                   #"SiparisTarihiSon" : datetime(2023, 2, 9),
                   "StrSiparisDurumu" : "",
                   "TedarikciID" : -1,
                   "UyeID" : -1,
                   "SiparisNo" : "",
                   "UyeTelefon" : ""}
    siparisSayfalama={"SiralamaYonu" : "Desc"}

    dd=client.service.SelectSiparis("057N2SQ8WPUV1Y0QPD49RK3BBYPB3K", siparisFiltre, siparisSayfalama)
    
    def recursive_dict(d):
        out = {}
        for k, v in asdict(d).items():
            if hasattr(v, '__keylist__'):
                out[k] = recursive_dict(v)
            elif isinstance(v, list):
                out[k] = []
                for item in v:
                    if hasattr(item, '__keylist__'):
                        out[k].append(recursive_dict(item))
                    else:
                        out[k].append(item)
            else:
                out[k] = v
        return out
    
    newdd = recursive_dict(dd)
    
    ordersData = newdd["WebSiparis"]
    print(ordersData[0]["TeslimatAdresi"])
    print(ordersData[0]["TeslimatAdresi"]["Il"])
    print(ordersData[0]["TeslimatAdresi"]["Ilce"])
    print(ordersData[0])
   
    for order in ordersData:
        if not Order.objects.filter(order_id = order["ID"]).exists():
            theStatus = get_object_or_404(Status, id = 1)
            orderProducts = []
           
            try:
                for orderProduct in order["Urunler"]["WebSiparisUrun"]:
                    orderProducts.append({"productName" : str(orderProduct["UrunAdi"]),
                                        "productImg" : str(orderProduct["ResimYolu"]),
                                        "productID" : int(orderProduct["UrunKartiID"]),
                                        "productStatus" : theStatus.title,
                                        "productPrice" : round(float(orderProduct["Tutar"]) + float(orderProduct["KdvTutari"]), 2),
                                        "productQuantity" : float(orderProduct["Adet"]),
                                        "productTotal" : round(float(orderProduct["Tutar"]) + float(orderProduct["KdvTutari"]), 2) * float(orderProduct["Adet"]),
                                        "productSKU" : float(orderProduct["StokKodu"])
                                        })
                newOrder = Order(order_id = order["ID"],
                                order_date = order["SiparisTarihi"].date(),
                                customer_name = order["AdiSoyadi"],
                                products = orderProducts,
                                cargo_address = order["TeslimatAdresi"],
                                total = round(order["SiparisToplamTutari"],2))
                newOrder.save()
            except:
                print("-----------")
                print("ID: " + str(order["ID"]) + " - siparişte ürün yok")
                print("-----------")
            
        #ihtiyaç halinde toplu güncelleme yapılmak istenirse bu alanı kullan
        """
        if Order.objects.filter(order_id = order["ID"]).exists():
            theOrder = get_object_or_404(Order, order_id = order["ID"])
            theStatus = get_object_or_404(Status, id = 11)
            orderProducts = []
            for orderProduct in order["Urunler"]["WebSiparisUrun"]:
                orderProducts.append({"productName" : str(orderProduct["UrunAdi"]),
                                      "productImg" : str(orderProduct["ResimYolu"]),
                                      "productID" : int(orderProduct["UrunKartiID"]),
                                      "productStatus" : theStatus.title,
                                      "productPrice" : round(float(orderProduct["Tutar"]) + float(orderProduct["KdvTutari"]), 2),
                                      "productQuantity" : float(orderProduct["Adet"]),
                                      "productTotal" : round(float(orderProduct["Tutar"]) + float(orderProduct["KdvTutari"]), 2) * float(orderProduct["Adet"])
                                      })
            theOrder.products = orderProducts
            theOrder.total = round(order["SiparisToplamTutari"],2)
            theOrder.save()
        """
        #ilgili aydaki tüm siparişlerdeki ürün durumlarını teslim edildi yapar
        """
        if Order.objects.filter(order_id = order["ID"]).exists():
            theOrder = get_object_or_404(Order, order_id = order["ID"])
            if theOrder.order_date.month == 9:
                for i in range(len(theOrder.products)):
                    theOrder.products[i]["productStatus"] = "Müşteriye Teslim Edildi"
            theOrder.save()
        """
        #ilgili siparişlerdeki ürünlerin stok kodları
        
        if Order.objects.filter(order_id = order["ID"]).exists():
            theOrder = get_object_or_404(Order, order_id = order["ID"])
                
            for i in range(len(order["Urunler"]["WebSiparisUrun"])):
                theOrder.products[i]["productSKU"] = order["Urunler"]["WebSiparisUrun"][i]["StokKodu"]
            theOrder.save()
        
        #ilgili siparişlerin adreslerini günceller
        """
        if Order.objects.filter(order_id = order["ID"]).exists():
            theOrder = get_object_or_404(Order, order_id = order["ID"])
            theOrder.cargo_address = order["TeslimatAdresi"]
            theOrder.save()
        """
    messages.success(request, "Siparişler Güncellendi")
    
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