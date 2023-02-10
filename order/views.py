from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from django.utils import translation

import json
from suds.client import Client
from suds.sudsobject import asdict
from datetime import date, timedelta, datetime


# Create your views here.

#@user_passes_test(lambda u: u.is_superuser, login_url = "/admin")
@login_required(login_url = "user:login")
def orders(request):
    tag = "Siparişler"
    
    
    
    context = {
                "tag" : tag
            }

    return render(request, "order/orders.html", context)

@login_required(login_url = "user:login")
def updateOrders(request):
    tag = "Siparişler"
    
    translation.activate('tr')
    
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
                   "SiparisTarihiBas" : datetime(2022, 11, 1),
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
    
    orders = newdd["WebSiparis"]
    
    today = datetime.today()
    
    print(newdd["WebSiparis"][0]["Urunler"]["WebSiparisUrun"])
    
    context = {
                "tag" : tag,
                "orders" : orders,
                "today" : today
            }

    return render(request, "order/orders.html", context)