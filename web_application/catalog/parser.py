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


from catalog.models import *


def worker(gr_id):

    with HTMLSession() as session:

        url = f'https://www.goodreads.com/book/show/{gr_id}.aaaaaa'

        response = session.get(url)

        if response.status_code != 200:
            print('ERROR', url)
            return

        book = {'goodreads_id': gr_id}

        try:

            book['name'] = response.html.xpath('//h1')[0].text

            try:
                book['description'] = response.html.xpath('//div[@id="description"]/span[2]')[0].text
            except IndexError:
                book['description'] = ''

            try:
                book['origin_image'] = response.html.xpath('//img[@id="coverImage"]/@src')[0]
            except IndexError:
                book['origin_image'] = ''

            cats = response.html.xpath('//a[@class="actionLinkLite bookPageGenreLink"]/text()')

            chars = []
            rows = response.html.xpath('//div[@class="clearFloats"]')
            for row in rows:
                key = row.xpath('//div[@class="infoBoxRowTitle"]')[0].text
                if key == 'Original Title':
                    book['original_title'] = row.xpath('//div[@class="infoBoxRowItem"]')[0].text
                elif key == 'ISBN':
                    book['isbn'] = row.xpath('//div[@class="infoBoxRowItem"]')[0].text
                elif key == 'Edition Language':
                    book['edition_language'] = row.xpath('//div[@class="infoBoxRowItem"]')[0].text
                elif key == 'Characters':
                    for link in row.xpath('//div[@class="infoBoxRowItem"]/a'):
                        character = {
                            'name': link.text,
                            'source': link.absolute_links.pop(),
                            'slug': slugify(link.text)
                        }
                        chars.append(character)
                elif key == 'Literary Awards':
                    book['literary_awards'] = row.xpath(
                        '//div[@class="infoBoxRowItem"]')[0].text
        except Exception as e:
            print(e, type(e), sys.exc_info()[-1].tb_lineno, url)
            return

        author = {}

        try:
            author['name'] = response.html.xpath(
                '//div[@class="bookAuthorProfile__name"]/a')[0].text
        except Exception as e:
            print(e, type(e), sys.exc_info()[-1].tb_lineno, url)

        try:
            author['link'] = response.html.xpath(
                '//div[@class="bookAuthorProfile__name"]/a/@href')[0]
            author['link'] = 'https://www.goodreads.com' + author['link']
        except Exception as e:
            print(e, type(e), sys.exc_info()[-1].tb_lineno, url)

        try:
            author['photo_origin'] = response.html.xpath(
                '//div[@class="bookAuthorProfile__photo"]/@style')[0][22:-2]

            img_resp = session.get(author['photo_origin'])
            image_name = author['photo_origin'].split('/')[-1]
            with open(f'media/authors/{image_name}', 'wb') as imgf:
                imgf.write(img_resp.content)

            author['photo'] = f'authors/{image_name}'

        except Exception as e:
            print(e, type(e), sys.exc_info()[-1].tb_lineno, url)

        try:
            author['biography'] = response.html.xpath(
                '//div[@class="bookAuthorProfile__about"]/'
                'span[contains(@id, "freeText")][2]'
            )[0].text
        except Exception as e:
            print(e, type(e), sys.exc_info()[-1].tb_lineno, url)

        try:
            author, created = Author.objects.get_or_create(**author)

            book, created = Book.objects.get_or_create(**book)
            book.owner = author
            book.save()

            for cat in cats:
                category, created = Category.objects.get_or_create(name=cat)
                book.cats.add(category)

            for char in chars:
                char, created = Character.objects.get_or_create(**char)
                book.char.add(char)

        except Exception as e:
            print(e, type(e), sys.exc_info()[-1].tb_lineno)

        try:
            img_resp = session.get(book.origin_image)
            image_name = book.origin_image.split('/')[-1]
            with open(f'media/photos/{image_name}', 'wb') as imgf:
                imgf.write(img_resp.content)

            Photo.objects.create(
                photo=f'photos/{image_name}',
                name=image_name,
                original=book.origin_image,
                book=book
            )
        except Exception as e:
            print(e, type(e), sys.exc_info()[-1].tb_lineno)

        print('OK', url)


def run(start, end, threads=10):
    # Book.objects.all().delete()
    # Author.objects.all().delete()
    # Category.objects.all().delete()
    # Photo.objects.all().delete()
    with ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(worker, range(start, end))


if __name__ == '__main__':
    run(0, 10000)
