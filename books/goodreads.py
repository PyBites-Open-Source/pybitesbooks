from collections import namedtuple, defaultdict
from datetime import datetime
import csv
from enum import Enum
from io import StringIO

from .googlebooks import get_book_info, search_books
from .models import UserBook

GOODREADS_STATUSES = {
    "read": "c",
    "currently-reading": "r",
    "to-read": "t",
}
ImportedBook = namedtuple('ImportedBook', 'title book status')


class BookImportStatus(Enum):
    ADDED = 1
    USER_ALREADY_ADDED = 2
    NOT_FOUND = 3


def convert_goodreads_to_google_books(csv_upload, request):
    file = csv_upload.read().decode('utf-8')
    reader = csv.DictReader(StringIO(file), delimiter=',')
    books = []

    for row in reader:
        title = row["Title"]
        author = row["Author"]
        status = GOODREADS_STATUSES.get(row["Exclusive Shelf"], "c")
        completed = datetime.strptime(
            row["Date Read"] or row["Date Added"], '%Y/%m/%d')

        google_book_response = search_books(f"{title} {author}", request)

        book, status = None, BookImportStatus.ADDED
        try:
            book_id = google_book_response["items"][0]["id"]
            book = get_book_info(book_id)
        except KeyError:
            status = BookImportStatus.NOT_FOUND
            continue

        if book is not None:
            try:
                UserBook.objects.get(
                    user=request.user, book=book)
            except UserBook.DoesNotExist:
                status = BookImportStatus.NOT_FOUND
                pass

        books.append(
            ImportedBook(
                title=title,
                book=book,
                status=status)
        )
    return books
