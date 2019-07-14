from django.shortcuts import render, redirect
from django.db.models import Count
from .models import Category, Book
from .parser import run
from threading import Thread


def index(request):
    response = render(request, 'home.html', {})
    return response


def catalog(request, **kwargs):
    slug = kwargs.get('slug', None)
    category = Category.objects.get(slug=slug)

    lang = request.GET.get('lang', None)

    if lang:
        books = Book.objects.filter(
            cats__in=[category], edition_language__iexact=lang)
    else:
        books = category.book_set.all()[0:20]

    books_langs = Book.objects.filter(cats__in=[category]).values(
        'edition_language').annotate(
        total=Count('edition_language')).order_by('-total')

    context = {
        'main_cat': category,
        'books': books,
        'languages': books_langs
    }
    return render(request, 'catalog.html', context)


def book(request, **kwargs):
    slug = kwargs.get('slug', None)
    book = Book.objects.get(slug=slug)
    context = {'book': book}
    return render(request, 'book.html', context)


def crawler(request, **kwargs):
    if request.user.is_authenticated:
        start = request.GET.get('start', 0)
        end = request.GET.get('end', 100000)
        try:
            start = int(start)
        except Exception as e:
            print(e, type(e))
            start = 0
        try:
            end = int(end)
        except Exception as e:
            print(e, type(e))
            end = 100000
        Thread(target=run, args=(start, end)).start()
    return redirect('/admin/')
