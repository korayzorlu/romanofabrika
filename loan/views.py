from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from django.contrib import messages

from django.utils import translation

from .forms import LoanForm, InstallmentStatusForm

from datetime import datetime
import calendar
import json
from dateutil.relativedelta import relativedelta
import ast

from .models import Loan, InstallmentStatus

# Create your views here.

@login_required(login_url = "user:login")
def loans(request):
    tag = "Krediler"
    
    translation.activate('tr')
    
    loans = Loan.objects.filter()
    
    for loan in loans:
        installmentStatuses = []
        for installment in loan.installments:
            installmentStatuses.append(installment["installmentStatus"])
        loan.completed_installment = installmentStatuses.count("Ödendi")
            
        for installment in loan.installments:
            if datetime.strptime(installment["installmentDate"], "%Y-%m-%d").date() > datetime.now().date():
                #print("Gelecek Taksit: " + str(installment["installmentDate"]))
                if installment["installmentStatus"] == "Ödenmedi":
                    loan.next_installment = datetime.strptime(installment["installmentDate"], "%Y-%m-%d").date()
                    loan.save()
                    break
        
        
        loan.save()
    
    nowDate = datetime.now().date()

        
    
    context = {
                "tag" : tag,
                "loans" : loans,
                "nowDate" : nowDate
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
                installments.append({"installmentDate" : str(start_date),
                                     "installmentNo" : count + 1,
                                     "installmentAmount" : round(loan.total_debt / (loan.installment_count - loan.installment_deferral),2),
                                     "installmentStatus" : ""})
                start_date = start_date + relativedelta(months=1)
                
            loan.installments = installments
            loan.save()
            
            
            
            messages.success(request, "Kredi Başarıyla Eklendi...")

            return HttpResponse(status=204)

    
    context = {
                "tag" : tag,
                "form" : form
    }
    
    return render(request, 'loan/loanForm.html', context)

@login_required(login_url = "user:login")
def updateLoan(request, id):
    installmentStatus = get_object_or_404(InstallmentStatus, id = 3)
    loan = get_object_or_404(Loan, id = id)
    
    form = LoanForm(request.POST or None, request.FILES or None, instance = loan)
    
    tag = loan.title

    if request.method == "POST":
        if form.is_valid():
            loan = form.save(commit = False)
            
            installments = []
            start_date = loan.start_date
            print(start_date + relativedelta(months=1))
            start_date = start_date + relativedelta(months=loan.installment_deferral)
            for count in range(loan.installment_count):
                installments.append({"installmentDate" : str(start_date),
                                     "installmentNo" : count + 1,
                                     "installmentAmount" : round(loan.total_debt / (loan.installment_count - loan.installment_deferral),2),
                                     "installmentStatus" : installmentStatus.title})
                start_date = start_date + relativedelta(months=1)
                
            loan.installments = installments
            
            loan.save()
            
        messages.success(request, "Değişiklikler Kaydedildi...")

        return HttpResponse(status=204)

    context = { 
                "tag" : tag,
                "form" : form,
                "loan" : loan
            }

    return render(request, "loan/loanForm.html", context)

@login_required(login_url = "user:login")
def updateInstallmentStatus(request, id):
    loan = get_object_or_404(Loan, id = id)
    
    installmentStatuses = InstallmentStatus.objects.filter()
    
    form = InstallmentStatusForm(request.POST or None, request.FILES or None, instance = loan)
    
    tag = loan.title

    if request.method == "POST":
        print(form.data)
        if form.is_valid():
            print(form.data)
            formDataList = form.data.getlist("installment_status")
            for i in range(loan.installment_count):
                theStatus = get_object_or_404(InstallmentStatus, id = int(formDataList[i]))
                loan.installments[i]["installmentStatus"] = theStatus.title
            loan.save()
            
        messages.success(request, "Değişiklikler Kaydedildi...")

        return HttpResponse(status=204)

    context = { 
                "tag" : tag,
                "form" : form,
                "loan" : loan,
                "installmentStatuses" : installmentStatuses
            }

    return render(request, "loan/installmentStatusForm.html", context)

@login_required(login_url = "user:login")
def getDeleteLoan(request, id):
    loan = get_object_or_404(Loan, id = id)

    context = {
                "loan" : loan
            }
    
    return render(request, "loan/deleteLoanForm.html", context)

@login_required(login_url = "user:login")
def deleteLoan(request, id):
    loan = get_object_or_404(Loan, id = id)
    
    loan.delete()

    messages.success(request, "Kredi Silindi...")
    
    return redirect("loans")