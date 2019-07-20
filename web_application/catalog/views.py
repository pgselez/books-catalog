from django.shortcuts import render, redirect, reverse
from django.db.models import Count

from django.views.generic import TemplateView, DetailView, ListView

from .models import Category, Book
from .parser import run
from threading import Thread


class IndexView(TemplateView):
    template_name = "home.html"


class CatalogView(DetailView):
    model = Category
    template_name = 'catalog.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        books_langs = Book.objects.filter(cats__in=[context['object']]).values(
                'edition_language').annotate(
                total=Count('edition_language')).order_by('-total')
        context['languages'] = books_langs
        return context


class BookListView(ListView):
    model = Book
    template_name = 'catalog.html'
    paginate_by = 40

    def get_queryset(self):
        cat_slug = self.kwargs.get('slug')
        self.category = Category.objects.get(slug=cat_slug)
        lang = self.request.GET.get('lang', None)
        if lang:
            books = Book.objects.filter(
                cats__in=[self.category], edition_language__iexact=lang)
        else:
            books = Book.objects.filter(cats__in=[self.category])
        return books.prefetch_related('photo_set')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        books_langs = Book.objects.filter(
            cats__in=[self.category]).values(
            'edition_language').annotate(
            total=Count('edition_language')).order_by('-total')
        context['languages'] = books_langs
        context['main_cat'] = self.category
        return context


class BookView(DetailView):
    model = Book
    template_name = 'book.html'


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
