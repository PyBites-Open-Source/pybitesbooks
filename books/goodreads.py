from collections import namedtuple
from datetime import datetime
import csv
from enum import Enum
from io import StringIO

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


class BookImportStatus(Enum):
    TO_BE_ADDED = 1
    ALREADY_ADDED = 2
    COULD_NOT_FIND = 3


def convert_goodreads_to_google_books(csv_upload, request):
    file = csv_upload.read().decode('utf-8')
    reader = csv.DictReader(StringIO(file), delimiter=',')
    imported_books = []

    for row in reader:
        title = row["Title"]
        author = row["Author"]
        reading_status = row["Exclusive Shelf"]
        date_completed = datetime.strptime(
            row["Date Read"] or row["Date Added"], '%Y/%m/%d')

        book = None
        book_status = BookImportStatus.TO_BE_ADDED

        goodreads_id = row["Book Id"]
        googlebooks_id = None

        book_mapping, created = BookConversion.objects.get_or_create(
            goodreads_id=goodreads_id)

        if created:
            # only query API for new book mappings
            google_book_response = search_books(
                f"{title} {author}", request)
            try:
                googlebooks_id = google_book_response["items"][0]["id"]
                book_mapping.googlebooks_id = googlebooks_id
                book_mapping.save()
            except KeyError:
                continue
        else:
            googlebooks_id = book_mapping.googlebooks_id

        if book_mapping.googlebooks_id is None:
            book_status = BookImportStatus.COULD_NOT_FIND

        if googlebooks_id is not None:
            book = get_book_info(googlebooks_id)

        if book is not None:
            try:
                UserBook.objects.get(user=request.user, book=book)
                book_status = BookImportStatus.ALREADY_ADDED
            except UserBook.DoesNotExist:
                pass

        imported_books.append(
            ImportedBook(
                title=title,
                book=book,
                reading_status=reading_status,
                date_completed=date_completed,
                book_status=book_status)
        )

    return imported_books
