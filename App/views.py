from django.shortcuts import render
import pymongo
# Create your views here.


def index(request):
    return render(request, 'index.html')


def index_test(request):
    return render(request, 'test.html')
