import os
import sys
import django

from requests_html import HTMLSession
from concurrent.futures import ThreadPoolExecutor


P = os.path.abspath(__file__)
P = os.path.dirname(os.path.dirname(P))
sys.path.append(P)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "books_catalog.settings")
django.setup()


from catalog.models import Book, Category, Character


cats_dict = {c.name: c for c in Category.objects.all()}


session = HTMLSession()
base_url = 'https://www.goodreads.com/book/show/{}.Harry_Potter'
urls = [base_url.format(i) for i in range(1, 1000)]


def worker(url):
    response = session.get(url)
    if response.status_code != 200:
        print('ERROR', url)
        return
    print('OK', url)

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
                characters.append(character)
            data['characters'] = characters
        elif key == 'Literary Awards':
            data['literary_awards'] = row.xpath('//div[@class="infoBoxRowItem"]')[0].text

    print(data)

    breakpoint()

    book = Book.objects.create(
        name=name,
        description=description,
        origin_image=image
    )

    for cat in cats:
        category = cats_dict[cat]
        book.cats.add(category)


worker(urls[0])

# with ThreadPoolExecutor(max_workers=10) as executor:
#     executor.map(worker, urls)
