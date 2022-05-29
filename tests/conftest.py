from itertools import cycle

from django.contrib.auth.models import User
import pytest

from books.models import Book, Category, UserBook


@pytest.fixture(scope="module", autouse=True)
def categories(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        categories = [
            "Computers / Programming / General",
            "Computers / Information Technology",
            "Self-Help / General",
            "Self-Help / Personal Growth / General",
            "Business & Economics / Personal Success",
            "Self-Help / Affirmations",
            "Body, Mind & Spirit / Inspiration & Personal Growth",
            "Body, Mind & Spirit / New Thought",
            "Health & Fitness / Alternative Therapies"
            "Self-Help / Personal Growth / Success",
            "Fiction / Science Fiction / Space Opera"
            "Fiction / Science Fiction / Action & Adventure",
            "Fiction / Science Fiction / Military",
        ]

        with django_db_blocker.unblock():
            for category in categories:
                Category.objects.create(name=category)

        categories = Category.objects.all()
        return categories


@pytest.fixture(scope="module")
def books(django_db_setup, django_db_blocker, categories):
    with django_db_blocker.unblock():
        book = Book(
            bookid="nneBa6-mWfgC",
            title="Coders at Work",
            authors="Peter Seibel",
            publisher="Apress",
            published="2009-09-16",
            isbn="978143021948463",
            pages=632,
            language="en",
            description="Peter Seibel interviews 15 of the most ..."
        )
        book.save()
        book.categories.add(*categories[:2])
        book.save()

        book = Book(
            bookid="__CvAFrcWY0C",
            title="Unlimited Power",
            authors="Tony Robbins",
            publisher="Simon and Schuster",
            published="2008-06-30",
            isbn="978141658637144",
            pages=448,
            language="en",
            description="Anthony Robbins calls it the ..."
        )
        book.save()
        book.categories.add(*categories[2:6])
        book.save()

        book = Book(
            bookid="3V_6DwAAQBAJ",
            title="Power Vs. Force",
            authors="David R. Hawkins",
            publisher="Hay House, Inc",
            published="2014",
            isbn="978140194507741",
            pages=412,
            language="en",
            description="Imagine—what if you had access to a simple ..."
        )
        book.save()
        book.categories.add(*categories[6:9])
        book.save()

        book = Book(
            bookid="bK1ktwAACAAJ",
            title="177 Mental Toughness Secrets of the World Class",
            authors="Steve Siebold",
            publisher="London House Press",
            published="2010",
            isbn="9780975500354",
            pages=281,
            language="en",
            description="NEW EDITION: Is it possible for a person of ..."
        )
        book.save()
        book.categories.add(categories[9])
        book.save()

        books = Book.objects.all()
        return books


@pytest.fixture(scope="module")
def two_books(django_db_setup, django_db_blocker, categories):
    with django_db_blocker.unblock():
        book = Book(
            bookid="jaM7DwAAQBAJ",
            title="Ender's Game",
            authors="Orson Scott Card",
            publisher="Tom Doherty Associates",
            published="2017-10-17",
            isbn="9780765394866",
            pages=448,
            language="en",
            description="This engaging, collectible, ..."
        )
        book.save()
        book.categories.add(*categories[10:])
        book.save()

        book = Book(
            bookid="UCJMRAAACAAJ",
            title="Elantris",
            authors="Brandon Sanderson",
            publisher="Gollancz",
            published="2011",
            isbn="9780575097445",
            pages=656,
            language="en",
            description="Elantris was built on magic and it thrived ..."
        )
        book.save()
        # this one did not yield categories from Google Books API

        added_titles = ["Ender's Game", "Elantris"]
        books = Book.objects.filter(title__in=added_titles)
        return books


@pytest.fixture(scope="module")
def user(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        username, password = "user1", 'bar'
        return User.objects.create_user(
            username=username, password=password)


@pytest.fixture
def login(django_db_setup, django_db_blocker, client, user):
    client.force_login(user)
    return client


@pytest.fixture(scope="module")
def user_books(django_db_setup, django_db_blocker, books, user):
    with django_db_blocker.unblock():
        statuses = cycle('r c'.split())
        user_books = [
            UserBook(user=user, book=book, status=next(statuses))
            for book in books
        ]
        UserBook.objects.bulk_create(user_books)
        return UserBook.objects.all()


@pytest.fixture(scope="module")
def user_fav_books(django_db_setup, django_db_blocker, two_books, user):
    with django_db_blocker.unblock():
        statuses = cycle('r c'.split())
        user_books = [
            UserBook(user=user, book=book, status=next(statuses),
                     favorite=True)
            for book in two_books
        ]
        UserBook.objects.bulk_create(user_books)
        return UserBook.objects.filter(favorite=True)
