from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from django.contrib import messages

from .models import Material
from .forms import MaterialForm, SourceForm, CategoryForm, UnitForm

# Create your views here.

#@user_passes_test(lambda u: u.is_superuser, login_url = "/admin")
@login_required(login_url = "user:login")
def materials(request):
    tag = "Malzemeler"
    
    materials = Material.objects.filter()
    
    context = {
                "tag" : tag,
                "materials" : materials
            }

    return render(request, "material/materials.html", context)

@login_required(login_url = "user:login")
def addMaterial(request):
    tag = "Malzeme Ekle"
    
    form = MaterialForm(request.POST or None, request.FILES or None)
    
    if request.method == "POST":

        if form.is_valid():
            material = form.save(commit = False)
            material.save()

        messages.success(request, "Malzeme Başarıyla Eklendi...")

        return HttpResponse(status=204)

    
    context = {
                "tag" : tag,
                "form" : form
    }
    
    return render(request, 'material/materialForm.html', context)

@login_required(login_url = "user:login")
def updateMaterial(request, id):
    materials = Material.objects.filter()
    material = get_object_or_404(Material, id = id)
    
    form = MaterialForm(request.POST or None, request.FILES or None, instance = material)
    
    tag = material.title

    if request.method == "POST":
        if form.is_valid():
            material = form.save(commit = False)
            material.save()
            
        messages.success(request, "Değişiklikler Kaydedildi...")

        return HttpResponse(status=204)

    context = { 
                "tag" : tag,
                "form" : form,
                "materials" : materials,
                "material" : material
            }

    return render(request, "material/materiaLForm.html", context)

@login_required(login_url = "user:login")
def getDeleteMaterial(request, id):
    material = get_object_or_404(Material, id = id)

    context = {
                "material" : material
            }
    
    return render(request, "material/deleteMaterialForm.html", context)

@login_required(login_url = "user:login")
def deleteMaterial(request, id):
    material = get_object_or_404(Material, id = id)
    
    material.delete()

    messages.success(request, "Malzeme Silindi...")
    
    return redirect("materials")

@login_required(login_url = "user:login")
def addSource(request):
    tag = "Kaynak Ekle"
    
    form = SourceForm(request.POST or None, request.FILES or None)
    
    if request.method == "POST":

        if form.is_valid():
            source = form.save(commit = False)
            source.save()

        messages.success(request, "Kaynak Başarıyla Eklendi...")

        return HttpResponse(status=204)

    context = {
                "tag" : tag,
                "form" : form
    }
    
    return render(request, 'material/sourceForm.html', context)

@login_required(login_url = "user:login")
def addCategory(request):
    tag = "Kategori Ekle"
    
    form = CategoryForm(request.POST or None, request.FILES or None)
    
    if request.method == "POST":

        if form.is_valid():
            category = form.save(commit = False)
            category.save()

        messages.success(request, "Kategori Başarıyla Eklendi...")

        return HttpResponse(status=204)

    context = {
                "tag" : tag,
                "form" : form
    }
    
    return render(request, 'material/categoryForm.html', context)

@login_required(login_url = "user:login")
def addUnit(request):
    tag = "Birim Ekle"
    
    form = UnitForm(request.POST or None, request.FILES or None)
    
    if request.method == "POST":

        if form.is_valid():
            unit = form.save(commit = False)
            unit.save()

        messages.success(request, "Birim Başarıyla Eklendi...")

        return HttpResponse(status=204)

    context = {
                "tag" : tag,
                "form" : form
    }
    
    return render(request, 'material/unitForm.html', context)