from django.contrib.auth.models import User
import pytest

from books.models import Book


@pytest.fixture
def books(db):
    books = [
        Book(bookid="nneBa6-mWfgC",
             title="Coders at Work",
             authors="Peter Seibel",
             publisher="Apress",
             published="2009-09-16",
             isbn="978143021948463",
             pages=632,
             language="en",
             description=("<p>Peter Seibel interviews 15 of the most "
                          "interesting computer programmers alive ...")),
        Book(bookid="__CvAFrcWY0C",
             title="Unlimited Power",
             authors="Tony Robbins",
             publisher="Simon and Schuster",
             published="2008-06-30",
             isbn="978141658637144",
             pages=448,
             language="en",
             description=("<p>Anthony Robbins calls it the "
                          "new science of personal achievement ...")),
        Book(bookid="3V_6DwAAQBAJ",
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
        Book(bookid="bK1ktwAACAAJ",
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
    Book.objects.bulk_create(books)
    return Book.objects.all()


@pytest.fixture
def user(db, client):
    username, password = "user1", 'bar'
    user = User.objects.create_user(username=username, password=password)
    client.login(username=username, password=password)
    return client
