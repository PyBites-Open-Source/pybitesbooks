from collections import Counter

from django.core.management.base import BaseCommand

from books.models import Book, Category


class Command(BaseCommand):
    help = 'remove duplicate cached books (needed for migration 0035)'

    def handle(self, *args, **options):
        books = Book.objects.all()
        cnt = Counter(book.bookid for book in books)
        for bookid, count in cnt.most_common():
            if count < 2:
                continue
            books = Book.objects.filter(bookid=bookid)
            for book in books[1:]:
                self.stdout.write(book.delete())
