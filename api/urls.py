from django.conf.urls import url

from myreadinglist import views as main_views
from . import views

app_name = 'api'
urlpatterns = [
    url(r'^get_books/', main_views.get_books, name='get_books'),
    url(r'^users/$', views.user_books, name='user_books'),
    url(r'^users/(?P<username>.*)$', views.user_books, name='user_books'),
    url(r'^random/$', views.random_book, name='random_book'),
    url(r'^random/(?P<grep>.*)$', views.random_book, name='random_book'),
]
