import random
from django.shortcuts import render, redirect, reverse
from django.db.models import Count

from django.http import JsonResponse

from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin


from django.views.generic import TemplateView, DetailView, ListView
from django.contrib import messages

from .models import Category, Book, Review
from .forms import ReviewForm, SearchForm
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


class BookListView(SingleObjectMixin, ListView):
    model = Book
    template_name = 'catalog.html'
    paginate_by = 40

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Category.objects.all())
        self.lang = self.request.GET.get('lang', None)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if self.lang:
            return self.object.book_set.filter(edition_language__iexact=self.lang)
        else:
            return self.object.book_set.all().prefetch_related('photo_set')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        books_langs = self.object.book_set.all().values(
            'edition_language').annotate(
            total=Count('edition_language')).order_by('-total')
        context['languages'] = books_langs
        context['main_cat'] = self.object
        return context


class BookView(FormMixin, DetailView):
    model = Book
    form_class = ReviewForm
    template_name = 'book.html'

    def get_success_url(self):
        return reverse('book', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReviewForm()
        context['author_books'] = Book.objects.filter(owner=self.object.owner)[:5]

        _cats = [c.id for c in self.object.cats.all()]

        cat_books_ids = Book.objects.filter(cats__in=_cats).values('id')

        ids = [x['id'] for x in cat_books_ids]
        random.shuffle(ids)
        books_ids = ids[:16]

        context['random_books'] = Book.objects.filter(id__in=books_ids)
        return context

    def post(self, request, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            Review.objects.create(
                book=self.object,
                nickname=form.cleaned_data['nickname'],
                summary=form.cleaned_data['summary'],
                review=form.cleaned_data['message']
            )
            # if request.is_ajax():
            #     return JsonResponse(data={'status': 'all is ok!'})
            messages.add_message(request, messages.INFO,
                                 'Your review is on moderation')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class SearchView(FormMixin, ListView):
    model = Book
    form_class = SearchForm
    template_name = 'search.html'
    paginate_by = 36

    def get_success_url(self):
        return reverse('search')

    def get(self, request, *args, **kwargs):
        self.keyword = self.request.GET.get('q')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(name__search=self.keyword)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = self.keyword
        return context


def crawler(request, **kwargs):
    if request.user.is_authenticated:
        last = Book.objects.latest('goodreads_id')
        end = 100000000000
        try:
            start = int(last.goodreads_id)
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
