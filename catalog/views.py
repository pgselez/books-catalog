from django.shortcuts import render


def index(request):
    response = render(request, 'home.html')
    return response


def catalog(request):
    response = render(request, 'catalog.html')
    return response
