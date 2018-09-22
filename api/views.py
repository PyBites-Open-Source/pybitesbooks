from collections import defaultdict
import json

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from books.models import UserBook


def user_books(request, username):
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
