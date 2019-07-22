from django.db.models import Count
from .models import Category


def categories(request):
    cats = Category.objects.annotate(
        books_count=Count('book')).order_by('-books_count')[:40]
    result = {'categories': cats}
    return result
