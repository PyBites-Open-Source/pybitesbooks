from django.conf.urls import url

from . import views

app_name = 'api'
urlpatterns = [
    url(r'^users/$', views.user_books, name='user_books'),
    url(r'^users/(?P<username>.*)$', views.user_books, name='user_books'),
    url(r'^random/$', views.random_book, name='random_book'),
    url(r'^random/(?P<grep>.*)$', views.random_book, name='random_book'),
    url(r'^books/(?P<bookid>.*)$', views.get_bookid, name='get_bookid'),
]
