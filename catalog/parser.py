import os
import sys
import django
from django.core.exceptions import ObjectDoesNotExist
from slugify import slugify

from requests_html import HTMLSession
from concurrent.futures import ThreadPoolExecutor


P = os.path.abspath(__file__)
P = os.path.dirname(os.path.dirname(P))
sys.path.append(P)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "books_catalog.settings")
django.setup()


from catalog.models import Book, Category, Character


cats_dict = {c.name: c for c in Category.objects.all()}


def worker(url):
    session = HTMLSession()
    response = session.get(url)
    if response.status_code != 200:
        print('ERROR', url)
        return
    try:
        name = response.html.xpath('//h1')[0].text
        description = response.html.xpath('//div[@id="description"]/span[2]')[0].text
        image = response.html.xpath('//img[@id="coverImage"]/@src')[0]
        cats = response.html.xpath('//a[@class="actionLinkLite bookPageGenreLink"]/text()')

        rows = response.html.xpath('//div[@class="clearFloats"]')

        data = {}

        for row in rows:
            key = row.xpath('//div[@class="infoBoxRowTitle"]')[0].text
            if key == 'Original Title':
                data['original_title'] = row.xpath('//div[@class="infoBoxRowItem"]')[0].text
            elif key == 'ISBN':
                data['isbn'] = row.xpath('//div[@class="infoBoxRowItem"]')[0].text
            elif key == 'Edition Language':
                data['edition_language'] = row.xpath('//div[@class="infoBoxRowItem"]')[0].text
            elif key == 'Characters':
                characters = []
                for link in row.xpath('//div[@class="infoBoxRowItem"]/a'):
                    character = Character(name=link.text, source=link.absolute_links.pop())
                    character.slug = slugify(link.text)
                    characters.append(character)
                data['characters'] = characters
            elif key == 'Literary Awards':
                data['literary_awards'] = row.xpath('//div[@class="infoBoxRowItem"]')[0].text
    except Exception as e:
        print(e, type(e), url)

    print('OK', url)

    Character.objects.bulk_create(data['characters'], ignore_conflicts=True)
    chars = Character.objects.filter(slug__in=[x.slug for x in data['characters']])

    try:
        book = Book.objects.get(name=name)
        book.original_title = data['original_title']
        book.isbn = data['isbn']
        book.edition_language = data['edition_language']
        book.literary_awards = data['literary_awards']
        book.save()
    except ObjectDoesNotExist:
        book = Book.objects.create(
            name=name,
            description=description,
            origin_image=image,
            original_title=data['original_title'],
            isbn=data['isbn'],
            edition_language=data['edition_language'],
            literary_awards=data['literary_awards'],
        )

        for cat in cats:
            category = cats_dict[cat]
            book.cats.add(category)

    for char in chars:
        book.char.add(char)


def run(start, end, threads=10):
    base_url = 'https://www.goodreads.com/book/show/{}.aaaaaa'
    urls = [base_url.format(i) for i in range(start, end)]

    with ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(worker, urls)
