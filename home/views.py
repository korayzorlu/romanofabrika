from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url = "/admin")
def index(request):

    return render(request, "index/index.html")