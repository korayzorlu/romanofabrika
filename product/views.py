from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from django.contrib import messages

from django.utils import translation

import json
from suds.client import Client
from suds.sudsobject import asdict
from datetime import date, timedelta, datetime


# Create your views here.

#@user_passes_test(lambda u: u.is_superuser, login_url = "/admin")
@login_required(login_url = "user:login")
def products(request):
    tag = "Ürünler"
    lineGraphTag = "Ürün Grafiği (Son 30 Gün)"
    
    client = Client("https://www.romanodizayn.com/Servis/UrunServis.svc?wsdl",location="https://www.romanodizayn.com/Servis/UrunServis.svc")
    
    urunFiltre = {"Aktif" : -1,
                  "Firsat" : -1,
                  "Indirimli" : -1,
                  "Vitrin" : -1,
                  "KategoriID" : 0,
                  "MarkaID" : 0,
                  "UrunKartiID" : 0,
                  "ToplamStokAdediBas" : 0,
                  "ToplamStokAdediSon" : 1000,
                  "TedarikciID" : 0}
    urunSayfalama = {"BaslangicIndex" : 0,
                     "KayitSayisi" : 100,
                     "SiralamaDegeri" : "YayinTarihi",
                     "SiralamaYonu" : "desc"}
    
    dd=client.service.SelectUrun("057N2SQ8WPUV1Y0QPD49RK3BBYPB3K", urunFiltre, urunSayfalama)
    
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
    
    products = newdd["UrunKarti"]
    
    print(newdd["UrunKarti"][0]["Varyasyonlar"])
    
    context = {
                "tag" : tag,
                "lineGraphTag" : lineGraphTag,
                "products" : products
            }

    return render(request, "product/products.html", context)