from collections import defaultdict
import json
from random import randint, choice

from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404

from books.models import UserBook


def get_users():
    user_books = defaultdict(list)
    books = UserBook.objects.select_related('user').all()
    for book in books:
        user_books[book.user.username].append(book.completed)
    return user_books


def get_user_last_book(username):
    user = get_object_or_404(User, username=username)

    books = UserBook.objects.select_related('book')
    books = books.filter(user=user, status='c')
    books = books.order_by('-completed', '-updated')

    book = books[0]
    data = dict(bookid=book.book.bookid,
                title=book.book.title,
                authors=book.book.authors,
                published=book.book.published,
                isbn=book.book.isbn,
                pages=book.book.pages,
                language=book.book.language,
                description=book.book.description)
    return data


def get_user_books(username):
    data = defaultdict(list)
    user = get_object_or_404(User, username=username)
    books = UserBook.objects.select_related('book').filter(user=user)

    for book in books:
        data = dict(bookid=book.book.bookid,
                    title=book.book.title,
                    authors=book.book.authors,
                    published=book.book.published,
                    isbn=book.book.isbn,
                    pages=book.book.pages,
                    language=book.book.language,
                    description=book.book.description)
        data[book.status].append(data)
    return data


def user_books(request, username=None):

    if username is None:
        data = get_users()
    else:
        data = get_user_books()

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
                authors=book.book.authors,
                published=book.book.published,
                isbn=book.book.isbn,
                pages=book.book.pages,
                language=book.book.language,
                description=book.book.description)

    return data


def random_book(request, grep=None):
    """Return a random book with optional filter"""
    data = get_random_book(grep)

    json_data = json.dumps(data, indent=4, default=str, sort_keys=False)

    return HttpResponse(json_data, content_type='application/json')
