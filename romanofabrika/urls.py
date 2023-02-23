"""romanofabrika URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

from django.conf import settings
from django.conf.urls.static import static

from home.views import index, dashboard
from material.views import materials
from expense.views import expenses
from order.views import orders
from product.views import products
from finance.views import finances
from loan.views import loans

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('dashboard/', dashboard, name="dashboard"),
    path('user/', include("user.urls")),
    path('materials/', include("material.urls")),
    path('materials/', materials, name="materials"),
    path('expenses/', include("expense.urls")),
    path('expenses/', expenses, name="expenses"),
    path('orders/', include("order.urls")),
    path('orders/', orders, name="orders"),
    path('products/', include("product.urls")),
    path('products/', products, name="products"),
    path('finances/', include("finance.urls")),
    path('finances/', finances, name="finances"),
    path('loans/', include("loan.urls")),
    path('loans/', loans, name="loans"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
