from django.shortcuts import render
from django.http import HttpResponseBadRequest
from .models import Category


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def index(request):
    cats = [x for x in Category.objects.all()]
    context = {'categories': list(chunks(cats, 4))}
    response = render(request, 'home.html', context)
    return response


def catalog(request, **kwargs):

    breakpoint()

    slug = kwargs.get('slug', None)
    if not slug:
        return HttpResponseBadRequest()

    category = Category.objects.get(slug=slug)
    books = category.book_set.all()

    cats = [x for x in Category.objects.all()]
    context = {
        'categories': list(chunks(cats, 4)),
        'books': books,
        'main_cat': category
    }
    response = render(request, 'catalog.html', context)
    return response
