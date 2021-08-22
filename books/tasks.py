from celery import shared_task
from django.conf import settings
from django.contrib.auth.models import User

from books.goodreads import convert_goodreads_to_google_books
from myreadinglist.mail import send_email

SUBJECT = "Your goodreads import has been processed"
MESSAGE_TEMPLATE = """
Hey {username},

Your import of goodreads book is done, we converted {num_converted} books.

Please check out the preview selecting the books you want to import:

{url}

Cheers,
The PyBites Books Team
"""  # noqa E501
PREVIEW_PAGE = settings.DOMAIN + "/books/import_books/preview"


@shared_task
def retrieve_google_books(file_content, username):
    """Convert goodreads to google books, sleeping
       one second in between requests to not hit Google
       API rate limits. Sent user email when done
       """
    books = convert_goodreads_to_google_books(
        file_content, username, sleep_seconds=1)

    num_converted = len(books)
    msg = MESSAGE_TEMPLATE.format(
        username=username,
        num_converted=num_converted,
        url=PREVIEW_PAGE
    )
    email = User.objects.get(username=username).email
    send_email(email, SUBJECT, msg)

    return f"{num_converted} books converted!"
