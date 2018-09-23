from django.conf.urls import url

from books import views as book_views

app_name = 'books'
urlpatterns = [
    url(r'^(?P<bookid>.*)$', book_views.book_page, name='book_page'),
]
