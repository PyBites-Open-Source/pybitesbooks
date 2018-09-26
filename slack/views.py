import json
import os
import re

from django.http import Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from api.views import (get_usernames, get_user_last_book,
                       get_random_book)

PB_READING_LIST = "http://pbreadinglist.herokuapp.com/books/"
SLACK_TOKEN = os.environ['SLACK_VERIFICATION_TOKEN']
HELP_TEXT = ('```'
             '/book help          -> print this help message\n'
             '/book               -> get a random book from PyBites Reading List\n'
             '/book grep          -> get a random book filtered on "grep" (if added)\n'
             '/book user          -> see our top 5 readers (dear all, read more!)\n'
             '/book user username -> get the last book "username" completed\n'
             '```')
COMMANDS = dict(rand=get_random_book,
                grep=get_random_book,
                user=get_usernames,
                username=get_user_last_book)


def _validate_token(request):
    token = request.get('token')
    if token is None or token != SLACK_TOKEN:
        raise Http404


def _create_book_msg(book):
    description = re.sub(r'<[^<]+?>', r'', book['description'])
    return (f"*{book['title']}*\nAuthor: _{book['authors']}_ "
            f"(pages: {book['pages']})\n"
            f"Description:\n```{description}```")


@csrf_exempt
def get_book(request):
    request = request.POST
    _validate_token(request)

    headline, msg = None, None

    text = request.get('text')
    text = text.split()
    single_word_cmd = text and len(text) == 1 and text[0]
    if single_word_cmd == 'help':
        headline = 'Command syntax:'
        msg = HELP_TEXT

    elif single_word_cmd == 'user':
        headline = 'PyBites Readers:'
        msg = ', '.join(COMMANDS['user']())

    else:
        # 0 or multiple words
        if len(text) == 0:
            book = COMMANDS['rand']()
            headline = f'Here is a random title for your reading list:'

        elif len(text) == 2 and text[0] == 'user':
            username = text[-1]
            book = COMMANDS['username'](username)
            headline = f'Last book {username.title()} read:'

        else:
            grep = ' '.join(text)
            book = COMMANDS['grep'](grep)
            headline = f'Here is a "{grep}" title for your reading list:'

        headline += f"\n{PB_READING_LIST}{book['bookid']}"
        msg = _create_book_msg(book)

    data = {
        "response_type": "in_channel",
        "text": headline,
        "color": "#3AA3E3",
        "image_url": "https://datadoghq.com/snapshot/path/to/snapshot.png",
        "attachments": [
            {
                "text": msg,
            }
        ]
    }

    return HttpResponse(json.dumps(data),
                        content_type='application/json')
