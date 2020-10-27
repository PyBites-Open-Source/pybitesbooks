import re

import bs4
import requests
from urllib import parse

from books.models import Book, Search

BASE_URL = 'https://www.googleapis.com/books/v1/volumes'
SEARCH_URL = BASE_URL + '?q={}'
BOOK_URL = BASE_URL + '/{}'
NOT_FOUND = 'Not found'
PLAY_URL = "https://play.google.com/store/books/details?id="


def get_book_info(book_id, refresh=False):
    ''' cache book info in db '''
    books = Book.objects.filter(bookid=book_id)
    if books and not refresh:
        return books.last()

    else:
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

        pages = volinfo['pageCount']
        language = volinfo['language']
        description = volinfo.get('description', 'No description')

        if 'imageLinks' in volinfo and 'small' in volinfo['imageLinks']:
            image_size = parse.parse_qs(parse.urlparse(volinfo['imageLinks']['small']).query)['zoom'][0]
        else:
            image_size = '1'

        similar_bookids = ','.join(get_similar_books(bookid))

        book = Book(bookid=bookid,
                    title=title,
                    authors=authors,
                    publisher=publisher,
                    published=published,
                    isbn=isbn,
                    pages=pages,
                    language=language,
                    description=description,
                    imagesize=image_size,
                    similar_bookids=similar_bookids)
        book.save()

        return book


def search_books(term, request):
    ''' autocomplete = keep this one api live / no cache '''
    search = Search(term=term)

    if request.user.is_authenticated:
        search.user = request.user

    search.save()

    query = SEARCH_URL.format(term)
    return requests.get(query).json()


def get_similar_books(bookid):
    resp = requests.get(f"{PLAY_URL}{bookid}")
    soup = bs4.BeautifulSoup(resp.content, 'html.parser')
    div = soup.find(text="Similar ebooks")
    if div is None:
        return {}
    links = div.find_all_next('a')
    ids = {re.sub(r'.*id=', '', link.attrs['href'])
           for link in links
           if "/store/books/details/" in link.attrs['href']}
    return ids


if __name__ == '__main__':
    from pprint import pprint as pp
    #pp(get_book_info('PvwDFlJUYHcC'))
    term = 'python for finance'
    #pp(search_books(term))
    for item in search_books(term)['items']:
        try:
            id_ = item['id']
            title = item['volumeInfo']['title']
        except KeyError:
            continue
        print(id_, title)
