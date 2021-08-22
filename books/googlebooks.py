import requests
from time import sleep
from urllib import parse

from .models import Book, Search

BASE_URL = 'https://www.googleapis.com/books/v1/volumes'
SEARCH_URL = BASE_URL + '?q={}'
BOOK_URL = BASE_URL + '/{}'
NOT_FOUND = 'Not found'
DEFAULT_LANGUAGE = "en"


def get_book_info(book_id, sleep_seconds=0):
    ''' cache book info in db '''
    book = Book.objects.filter(bookid=book_id)
    if book:
        return book[0]

    else:
        if sleep_seconds > 0:
            sleep(sleep_seconds)

        query = BOOK_URL.format(book_id)
        resp = requests.get(query).json()

        volinfo = resp['volumeInfo']

        bookid = book_id
        title = volinfo['title']
        authors = ', '.join(volinfo.get('authors', NOT_FOUND))
        publisher = volinfo.get('publisher', NOT_FOUND).strip('"')
        published = volinfo.get('publishedDate', NOT_FOUND)

        identifiers = volinfo.get('industryIdentifiers')
        isbn = identifiers[-1]['identifier'] if identifiers else NOT_FOUND

        pages = volinfo.get('pageCount', 0)
        language = volinfo.get('language', DEFAULT_LANGUAGE)
        description = volinfo.get('description', 'No description')

        if 'imageLinks' in volinfo and 'small' in volinfo['imageLinks']:
            image_size = parse.parse_qs(parse.urlparse(volinfo['imageLinks']['small']).query)['zoom'][0]
        else:
            image_size = '1'

        book = Book(bookid=bookid,
                    title=title,
                    authors=authors,
                    publisher=publisher,
                    published=published,
                    isbn=isbn,
                    pages=pages,
                    language=language,
                    description=description,
                    imagesize=image_size)
        book.save()

        return book


def search_books(term, request=None, sleep_seconds=0, lang=None):
    ''' autocomplete = keep this one api live / no cache '''
    search = Search(term=term)
    if request and request.user.is_authenticated:
        search.user = request.user
    search.save()

    query = SEARCH_URL.format(term)

    if lang is not None:
        query += f"&langRestrict={lang}"

    if sleep_seconds > 0:
        sleep(sleep_seconds)
    return requests.get(query).json()


if __name__ == '__main__':
    term = 'python for finance'
    for item in search_books(term)['items']:
        try:
            id_ = item['id']
            title = item['volumeInfo']['title']
        except KeyError:
            continue
        print(id_, title)
