from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from .models import Material

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