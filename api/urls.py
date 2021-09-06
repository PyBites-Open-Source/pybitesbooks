from django.urls import path

from . import views

app_name = 'api'
urlpatterns = [
    path('users', views.user_books, name='user_books'),
    path('users/<str:username>', views.user_books, name='user_books'),
    path('random', views.random_book, name='random_book'),
    path('random/<str:grep>', views.random_book, name='random_book'),
    path('books/<str:bookid>', views.get_bookid, name='get_bookid'),
    path('lists/<str:name>', views.get_book_list, name='get_book_list'),
]
