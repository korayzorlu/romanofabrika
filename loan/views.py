from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

# Create your views here.

@login_required(login_url = "user:login")
def loans(request):
    tag = "Krediler"

  
    
    context = {
                "tag" : tag
            }

    return render(request, "loan/loans.html", context)