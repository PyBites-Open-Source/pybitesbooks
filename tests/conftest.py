from itertools import cycle

from django.contrib.auth.models import User
import pytest

from books.models import Book, UserBook


@pytest.fixture(scope="module")
def books(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        books = [
            Book(pk=1,  # required for sqlite test DB
                 bookid="nneBa6-mWfgC",
                 title="Coders at Work",
                 authors="Peter Seibel",
                 publisher="Apress",
                 published="2009-09-16",
                 isbn="978143021948463",
                 pages=632,
                 language="en",
                 description=("<p>Peter Seibel interviews 15 of the most "
                              "interesting computer programmers alive ...")),
            Book(pk=2,
                 bookid="__CvAFrcWY0C",
                 title="Unlimited Power",
                 authors="Tony Robbins",
                 publisher="Simon and Schuster",
                 published="2008-06-30",
                 isbn="978141658637144",
                 pages=448,
                 language="en",
                 description=("<p>Anthony Robbins calls it the "
                              "new science of personal achievement ...")),
            Book(pk=3,
                 bookid="3V_6DwAAQBAJ",
                 title="Power Vs. Force",
                 authors="David R. Hawkins",
                 publisher="Hay House, Inc",
                 published="2014",
                 isbn="978140194507741",
                 pages=412,
                 language="en",
                 description=("Imagine—what if you had access to a simple "
                              "yes-or-no answer to any question you wished "
                              "to ask? ...")),
            Book(pk=4,
                 bookid="bK1ktwAACAAJ",
                 title="177 Mental Toughness Secrets of the World Class",
                 authors="Steve Siebold",
                 publisher="London House Press",
                 published="2010",
                 isbn="9780975500354",
                 pages=281,
                 language="en",
                 description=("NEW EDITION: Is it possible for a person of "
                              "average intelligence and modest means to "
                              "ascend to the throne of the world class? "
                              "The answer is YES!"))
        ]
        return Book.objects.bulk_create(books)


@pytest.fixture(scope="module")
def two_books(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        books = [
            Book(pk=5,
                 bookid="jaM7DwAAQBAJ",
                 title="Ender's Game",
                 authors="Orson Scott Card",
                 publisher="Tom Doherty Associates",
                 published="2017-10-17",
                 isbn="9780765394866",
                 pages=448,
                 language="en",
                 description=("This engaging, collectible, miniature hardcover"
                              " of the Orson Scott Card classic ...")),
            Book(pk=6,
                 bookid="UCJMRAAACAAJ",
                 title="Elantris",
                 authors="Brandon Sanderson",
                 publisher="Gollancz",
                 published="2011",
                 isbn="9780575097445",
                 pages=656,
                 language="en",
                 description=("Elantris was built on magic and it thrived. "
                              "But then the magic began to fade ..."))
        ]
        return Book.objects.bulk_create(books)


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
        return UserBook.objects.bulk_create(user_books)


@pytest.fixture(scope="module")
def user_fav_books(django_db_setup, django_db_blocker, two_books, user):
    with django_db_blocker.unblock():
        statuses = cycle('r c'.split())
        user_books = [
            UserBook(user=user, book=book, status=next(statuses),
                     favorite=True)
            for book in two_books
        ]
        return UserBook.objects.bulk_create(user_books)
