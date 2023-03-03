from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from django.contrib import messages

from django.utils import translation

from .models import Category, Product
from .tasks import add

import json
from suds.client import Client
from suds.sudsobject import asdict
from datetime import date, timedelta, datetime

from celery.result import AsyncResult


# Create your views here.

#@user_passes_test(lambda u: u.is_superuser, login_url = "/admin")
@login_required(login_url = "user:login")
def products(request):
    tag = "Ürünler"
    
    translation.activate('tr')
    
    #add.delay()
    
    products = Product.objects.filter()
    
    context = {
                "tag" : tag,
                "products" : products
            }

    return render(request, "product/products.html", context)

@login_required(login_url = "user:login")
def updateProducts(request):
    tag = "Ürünler"
    
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
                     "KayitSayisi" : 5,
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
    
    productsData = newdd["UrunKarti"]
    
    for product in productsData:
        if not Product.objects.filter(product_id = product["ID"]).exists():
            theCategory = get_object_or_404(Category, category_id = product["AnaKategoriID"])
            productVariations = []
            
            try:
                for productVariation in product["Varyasyonlar"]["Varyasyon"]:
                    productVariations.append({"variationID" : productVariation["ID"],
                                              "variationBarcode" : productVariation["Barkod"],
                                              "variationSKU" : productVariation["StokKodu"],
                                              "variationQuantity" : float(productVariation["StokAdedi"]),
                                              "variationSalePrice" : float(productVariation["SatisFiyati"]),
                                              "variationDiscountPrice" : float(productVariation["IndirimliFiyati"]),
                                              "variationCartPrice" : 0.00})
                newProduct = Product(product_status = product["Aktif"],
                                     product_id = product["ID"],
                                     title = product["UrunAdi"],
                                     category = theCategory,
                                     categories = product["Kategoriler"]["int"],
                                     description = product["Aciklama"],
                                     images = product["Resimler"]["string"],
                                     special_3 = product["OzelAlan3"],
                                     special_4 = product["OzelAlan4"],
                                     special_5 = product["OzelAlan5"],
                                     variations = productVariations)
                newProduct.save()
                theProduct = get_object_or_404(Product, product_id = product["ID"])
                for i in range(len(theProduct.variations)):
                    if theProduct.special_3 == "%30" or theProduct.special_3 == "30%":
                        theProduct.variations[i]["variationCartPrice"] = theProduct.variations[i]["variationDiscountPrice"] * 0.7
                    if theProduct.special_4 == "%40" or theProduct.special_4 == "40%":
                        theProduct.variations[i]["variationCartPrice"] = theProduct.variations[i]["variationDiscountPrice"] * 0.6
                    if theProduct.special_5 == "%50" or theProduct.special_5 == "50%":
                        theProduct.variations[i]["variationCartPrice"] = theProduct.variations[i]["variationDiscountPrice"] * 0.5
                theProduct.save()
            except Exception as e:
                print(e)
                
        if Product.objects.filter(product_id = product["ID"]).exists():
            theCategory = get_object_or_404(Category, category_id = product["AnaKategoriID"])
            theProduct = get_object_or_404(Product, product_id = product["ID"])
            productVariations = []
            
            try:
                for productVariation in product["Varyasyonlar"]["Varyasyon"]:
                    productVariations.append({"variationID" : productVariation["ID"],
                                              "variationBarcode" : productVariation["Barkod"],
                                              "variationSKU" : productVariation["StokKodu"],
                                              "variationQuantity" : float(productVariation["StokAdedi"]),
                                              "variationSalePrice" : float(productVariation["SatisFiyati"]),
                                              "variationDiscountPrice" : float(productVariation["IndirimliFiyati"]),
                                              "variationCartPrice" : 0.00})
                theProduct.product_status = product["Aktif"]
                theProduct.product_id = product["ID"]
                theProduct.title = product["UrunAdi"]
                theProduct.category = theCategory
                theProduct.categories = product["Kategoriler"]["int"]
                theProduct.description = product["Aciklama"]
                theProduct.images = product["Resimler"]["string"]
                theProduct.special_3 = product["OzelAlan3"]
                theProduct.special_4 = product["OzelAlan4"]
                theProduct.special_5 = product["OzelAlan5"]
                theProduct.variations = productVariations
                theProduct.save()
                theProduct = get_object_or_404(Product, product_id = product["ID"])
                for i in range(len(theProduct.variations)):
                    if theProduct.special_3 == "%30" or theProduct.special_3 == "30%":
                        theProduct.variations[i]["variationCartPrice"] = theProduct.variations[i]["variationDiscountPrice"] * 0.7
                    if theProduct.special_4 == "%40" or theProduct.special_4 == "40%":
                        theProduct.variations[i]["variationCartPrice"] = theProduct.variations[i]["variationDiscountPrice"] * 0.6
                    if theProduct.special_5 == "%50" or theProduct.special_5 == "50%":
                        theProduct.variations[i]["variationCartPrice"] = theProduct.variations[i]["variationDiscountPrice"] * 0.5
                theProduct.save()
            except Exception as e:
                print(e)
                
    messages.success(request, "Ürünler Güncellendi")
    
    return redirect("products")

@login_required(login_url = "user:login")
def updateCategories(request):
    tag = "Ürünler"
    
    client = Client("https://www.romanodizayn.com/Servis/UrunServis.svc?wsdl",location="https://www.romanodizayn.com/Servis/UrunServis.svc")
    
    dd=client.service.SelectKategori("057N2SQ8WPUV1Y0QPD49RK3BBYPB3K", 0, "")
    
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
    
    categoriesData = newdd["Kategori"]
    
    for i in range(2):
        for category in categoriesData:
            print(category["PID"])
            if not Category.objects.filter(category_id = int(category["ID"])).exists():
                if not Category.objects.filter(category_id = int(category["PID"])).exists():
                    newCategory = Category(category_id = int(category["ID"]),
                                        title = category["Tanim"])
                    newCategory.save()
                else:
                    theParent = get_object_or_404(Category, category_id = category["PID"])
                    newCategory = Category(category_id = int(category["ID"]),
                                        title = category["Tanim"],
                                        parent = theParent)
                    newCategory.save()
            if Category.objects.filter(category_id = int(category["ID"])).exists():
                if Category.objects.filter(category_id = int(category["PID"])).exists():
                    theCategory = get_object_or_404(Category, category_id = category["ID"])
                    theParent = get_object_or_404(Category, category_id = category["PID"])
                    theCategory.parent = theParent
                    theCategory.save()
                
    messages.success(request, "Kategoriler Güncellendi")
    
    return redirect("products")

@login_required(login_url = "user:login")
def showImage(request, id):
    
    product = get_object_or_404(Product, id = id)
    
    src = product.images[0]
    
    context = {
                "src" : src
            }

    return render(request, "product/imageModal.html", context)