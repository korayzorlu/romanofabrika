from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from django.contrib import messages

from .models import Expense
from .forms import ExpenseForm

# Create your views here.

@login_required(login_url = "user:login")
def expenses(request):
    tag = "Giderler"
    
    expenses = Expense.objects.filter()
    
    context = {
                "tag" : tag,
                "expenses" : expenses
            }

    return render(request, "expense/expenses.html", context)

def addExpense(request):
    tag = "Gider Ekle"
    
    form = ExpenseForm(request.POST or None, request.FILES or None)
    
    if request.method == "POST":

        if form.is_valid():
            expense = form.save(commit = False)
            expense.save()

        messages.success(request, "Gider Başarıyla Eklendi...")

        return HttpResponse(status=204)

    
    context = {
                "tag" : tag,
                "form" : form
    }
    
    return render(request, 'expense/expenseForm.html', context)

def updateExpense(request, id):
    expenses = Expense.objects.filter()
    expense = get_object_or_404(Expense, id = id)
    
    form = ExpenseForm(request.POST or None, request.FILES or None, instance = expense)
    
    tag = expense.title

    if request.method == "POST":
        if form.is_valid():
            expense = form.save(commit = False)
            expense.save()
            
        messages.success(request, "Değişiklikler Kaydedildi...")

        return HttpResponse(status=204)

    context = { 
                "tag" : tag,
                "form" : form,
                "expenses" : expenses
            }

    return render(request, "expense/expenseForm.html", context)