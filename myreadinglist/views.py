from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render

from books.googlebooks import search_books
from books.models import Book, UserBook, COMPLETED

BOOK_ENTRY = ('<span class="searchResWrapper">'
              '<span class="searchRes" id="{id}">'
              '<img class="bookThumb" src="{thumb}">'
              '<span class="titleAndAuthors">{title} ({authors})</span>'
              '</span></span>\n')


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


def index(request):
    last_searches = Book.objects.order_by('-inserted').all()[:50]

    user_books = UserBook.objects.select_related('user').filter(status=COMPLETED)
    top_users = user_books.values('user__username').annotate(count=Count('book'))
    top_users = top_users.values('user__username', 'count').order_by('-count')

    return render(request, 'index.html', {'last_searches': last_searches,
                                          'top_users': top_users})
