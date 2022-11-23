from collections import defaultdict
import json
from random import randint, choice

from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404

from books.models import Book, UserBook


def get_users():
    user_books = defaultdict(list)
    books = UserBook.objects.select_related('user').all()
    for book in books:
        user_books[book.user.username].append(book)
    return user_books


def get_user_last_book(username):
    user = get_object_or_404(User, username=username)

    books = UserBook.objects.select_related('book')
    books = books.filter(user=user).order_by('-inserted')
    if not books:
        raise Http404

    book = books[0]
    data = dict(bookid=book.book.bookid,
                title=book.book.title,
                url=book.book.url,
                authors=book.book.authors,
                published=book.book.published,
                isbn=book.book.isbn,
                pages=book.book.pages,
                language=book.book.language,
                description=book.book.description,
                imagesize=book.book.imagesize)
    return data


def get_user_books(username):
    data = defaultdict(list)
    user = get_object_or_404(User, username=username)
    books = UserBook.objects.select_related('book').filter(user=user)

    for book in books:
        row = dict(bookid=book.book.bookid,
                   title=book.book.title,
                   url=book.book.url,
                   authors=book.book.authors,
                   favorite=book.favorite,
                   published=book.book.published,
                   isbn=book.book.isbn,
                   pages=book.book.pages,
                   language=book.book.language,
                   description=book.book.description,
                   imagesize=book.book.imagesize)
        data[book.status].append(row)
    return data


def user_books(request, username=None):

    if username is None:
        data = get_users()
    else:
        data = get_user_books(username)

    json_data = json.dumps(data, indent=4, default=str, sort_keys=False)

    return HttpResponse(json_data, content_type='application/json')


def get_random_book(grep=None):
    books = UserBook.objects.select_related('book').all()

    if grep is not None:
        books = books.filter(book__title__icontains=grep.lower())
        if not books:
            raise Http404
        book = choice(books)
    else:
        count = books.count()
        book = books[randint(0, count - 1)]

    data = dict(bookid=book.book.bookid,
                title=book.book.title,
                url=book.book.url,
                authors=book.book.authors,
                published=book.book.published,
                isbn=book.book.isbn,
                pages=book.book.pages,
                language=book.book.language,
                description=book.book.description,
                imagesize=book.book.imagesize)

    return data


def random_book(request, grep=None):
    """Return a random book with optional filter"""
    data = get_random_book(grep)

    json_data = json.dumps(data, indent=4, default=str, sort_keys=False)

    return HttpResponse(json_data, content_type='application/json')


def get_bookid(request, bookid):
    books = Book.objects.filter(bookid=bookid)
    if not books:
        raise Http404

    book = books[0]
    data = dict(bookid=book.bookid,
                title=book.title,
                url=book.url,
                authors=book.authors,
                publisher=book.publisher,
                published=book.published,
                isbn=book.isbn,
                pages=book.pages,
                language=book.language,
                description=book.description,
                imagesize=book.imagesize)

    json_data = json.dumps(data, indent=4, default=str, sort_keys=False)

    return HttpResponse(json_data, content_type='application/json')


def get_book_list(request, name):
    books = UserBook.objects.select_related(
        "book"
    ).filter(
        booklists__name=name
    ).order_by("book__title")

    if not books:
        raise Http404

    data = []
    for book in books:
        book_obj = dict(
            bookid=book.book.bookid,
            title=book.book.title,
            url=book.book.url,
            authors=book.book.authors,
            pages=book.book.pages,
            description=book.book.description)
        data.append(book_obj)

    return HttpResponse(
        json.dumps(
            data, indent=4, default=str, sort_keys=False),
        content_type='application/json'
    )


def get_book_stats(request, username):
    user_books = UserBook.objects.select_related(
        'book', 'user'
    # ).prefetch_related(
    #    'book__categories'
    ).filter(user__username=username)

    data = defaultdict(list)
    for user_book in user_books:
        row = dict(bookid=user_book.book.bookid,
                   title=user_book.book.title,
                   url=user_book.book.url,
                   # categories=[c.name for c in
                   #             user_book.book.categories.all()],
                   status=user_book.status,
                   favorite=user_book.favorite,
                   completed=user_book.completed)
        data[user_book.user.username].append(row)

    json_data = json.dumps(data, indent=4, default=str, sort_keys=False)
    return HttpResponse(json_data, content_type='application/json')
