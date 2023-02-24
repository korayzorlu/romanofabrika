from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from django.contrib import messages

from .forms import LoanForm

# Create your views here.

@login_required(login_url = "user:login")
def loans(request):
    tag = "Krediler"

  
    
    context = {
                "tag" : tag
            }

    return render(request, "loan/loans.html", context)

@login_required(login_url = "user:login")
def addLoan(request):
    tag = "Kredi Ekle"
    
    form = LoanForm(request.POST or None, request.FILES or None)
    
    if request.method == "POST":
        print(form.errors.values())
        if form.is_valid():
            loan = form.save(commit = False)
            loan.save()
            
            messages.success(request, "Gider Başarıyla Eklendi...")

            return HttpResponse(status=204)

    
    context = {
                "tag" : tag,
                "form" : form
    }
    
    return render(request, 'loan/loanForm.html', context)