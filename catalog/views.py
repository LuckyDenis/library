from django.shortcuts import render
from django.shortcuts import HttpResponse


def index(request):
    hello = '<span class="hello"></span>'
    return HttpResponse(hello)
