from django.shortcuts import render
from .models import Category, Book
from . import chunks


def index(request):
    cats = [x for x in Category.objects.all()]
    context = {'categories': list(chunks(cats, 4))}
    response = render(request, 'home.html', context)
    return response


def catalog(request, **kwargs):
    slug = kwargs.get('slug', None)
    category = Category.objects.get(slug=slug)
    cats = [x for x in Category.objects.all()]
    context = {
        'categories': list(chunks(cats, 4)),
        'main_cat': category
    }
    return render(request, 'catalog.html', context)


def book(request, **kwargs):
    slug = kwargs.get('slug', None)
    book = Book.objects.get(slug=slug)
    cats = [x for x in Category.objects.all()]
    context = {
        'categories': list(chunks(cats, 4)),
        'book': book
    }
    return render(request, 'book.html', context)
