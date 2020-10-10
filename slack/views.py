import json
import os

from decouple import config
from django.contrib.humanize.templatetags.humanize import naturalday
from django.http import Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from api.views import (get_users,
                       get_user_last_book,
                       get_random_book)

HOME = 'https://pbreadinglist.herokuapp.com'
BOOK_THUMB = "https://books.google.com/books?id={bookid}&printsec=frontcover&img=1&zoom={imagesize}&source=gbs_gdata"  # noqa
SLACK_TOKEN = config('SLACK_VERIFICATION_TOKEN')
HELP_TEXT = ('```'
             '/book help          -> print this help message\n'
             '/book               -> get a random book added to PyBites Reading List\n'  # noqa E501
             '/book grep          -> get a random book filtered on "grep" (if added)\n'  # noqa E501
             '/book user          -> get usernames and their most recent book read\n'
             '/book user username -> get the last book "username" added\n'
             '```')
COMMANDS = dict(rand=get_random_book,
                grep=get_random_book,
                user=get_users,
                username=get_user_last_book)


def _validate_token(request):
    token = request.get('token')
    if token is None or token != SLACK_TOKEN:
        raise Http404


def _create_user_output(user_books):
    users = []
    for user, books in user_books.items():
        last_book = (books and sorted(books,
                                      key=lambda x: x.completed)[-1]
                     or 'no books read yet')
        users.append((user, last_book))

    col1, col2 = 'User', f'Last read -> {HOME}'
    msg = [f'{col1:<19}: {col2}']
    msg.append('-' * 74)  # slack pre line length it seems

    for user, last_book in sorted(users,
                                  key=lambda x: x[1].completed,
                                  reverse=True):
        title = last_book.book.title
        title = len(title) > 32 and title[:32] + ' ...' or f'{title:<36}'
        msg.append(f'{user:<19}: {title} ({naturalday(last_book.completed)})')
    return '```' + '\n'.join(msg) + '```'

def _get_attachment(msg, book=None):
    if book is None:
        return {"text": msg,
                "color": "#3AA3E3"}
    else:
        return {"title": book['title'],
                "title_link": book['url'],
                "image_url": BOOK_THUMB.format(bookid=book['bookid'], imagesize=book['imagesize']),
                "text": msg,
                "color": "#3AA3E3"}

@csrf_exempt
def get_book(request):
    request = request.POST
    _validate_token(request)

    headline, msg = None, None

    text = request.get('text')
    text = text.split()
    single_word_cmd = text and len(text) == 1 and text[0]
    book = None
    if single_word_cmd == 'help':
        headline = 'Command syntax:'
        msg = HELP_TEXT

    elif single_word_cmd == 'user':
        headline = 'PyBites Readers:'
        user_books = COMMANDS['user']()
        msg = _create_user_output(user_books)

    else:
        # 0 or multiple words
        if len(text) == 0:
            book = COMMANDS['rand']()
            headline = f'Here is a random title for your reading list:'

        elif len(text) == 2 and text[0] == 'user':
            username = text[-1]
            book = COMMANDS['username'](username)
            headline = f'Last book _{username}_ added:'

        else:
            grep = ' '.join(text)
            book = COMMANDS['grep'](grep)
            headline = f'Here is a "{grep}" title for your reading list:'

        msg = f"Author: _{book['authors']}_ (pages: {book['pages']})"

    data = {"response_type": "in_channel",
            "text": headline,
            "attachments": [_get_attachment(msg, book)]}

    return HttpResponse(json.dumps(data),
                        content_type='application/json')
