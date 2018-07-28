from django.http import HttpResponse
from django.shortcuts import render

from myreadinglist.googlebooks import search_books, get_book_info

BOOK_ENTRY = ('<span class="searchResWrapper">'
              '<span class="searchRes" id="{id}">'
              '<img class="miniAvatar" src="{thumb}">'
              '{title} ({authors})</span>'
              '</span>\n')


def _parse_response(items):
    for item in items:
        try:
            id_ = item['id']
            volinfo = item['volumeInfo']
            title = volinfo['title']
            authors = volinfo['authors'][0]
            thumb = volinfo['imageLinks']['smallThumbnail']
        except KeyError:
            continue
        book_entry = BOOK_ENTRY.format(id=id_,
                                       title=title,
                                       authors=authors,
                                       thumb=thumb)
        yield book_entry


def get_books(request):
    no_result = HttpResponse('fail')

    try:
        term = request.GET.get('q')
    except:
        return no_result

    term = request.GET.get('q', '')
    books = search_books(term, request)
    items = books.get('items')
    if not items:
        return no_result

    data = list(_parse_response(items))

    return HttpResponse(data)


def book_page(request, bookid):
    book = get_book_info(bookid)
    return render(request, 'book.html', {'book': book})


def home(request):
    return render(request, 'home.html')
