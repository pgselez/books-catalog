from django.shortcuts import render, redirect
from .models import Category, Book
from .parser import run
from threading import Thread


def index(request):
    response = render(request, 'home.html', {})
    return response


def catalog(request, **kwargs):
    slug = kwargs.get('slug', None)
    category = Category.objects.get(slug=slug)
    context = {'main_cat': category}
    return render(request, 'catalog.html', context)


def book(request, **kwargs):
    slug = kwargs.get('slug', None)
    book = Book.objects.get(slug=slug)
    context = {'book': book}
    return render(request, 'book.html', context)


def crawler(request, **kwargs):
    if request.user.is_authenticated:
        Thread(target=run, args=(10000, 15000)).start()
    return redirect('/admin/')
