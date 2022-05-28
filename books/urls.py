from django.urls import path

from books import views as book_views

app_name = 'books'
urlpatterns = [
    path('import_books/preview', book_views.import_books, name='import_books'),
    path('import_books', book_views.import_books, name='import_books'),
    path('<str:bookid>', book_views.book_page, name='book_page'),
    path('categories/<path:category_name>', book_views.books_per_category, name='books_per_category'),
]
