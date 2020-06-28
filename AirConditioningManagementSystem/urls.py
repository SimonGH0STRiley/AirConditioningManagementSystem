"""AirConditioningManagementSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import include, path
# from django.views.generic import TemplateView
from backend import views

urlpatterns = [
    path('', views.index),
    path('admin/', admin.site.urls),
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('acadminview/', views.acadminview, name='acadminview'),
    path('waiterview/', views.waiterview, name='waiterview'),
    path('managerview/', views.managerview, name='managerview'),
    path('tenantview/<char:room_id>', views.tenantview, name='tenantview'),
    # path('', views.index),
    # path('admin/', admin.site.urls),
    # path('index/', views.index),
    # path('login/', views.login),
    # path('register/', views.register),
    # path('logout/', views.logout),
    # path('acadminview/', views.acadminview),
    # path('waiterview/', views.waiterview),
    # path('managerview/', views.managerview),
    # path('tenantview/', views.tenantview),
]
