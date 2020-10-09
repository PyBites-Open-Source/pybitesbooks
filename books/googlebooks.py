import requests
from urllib import parse

from books.models import Book, Search

BASE_URL = 'https://www.googleapis.com/books/v1/volumes'
SEARCH_URL = BASE_URL + '?q={}'
BOOK_URL = BASE_URL + '/{}'
NOT_FOUND = 'Not found'

def get_book_info(book_id):
    ''' cache book info in db '''
    book = Book.objects.filter(bookid=book_id)
    if book:
        return book[0]

    else:
        query = BOOK_URL.format(book_id)
        resp = requests.get(query).json()

        volinfo = resp['volumeInfo']

        bookid = book_id
        title = volinfo['title']
        authors = ', '.join(volinfo['authors'])
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


def search_books(term, request):
    ''' autocomplete = keep this one api live / no cache '''
    search = Search(term=term)

    if request.user.is_authenticated:
        search.user = request.user

    search.save()

    query = SEARCH_URL.format(term)
    return requests.get(query).json()


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
