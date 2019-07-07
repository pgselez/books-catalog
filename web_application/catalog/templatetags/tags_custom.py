from django import template
from catalog.models import Category


register = template.Library()


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


@register.simple_tag(name='tags_categories')
def tags_categories():
    cats = [x for x in Category.objects.all()]
    return list(chunks(cats, 4))


@register.filter(name='s_upper')
def s_upper(string):
    r = ''
    for n, s in enumerate(string):
        if n % 2 == 0:
            r += s.upper()
        else:
            r += s.lower()
    return r
