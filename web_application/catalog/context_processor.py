from django.db.models import Count
from .models import Category


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def categories(request):
    cats = Category.objects.annotate(
        books_count=Count('book')).order_by('-books_count')[:40]
    result = {'categories': cats}
    return result
