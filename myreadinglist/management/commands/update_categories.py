from time import sleep

from django.core.management.base import BaseCommand

from books.googlebooks import get_book_info_from_api
from books.models import Book, Category


class Command(BaseCommand):
    help = 'Add categories to existing books'

    def handle(self, *args, **options):
        books = Book.objects.all()
        for book in books:
            print(book.bookid, book.title)
            if book.categories.count() > 0:
                print("book already has categories, skipping")
                continue
            try:
                get_book_info_from_api(book.bookid)
            except KeyError:
                print("cannot get book, skipping")
            sleep(0.5)  # not sure about rates
