from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from django.contrib import messages
from django.http import FileResponse

from django.utils import timezone

from .models import Expense, Company, Category, Unit
from .forms import ExpenseForm, CompanyForm, ExcelForm, CategoryForm, UnitForm

from datetime import date, timedelta
import pandas as pd

# Create your views here.

@login_required(login_url = "user:login")
def expenses(request):
    tag = "Giderler"
    
    expenses = Expense.objects.filter().order_by("-created_date")
    categories = Category.objects.filter()
    
    testtest = get_object_or_404(Expense, id = 89)
    testtest.title = "asdtesttest123"
    testtest.save()
    print(timezone.now().time())
    
    #####Line Graph#####
    days = []

    for i in range(31):
        days.append((timezone.now().date()-timedelta(days=i)).isoformat())

    days.reverse()
    
    dataExpenses = []
    
    for day in days:
        dailyExpense = []
        for expense in expenses:
            if str(expense.created_date) == str(day):
                dailyExpense.append(float(expense.total))
            else:
                dailyExpense.append(0)
        dataExpenses.append(sum(dailyExpense))
    
    lineData = []

    for i in range(31):
        lineData.append({
            "day" : days[i],
            "data" : round(dataExpenses[i],2)
        })
    
    ########################
    
    #####Pie Graph#####
    dataCategory = []
    dataTotal = []
    
    for category in categories:
        categoryExpense = []
        for expense in expenses:
            if str(expense.category) == str(category.title):
                categoryExpense.append(float(expense.total))
        dataCategory.append(category.title)
        dataTotal.append(sum(categoryExpense))
    
    pieData = []
    
    for i in range(len(dataCategory)):
        pieData.append({
            "category" : dataCategory[i],
            "data" : round(dataTotal[i],2)
        })

    ##########################
    
    context = {
                "tag" : tag,
                "expenses" : expenses,
                "lineData" : lineData,
                "pieData" : pieData
            }

    return render(request, "expense/expenses.html", context)

@login_required(login_url = "user:login")
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

@login_required(login_url = "user:login")
def downloadExpenseExcel(request):
    response = FileResponse(open('./excelfile/add-expense.xlsx', 'rb'))
    return response


@login_required(login_url = "user:login")
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
                return HttpResponse(status=204)
            try:
                data = pd.read_excel(str(newfile.file.path))
                df = pd.DataFrame(data)
            except ValueError:
                newfile.delete()
                messages.info(request, "Şablon Excel formatında olmalıdır!")
                return HttpResponse(status=204)

            try:
                for i in range(len(df["ÜRÜN BAŞLIĞI"])):
                    if pd.isnull(df["ÜRÜN BAŞLIĞI"][i]):
                        newfile.delete()
                        messages.info(request, "Bazı ürün/ürünlerin başlığı girilmemiş! Lütfen boş olan başlıkları doldurup tekrar deneyin...")
                        return HttpResponse(status=204)
                    
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
                return HttpResponse(status=204)

            except ValueError as e:
                print(e)
                newfile.delete()
                messages.info(request, "Şablon Hatalı! Sayı girilmesi gereken alanlara karakter girilmediğini veya boş bırakılmadığını kontrol ediniz ve tekrar deneyiniz.")
                return HttpResponse(status=204)

            newfile.delete()

        messages.success(request, "Ürün Başarıyla Eklendi...")

        return HttpResponse(status=204)

    context = { 
                "tag" : tag,
                "form" : form,
                "expenses" : expenses,
            }

    return render(request, "expense/expenseBatchForm.html", context)

@login_required(login_url = "user:login")
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

@login_required(login_url = "user:login")
def getDeleteExpense(request, id):
    expense = get_object_or_404(Expense, id = id)

    context = {
                "expense" : expense
            }
    
    return render(request, "expense/deleteExpenseForm.html", context)

@login_required(login_url = "user:login")
def deleteExpense(request, id):
    expense = get_object_or_404(Expense, id = id)
    
    expense.delete()

    messages.success(request, "Gider Silindi...")
    
    return redirect("expenses")

@login_required(login_url = "user:login")
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
    
    return render(request, 'expense/categoryForm.html', context)

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
    
    return render(request, 'expense/unitForm.html', context)