from .models import Category


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def categories(request):
    cats = [x for x in Category.objects.all()]
    result = {'categories': list(chunks(cats, 4))}
    return result
