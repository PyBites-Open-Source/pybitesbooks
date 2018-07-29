from collections import OrderedDict

from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .googlebooks import get_book_info
from .forms import UserBookForm
from .models import UserBook


def book_page(request, bookid):
    post = request.POST

    book = get_book_info(bookid)

    submitted = post.get('addBookSubmit')
    status = post.get('status')
    completed = post.get('completed') or None
    if completed:
        completed = timezone.datetime.strptime(completed, '%Y-%m-%d')

    userbook = None
    if submitted and status:
        userbook, created = UserBook.objects.get_or_create(book=book,
                                                        user=request.user)
        userbook.status = status
        userbook.completed = completed
        userbook.save()

        action = created and 'added' or 'updated'
        messages.success(request, f'Successfully {action} book')

    if request.method == 'POST':
        form = UserBookForm(post)
    elif userbook:
        # make sure to bounce back previously entered form values
        form = UserBookForm(initial=dict(status=userbook.status,
                                         completed=userbook.completed))
    else:
        form = UserBookForm()

    return render(request, 'book.html', {'book': book,
                                         'userbook': userbook,
                                         'form': form})


def user_page(request, username):
    user = get_object_or_404(User, username=username)
    books = UserBook.objects.select_related('book').filter(user=user).order_by('-updated').all()

    userbooks = OrderedDict([('r', []), ('c', []), ('t', [])])
    books_pages = []
    for book in books:
        userbooks[book.status].append(book)
        try:
            pages = book.done_reading and int(book.book.pages) or 0
        except ValueError:
            pages = 0
        books_pages.append(pages)

    return render(request, 'user.html', {'userbooks': userbooks,
                                         'username': username,
                                         'num_books': len(books_pages),
                                         'num_pages': sum(books_pages)})
