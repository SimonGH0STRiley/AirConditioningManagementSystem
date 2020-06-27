from django.shortcuts import render, HttpResponse
from backend import models


# Create your views here.

def fun(request):
    t = models.Record.objects.all()
    print(t)
    return HttpResponse("ok")
