from time import sleep

from django.core.management.base import BaseCommand

from books.googlebooks import get_book_info_from_api
from books.models import Book, Category


class Command(BaseCommand):
    help = 'Add categories to existing books'

    def handle(self, *args, **options):
        books = Book.objects.all()
        for book in books:
            resp = get_book_info_from_api(book.bookid)
            breakpoint()
