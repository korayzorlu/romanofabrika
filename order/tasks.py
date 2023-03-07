# Create your tasks here


from celery import shared_task

from romanofabrika.celery import app

from django.shortcuts import render, HttpResponse, redirect, get_object_or_404

from django.contrib import messages

from suds.client import Client
from suds.sudsobject import asdict

from .models import Order, Status

from datetime import datetime, timedelta

@shared_task
def add():
    
    return "test başarılı"

@shared_task
def updateOrdersTask():
    
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
                   "SiparisKaynagi" : "",
                   "SiparisKodu" : "",
                   #"SiparisTarihiBas" : datetime(2021, 1, 1),
                   "SiparisTarihiBas" : datetime.now() - timedelta(days=7),
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
    #print(ordersData[0]["TeslimatAdresi"])
    #print(ordersData[0]["TeslimatAdresi"]["Il"])
    #print(ordersData[0]["TeslimatAdresi"]["Ilce"])
    #print(ordersData[0])
   
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
                                        "productSKU" : orderProduct["StokKodu"]
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
        
        """
        #ilgili siparişlerdeki ürünlerin stok kodları
        
        if Order.objects.filter(order_id = order["ID"]).exists():
            theOrder = get_object_or_404(Order, order_id = order["ID"])
                
            for i in range(len(order["Urunler"]["WebSiparisUrun"])):
                theOrder.products[i]["productSKU"] = order["Urunler"]["WebSiparisUrun"][i]["StokKodu"]
            theOrder.save()
        """
        
        #ilgili siparişlerin adreslerini günceller
        """
        if Order.objects.filter(order_id = order["ID"]).exists():
            theOrder = get_object_or_404(Order, order_id = order["ID"])
            theOrder.cargo_address = order["TeslimatAdresi"]
            theOrder.save()
        """
                
    return "Siparişler Guncellendi"