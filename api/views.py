from collections import defaultdict, Counter
import json
from random import randint, choice

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from books.models import UserBook


def user_books(request, username=None):

    if username is None:
        data = Counter()
        books = UserBook.objects.select_related('user').all()
        for book in books:
            data[book.user.username] += 1

    else:
        data = defaultdict(list)
        user = get_object_or_404(User, username=username)
        books = UserBook.objects.select_related('book').filter(user=user)

        for book in books:
            data[book.status].append(dict(bookid=book.book.bookid,
                                          title=book.book.title,
                                          authors=book.book.authors,
                                          completed=book.completed))

    json_data = json.dumps(data, indent=4, default=str, sort_keys=False)

    return HttpResponse(json_data, content_type='application/json')


def random_book(request, grep=None):
    """Return a random book with optional filter"""
    books = UserBook.objects.select_related('book').all()

    if grep is not None:
        books = books.filter(book__title__icontains=grep.lower())
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

    json_data = json.dumps(data, indent=4, default=str, sort_keys=False)

    return HttpResponse(json_data, content_type='application/json')
