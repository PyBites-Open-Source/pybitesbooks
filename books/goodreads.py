from collections import namedtuple
import concurrent.futures
from datetime import datetime
import csv
from enum import Enum
from io import StringIO
from time import sleep

from .decorators import timeit
from .googlebooks import get_book_info, search_books
from .models import UserBook, BookConversion

GOOGLE_TO_GOODREADS_READ_STATUSES = {
    "c": "read",
    "r": "currently-reading",
    "t": "to-read",
}
ImportedBook = namedtuple('ImportedBook',
                          ('title book reading_status '
                           'date_completed book_status'))


def process_rows_concurrently(rows, request):
    """Nice but causes too many queries :(
       https://developers.google.com/analytics/devguides/config/mgmt/v3/limits-quotas
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_row = {executor.submit(_process_row, row, request): row
                         for row in rows}
        for future in concurrent.futures.as_completed(future_to_row):
            yield future.result()


class BookImportStatus(Enum):
    TO_BE_ADDED = 1
    ALREADY_ADDED = 2
    COULD_NOT_FIND = 3


def _process_row(row, request, sleep_seconds):
    title = row["Title"]
    author = row["Author"]
    reading_status = row["Exclusive Shelf"]
    date_completed = datetime.strptime(
        row["Date Read"] or row["Date Added"], '%Y/%m/%d')

    goodreads_id = row["Book Id"]
    book_status = BookImportStatus.TO_BE_ADDED
    book = None

    book_mapping, _ = BookConversion.objects.get_or_create(
        goodreads_id=goodreads_id)

    if not book_mapping.googlebooks_id:
        # only query API for new book mappings
        term = f"{title} {author}"
        sleep(sleep_seconds)
        google_book_response = search_books(
            term, request)
        try:
            bookid = google_book_response["items"][0]["id"]
            book_mapping.googlebooks_id = bookid
            book_mapping.save()
        except KeyError:
            print("cannot get google books id", google_book_response)

    if book_mapping.googlebooks_id:
        try:
            sleep(sleep_seconds)
            book = get_book_info(book_mapping.googlebooks_id)
        except KeyError:
            book = None
    else:
        book_status = BookImportStatus.COULD_NOT_FIND

    if book is not None:
        user_books = UserBook.objects.filter(user=request.user, book=book)
        if user_books.count() > 0:
            book_status = BookImportStatus.ALREADY_ADDED

    return ImportedBook(title=title,
                        book=book,
                        reading_status=reading_status,
                        date_completed=date_completed,
                        book_status=book_status)


@timeit
def convert_goodreads_to_google_books(csv_upload, request, sleep_seconds=0):
    file = csv_upload.read().decode('utf-8')
    reader = csv.DictReader(StringIO(file), delimiter=',')
    # imported_books = list(process_rows_concurrently(reader, request))
    imported_books = []
    for row in reader:
        imported_books.append(_process_row(row, request, sleep_seconds))
    return imported_books
