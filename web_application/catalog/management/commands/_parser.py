import sys
from requests_html import HTMLSession
from concurrent.futures import ThreadPoolExecutor
from catalog.models import *


def worker(gr_id):

    with HTMLSession() as session:

        url = f'https://www.goodreads.com/book/show/{gr_id}.aaaaaa'

        response = session.get(url)

        if response.status_code != 200:
            print('ERROR', url)
            return

        book_dict = {'goodreads_id': gr_id}

        try:

            book_dict['name'] = response.html.xpath('//h1')[0].text

            try:
                book_dict['description'] = response.html.xpath('//div[@id="description"]/span[2]')[0].text
            except IndexError:
                book_dict['description'] = ''

            try:
                book_dict['origin_image'] = response.html.xpath('//img[@id="coverImage"]/@src')[0]
            except IndexError:
                book_dict['origin_image'] = ''

            cats = response.html.xpath('//a[@class="actionLinkLite bookPageGenreLink"]/text()')

            chars = []
            rows = response.html.xpath('//div[@class="clearFloats"]')
            for row in rows:
                key = row.xpath('//div[@class="infoBoxRowTitle"]')[0].text
                if key == 'Original Title':
                    book_dict['original_title'] = row.xpath('//div[@class="infoBoxRowItem"]')[0].text
                elif key == 'ISBN':
                    book_dict['isbn'] = row.xpath('//div[@class="infoBoxRowItem"]')[0].text
                elif key == 'Edition Language':
                    book_dict['edition_language'] = row.xpath('//div[@class="infoBoxRowItem"]')[0].text
                elif key == 'Characters':
                    for link in row.xpath('//div[@class="infoBoxRowItem"]/a'):
                        character = {
                            'name': link.text,
                            'source': link.absolute_links.pop(),
                            'slug': slugify(link.text)
                        }
                        chars.append(character)
                elif key == 'Literary Awards':
                    book_dict['literary_awards'] = row.xpath(
                        '//div[@class="infoBoxRowItem"]')[0].text
                del key
        except Exception as e:
            print(e, type(e), sys.exc_info()[-1].tb_lineno, url)
            return

        author_dict = {}

        try:
            author_dict['name'] = response.html.xpath(
                '//div[@class="bookAuthorProfile__name"]/a')[0].text
        except Exception as e:
            print(e, type(e), sys.exc_info()[-1].tb_lineno, url)

        try:
            author_dict['link'] = response.html.xpath(
                '//div[@class="bookAuthorProfile__name"]/a/@href')[0]
            author_dict['link'] = 'https://www.goodreads.com' + author_dict['link']
        except Exception as e:
            print(e, type(e), sys.exc_info()[-1].tb_lineno, url)

        try:
            author_dict['photo_origin'] = response.html.xpath(
                '//div[@class="bookAuthorProfile__photo"]/@style')[0][22:-2]

            img_resp = session.get(author_dict['photo_origin'])
            image_name = author_dict['photo_origin'].split('/')[-1]
            with open(f'media/authors/{image_name}', 'wb') as imgf:
                imgf.write(img_resp.content)

            del img_resp

            author_dict['photo'] = f'authors/{image_name}'

            del image_name

        except Exception as e:
            print(e, type(e), sys.exc_info()[-1].tb_lineno, url)

        try:
            author_dict['biography'] = response.html.xpath(
                '//div[@class="bookAuthorProfile__about"]/'
                'span[contains(@id, "freeText")][2]'
            )[0].text
        except Exception as e:
            print(e, type(e), sys.exc_info()[-1].tb_lineno, url)

        try:
            author, created = Author.objects.get_or_create(**author_dict)

            del author_dict

            book, created = Book.objects.get_or_create(**book_dict)
            book.owner = author
            book.save()

            for cat in cats:
                category, created = Category.objects.get_or_create(name=cat)
                book.cats.add(category)

            del cats

            for char in chars:
                char, created = Character.objects.get_or_create(**char)
                book.char.add(char)

            del chars

        except Exception as e:
            print(e, type(e), sys.exc_info()[-1].tb_lineno)

        try:
            img_resp = session.get(book.origin_image)
            image_name = book.origin_image.split('/')[-1]
            with open(f'media/photos/{image_name}', 'wb') as imgf:
                imgf.write(img_resp.content)

            del img_resp

            Photo.objects.create(
                photo=f'photos/{image_name}',
                name=image_name,
                original=book.origin_image,
                book=book
            )
        except Exception as e:
            print(e, type(e), sys.exc_info()[-1].tb_lineno)

        del book

        print('OK', url)


def run(start, end, threads=10):
    with ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(worker, range(start, end))
