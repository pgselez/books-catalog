import random
from django.db.models import Count
from .models import Category, Tag


def categories(request):
    cats = Category.objects.annotate(
        books_count=Count('book')).order_by('-books_count')[:40]
    result = {'categories': cats}
    return result


def tags(request):
    count = Tag.objects.all().count()
    slice = random.randint(0, count-20) if count > 20 else 0
    tags = Tag.objects.all()[slice: slice + 20]
    result = {'tags': tags}
    return result
