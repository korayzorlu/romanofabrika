from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from django.contrib import messages

from .forms import LoanForm

from datetime import datetime
import calendar
import json
from dateutil.relativedelta import relativedelta

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
        if form.is_valid():
            loan = form.save(commit = False)
            loan.save()
            
            installments = []
            start_date = loan.start_date
            print(start_date + relativedelta(months=1))
            start_date = start_date + relativedelta(months=loan.installment_deferral)
            for count in range(loan.installment_count):
                installments.append({"Taksit Tarihi" : str(start_date),
                                     "Taksit No" : count + 1,
                                     "Taksit Tutarı" : round(loan.amount / (loan.installment_count - loan.installment_deferral),2),
                                     "Taksit Durumu" : ""})
                start_date = start_date + relativedelta(months=1)
                
            loan.installments = installments
            loan.save()
            print(loan.installments)
            
            
            
            messages.success(request, "Kredi Başarıyla Eklendi...")

            return HttpResponse(status=204)

    
    context = {
                "tag" : tag,
                "form" : form
    }
    
    return render(request, 'loan/loanForm.html', context)