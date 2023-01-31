from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from django.contrib import messages
from django.http import FileResponse

from django.utils import timezone

from .models import Expense, Company, Category, Unit
from .forms import ExpenseForm, CompanyForm, ExcelForm

from datetime import date, timedelta
import pandas as pd

# Create your views here.

@login_required(login_url = "user:login")
def expenses(request):
    tag = "Giderler"
    
    expenses = Expense.objects.filter()
    
    #Line Graph
    days = []

    for i in range(31):
        days.append((timezone.now().date()-timedelta(days=i)).isoformat())

    days.reverse()
    
    dataExpenses = []
    
    for day in days:
        dailyExpense = []
        for expense in expenses:
            if str(expense.created_date) == str(day):
                print(day)
                dailyExpense.append(float(expense.total))
            else:
                dailyExpense.append(0)
        dataExpenses.append(sum(dailyExpense))
    
    print(dataExpenses)
    
    print(days)

    lineData = []

    for i in range(31):
        lineData.append({
            "day" : days[i],
            "data" : dataExpenses[i]
        })
    print(lineData)
    context = {
                "tag" : tag,
                "expenses" : expenses,
                "lineData" : lineData
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

def addExpenseBatch(request):
    tag = "Excel İle Gider Ekle"

    expenses = Expense.objects.filter()

    form = ExcelForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
        if form.is_valid():
            newfile = form.save(commit = False)
            newfile.save()

            if request.FILES.getlist("file") == []:
                messages.info(request, "Dosya Bulunamadı!")
                return redirect("product:addproductbatch")
            try:
                data = pd.read_excel(str(newfile.file.path))
                df = pd.DataFrame(data)
            except ValueError:
                newfile.delete()
                messages.info(request, "Şablon Excel formatında olmalıdır!")
                return redirect("expenses")

            try:
                for i in range(len(df["ÜRÜN BAŞLIĞI"])):
                    if pd.isnull(df["ÜRÜN BAŞLIĞI"][i]):
                        newfile.delete()
                        messages.info(request, "Şablon Hatalı! Ürün başlığı giriniz ve tekrar deneyiniz.")
                        return redirect("expenses")
                    
                    #####Select'lerde hücre boşsa default değeri bulup doldurmak#####
                    try:
                        company = get_object_or_404(Company, title = df["FİRMA"][i])
                    except:
                        if pd.isnull(df["FİRMA"][i]):
                            defaultCompanyId = Expense._meta.get_field('company').get_default()
                            defaultCompany = get_object_or_404(Company, id = defaultCompanyId)
                            company = defaultCompany
                        else:
                            company = Company.objects.create(title = df["FİRMA"][i])
                    try:
                        category = get_object_or_404(Category, title = df["KATEGORİ"][i])
                    except:
                        if pd.isnull(df["KATEGORİ"][i]):
                            defaultCategoryId = Expense._meta.get_field('category').get_default()
                            defaultCategory = get_object_or_404(Category, id = defaultCategoryId)
                            category = defaultCategory
                        else:
                            category = Category.objects.create(title = df["KATEGORİ"][i])
                    try:
                        unit = get_object_or_404(Unit, title = df["BİRİM"][i])
                    except:
                        if pd.isnull(df["BİRİM"][i]):
                            defaultUnitId = Expense._meta.get_field('unit').get_default()
                            defaultUnit= get_object_or_404(Unit, id = defaultUnitId)
                            unit = defaultUnit
                        else:
                            unit = Unit.objects.create(title = df["BİRİM"][i])
                    #######################################################################
                    
                    newexpense = Expense.objects.create(
                        created_date = df["TARİH"][i],
                        company = company,
                        category = category,
                        title = df["ÜRÜN BAŞLIĞI"][i],
                        unit = unit,
                        quantity = df["MİKTAR"][i],
                        price = df["BİRİM TUTAR"][i],
                        )
            except KeyError:
                newfile.delete()
                messages.info(request, "Şablon Hatalı! Sütun başlıklarını kontrol ediniz ve tekrar deneyiniz.")
                return redirect("expenses")

            except ValueError as e:
                print(e)
                newfile.delete()
                messages.info(request, "Şablon Hatalı! Sayı girilmesi gereken alanlara karakter girilmediğini veya boş bırakılmadığını kontrol ediniz ve tekrar deneyiniz.")
                return redirect("expenses")

            newfile.delete()

        messages.success(request, "Ürün Başarıyla Eklendi...")

        return redirect("expenses")

    context = { 
                "tag" : tag,
                "form" : form,
                "expenses" : expenses,
            }

    return render(request, "expense/expenseBatchForm.html", context)

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
                "expenses" : expenses,
                "expense" : expense
            }

    return render(request, "expense/expenseForm.html", context)

def getDeleteExpense(request, id):
    expense = get_object_or_404(Expense, id = id)

    context = {
                "expense" : expense
            }
    
    return render(request, "expense/deleteExpenseForm.html", context)

def deleteExpense(request, id):
    expense = get_object_or_404(Expense, id = id)
    
    expense.delete()

    messages.success(request, "Gider Silindi...")
    
    return redirect("expenses")

def addCompany(request):
    tag = "Firma Ekle"
    
    form = CompanyForm(request.POST or None, request.FILES or None)
    
    if request.method == "POST":

        if form.is_valid():
            company = form.save(commit = False)
            company.save()

        messages.success(request, "Firma Başarıyla Eklendi...")

        return HttpResponse(status=204)

    
    context = {
                "tag" : tag,
                "form" : form
    }
    
    return render(request, 'expense/companyForm.html', context)

def downloadExpenseExcel(request):
    response = FileResponse(open('./excelfile/add-expense.xlsx', 'rb'))
    return response