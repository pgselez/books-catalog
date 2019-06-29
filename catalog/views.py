from django.shortcuts import render
from .models import Category


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def index(request):

    cats = [x for x in Category.objects.all()]

    context = {
        'categories': chunks(cats, 4)
    }
    response = render(request, 'home.html', context)
    return response


def catalog(request):
    response = render(request, 'catalog.html')
    return response
