from datetime import datetime
import csv
from enum import Enum
from io import StringIO

from django.contrib.auth.models import User
import pytz

from .googlebooks import get_book_info, search_books
from .models import UserBook, BookConversion, ImportedBook

GOOGLE_TO_GOODREADS_READ_STATUSES = {
    "c": "read",
    "r": "currently-reading",
    "t": "to-read",
}


class BookImportStatus(Enum):
    TO_BE_ADDED = 1
    ALREADY_ADDED = 2
    COULD_NOT_FIND = 3


def _cache_book_for_row(row, username, sleep_seconds):
    user = User.objects.get(username=username)
    title = row["Title"]

    # if import title is cached return it (this is done in
    # the view but this instance is useful if user uploads
    # a new csv file with only a few new titles)
    try:
        imported_book = ImportedBook.objects.get(
            title=title,
            user=user)
        return imported_book
    except ImportedBook.DoesNotExist:
        pass

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
        google_book_response = search_books(
            term, sleep_seconds=sleep_seconds)
        try:
            bookid = google_book_response["items"][0]["id"]
            book_mapping.googlebooks_id = bookid
            book_mapping.save()
        except KeyError:
            print("cannot get G book:", google_book_response)

    if book_mapping.googlebooks_id:
        try:
            book = get_book_info(book_mapping.googlebooks_id,
                                 sleep_seconds=sleep_seconds)
        except KeyError:
            book = None
    else:
        book_status = BookImportStatus.COULD_NOT_FIND

    if book is not None:
        user_books = UserBook.objects.filter(
            user=user, book=book)
        if user_books.count() > 0:
            book_status = BookImportStatus.ALREADY_ADDED

    imported_book = ImportedBook.objects.create(
        title=title,
        book=book,
        reading_status=reading_status,
        date_completed=pytz.utc.localize(date_completed),
        book_status=book_status.name,
        user=user)

    return imported_book


def convert_goodreads_to_google_books(
    file_content, username, sleep_seconds=0
):
    # remove read().decode('utf-8') as it's not serializable
    reader = csv.DictReader(
        StringIO(file_content), delimiter=',')

    imported_books = []
    for row in reader:
        book = _cache_book_for_row(row, username, sleep_seconds)
        imported_books.append(book)

    return imported_books
