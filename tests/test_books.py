import pytest

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize("bookid, title", [
    ("nneBa6-mWfgC", "Coders at Work"),
    ("__CvAFrcWY0C", "Unlimited Power"),
    ("3V_6DwAAQBAJ", "Power Vs. Force"),
    ("bK1ktwAACAAJ", "177 Mental Toughness Secrets of the World Class"),
])
def test_homepage_shows_books(client, books, bookid, title):
    response = client.get('/')
    expected = (f'<a href="/books/{bookid}"><img class="thumbNail" '
                f'src="http://books.google.com/books?id={bookid}&'
                'printsec=frontcover&img=1&zoom=1&source=gbs_gdata" '
                f'alt="{title}"></a>')
    assert expected in response.content.decode()


@pytest.mark.parametrize("snippet, is_in", [
    ("<td>Peter Seibel</td>", True),
    ("<td>Apress</td>", True),
    ("<td>2009-09-16</td>", True),
    ("<td>978143021948463</td>", True),
    ("<td>Page Count</td><td>632</td>", True),
    (('<form class="mui-form" id="addBookForm" '
      'method="post">'), False),
])
def test_book_page_logged_out(client, books, snippet, is_in):
    response = client.get('/books/nneBa6-mWfgC')
    html = response.content.decode()
    assert snippet in html if is_in else snippet not in html


def test_book_page_logged_in(login, books):
    response = login.get('/books/nneBa6-mWfgC')
    html = response.content.decode()
    assert ('<form class="mui-form" id="addBookForm" '
            'method="post">') in html


@pytest.mark.parametrize("snippet", [
    "Reading (2)",
    "Completed (2)",
    "Wants to read (0)",
    "wow you read 2 books!",
    "World Class - completed",
    "Unlimited Power - completed",
    ('Total reading: <strong class="mui--text-title">'
        '4</strong> books added'),
    ('of which <strong class="mui--text-title">2</strong>'
        ' read totalling '),
    '<strong class="mui--text-title">729</strong> pages.'
])
def test_user_profile_page(client, user, user_books, snippet):
    response = client.get(f'/users/{user.username}')
    html = response.content.decode()
    assert snippet in html


def test_user_profile_page_no_favorites(client, user):
    response = client.get(f'/users/{user.username}')
    html = response.content.decode()
    assert 'Favorite Books' not in html


def test_user_profile_page_favorites(client, user, user_fav_books):
    response = client.get(f'/users/{user.username}')
    html = response.content.decode()
    assert 'Favorite Books' in html


@pytest.mark.parametrize("snippet, is_in", [
    ("bookid=nneBa6-mWfgC  checked", False),
    ("bookid=__CvAFrcWY0C  checked", False),
    ("bookid=3V_6DwAAQBAJ  checked", False),
    ("bookid=bK1ktwAACAAJ  checked", False),
    ("bookid=jaM7DwAAQBAJ  checked", True),
    ("bookid=UCJMRAAACAAJ  checked", True),
])
def test_user_profile_page_stars(client, user, user_fav_books, snippet, is_in):
    response = client.get(f'/users/{user.username}')
    html = response.content.decode()
    assert snippet in html if is_in else snippet not in html
