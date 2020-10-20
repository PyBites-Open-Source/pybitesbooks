from django.urls import path

from books import views as book_views

app_name = 'books'
urlpatterns = [
    path('<str:bookid>', book_views.book_page, name='book_page'),
]
