from django.contrib import messages
from django.shortcuts import render
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

    userbook, created = UserBook.objects.get_or_create(book=book,
                                                       user=request.user)

    if submitted and status:
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
