from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

# Create your views here.


def pageNotFound(request, exception):
    return HttpResponseNotFound(f'<h1>Sorry, page not found</h1>')



