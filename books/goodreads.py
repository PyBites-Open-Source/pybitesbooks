from collections import namedtuple
import concurrent.futures
from datetime import datetime
import csv
from enum import Enum
from io import StringIO

from .decorators import timeit
from .googlebooks import get_book_info, search_books
from .models import UserBook, BookConversion

GOOGLE_TO_GOODREADS_READ_STATUSES = {
    "r": "read",
    "c": "currently-reading",
    "t": "to-read",
}
ImportedBook = namedtuple('ImportedBook',
                          ('title book reading_status '
                           'date_completed book_status'))


def process_rows_concurrently(rows, request):
    with concurrent.futures.ThreadPoolExecutor(max_workers=32) as executor:
        future_to_row = {executor.submit(_process_row, row, request): row
                         for row in rows}
        for future in concurrent.futures.as_completed(future_to_row):
            yield future.result()


class BookImportStatus(Enum):
    TO_BE_ADDED = 1
    ALREADY_ADDED = 2
    COULD_NOT_FIND = 3


def _process_row(row, request):
    title = row["Title"]
    author = row["Author"]
    reading_status = row["Exclusive Shelf"]
    date_completed = datetime.strptime(
        row["Date Read"] or row["Date Added"], '%Y/%m/%d')

    goodreads_id = row["Book Id"]
    book_status = BookImportStatus.TO_BE_ADDED
    book = None

    book_mapping, created = BookConversion.objects.get_or_create(
        goodreads_id=goodreads_id)

    if created:
        # only query API for new book mappings
        google_book_response = search_books(
            f"{title} {author}", request)
        try:
            bookid = google_book_response["items"][0]["id"]
            book_mapping.googlebooks_id = bookid
            book_mapping.save()
        except KeyError:
            pass

    if book_mapping.googlebooks_id:
        try:
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
def convert_goodreads_to_google_books(csv_upload, request):
    file = csv_upload.read().decode('utf-8')
    reader = csv.DictReader(StringIO(file), delimiter=',')
    imported_books = list(process_rows_concurrently(reader, request))
    return imported_books
