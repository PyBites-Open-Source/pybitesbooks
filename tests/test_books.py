import re

import pytest

pytestmark = pytest.mark.django_db


def test_homepage_shows_user_completed_books(client, user_books):
    response = client.get('/')
    html = response.content.decode()
    book1 = ('<a href="/books/__CvAFrcWY0C"><img class="thumbNail" '
             'src="http://books.google.com/books?id=__CvAFrcWY0C&'
             'printsec=frontcover&img=1&zoom=1&source=gbs_gdata" '
             'alt="Unlimited Power"></a>')
    book2 = ('<a href="/books/bK1ktwAACAAJ"><img class="thumbNail" '
             'src="http://books.google.com/books?id=bK1ktwAACAAJ&'
             'printsec=frontcover&img=1&zoom=1&source=gbs_gdata" '
             'alt="177 Mental Toughness Secrets of the World Class">'
             '</a>')
    assert book1 in html
    assert book2 in html


def test_book_page_logged_out(client, books):
    response = client.get('/books/nneBa6-mWfgC')
    html = response.content.decode()
    assert "<td>Peter Seibel</td>" in html
    assert "<td>Apress</td>" in html
    assert "<td>978143021948463</td>" in html
    assert not re.search(r"<form.*addBookForm", html)
    assert "Computers / Programming / General" in html
    assert "Computers / Information Technology" in html


def test_book_page_logged_in(login, books):
    response = login.get('/books/nneBa6-mWfgC')
    html = response.content.decode()
    assert re.search(r"<form.*addBookForm", html)
    assert "Computers / Programming / General" in html
    assert "Computers / Information Technology" in html


def test_user_profile_page(client, user, user_books):
    response = client.get(f'/users/{user.username}')
    html = response.content.decode()
    assert "Reading (2)" in html
    assert "Completed (2)" in html
    assert "Wants to read (0)" in html
    assert "wow you read 2 books!" in html
    assert "World Class - completed" in html
    assert "Unlimited Power - completed" in html
    assert re.search(r"Total reading:.*>4<.* books added", html)
    assert re.search(r"of which.*>2<.* read .*>729<.* pages", html)


@pytest.mark.parametrize("snippet", [
    'nneBa6-mWfgC >',
    '__CvAFrcWY0C >',
    '3V_6DwAAQBAJ >',
    'bK1ktwAACAAJ >',
    'jaM7DwAAQBAJ  checked>',
    'UCJMRAAACAAJ  checked>',
])
def test_user_profile_page_stars(client, user, user_fav_books, snippet):
    response = client.get(f'/users/{user.username}')
    html = response.content.decode()
    assert (f'<input class="js-favorite" title="favorite"'
            f' type="checkbox" bookid={snippet}') in html
