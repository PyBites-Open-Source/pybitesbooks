import pytest

from books.models import Book


@pytest.mark.parametrize("bookid, title", [
    ("nneBa6-mWfgC", "Coders at Work"),
    ("__CvAFrcWY0C", "Unlimited Power"),
    ("3V_6DwAAQBAJ", "Power Vs. Force"),
    ("bK1ktwAACAAJ", "177 Mental Toughness Secrets of the World Class"),
])
def test_homepage_shows_books(client, books, bookid, title):
    response = client.get('/')
    expected = ('<a href="/books/{bookid}"><img class="thumbNail" '
                'src="http://books.google.com/books?id={bookid}&'
                'printsec=frontcover&img=1&zoom=1&source=gbs_gdata" '
                'alt="{title}"></a>').format(bookid=bookid,
                                             title=title)
    assert expected in response.content.decode()


def test_book_page_logged_out(client, books):
    response = client.get('/books/nneBa6-mWfgC')
    html = response.content.decode()
    assert "<td>Peter Seibel</td>" in html
    assert "<td>Apress</td>" in html
    assert "<td>2009-09-16</td>" in html
    assert "<td>978143021948463</td>" in html
    assert "<td>Page Count</td><td>632</td>" in html
    assert ('<form class="mui-form" id="addBookForm" '
            'method="post">') not in html


def test_book_page_logged_in(user, books):
    response = user.get('/books/nneBa6-mWfgC')
    html = response.content.decode()
    assert ('<form class="mui-form" id="addBookForm" '
            'method="post">') in html
