from collections import OrderedDict

from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .googlebooks import get_book_info
from .forms import UserBookForm
from .models import UserBook, BookNote


def book_page(request, bookid):
    post = request.POST
    print(post)

    # return vars
    userbook = None

    # get book info
    book = get_book_info(bookid)

    # a form was submitted
    book_edit = post.get('bookSubmit')
    note_edit = post.get('noteSubmit')

    # book form
    if book_edit:
        status = post.get('status')
        completed = post.get('completed') or None
        if completed:
            completed = timezone.datetime.strptime(completed, '%Y-%m-%d')

        userbook, created = UserBook.objects.get_or_create(book=book,
                                                           user=request.user)
        userbook.status = status
        userbook.completed = completed
        userbook.save()

        action = created and 'added' or 'updated'
        messages.success(request, f'Successfully {action} book')

    # note form
    elif note_edit:
        noteid = post.get('noteid')
        type_note = post.get('type_note')
        description = post.get('description')
        private = post.get('private') and True or False

        usernote, created = BookNote.objects.get_or_create(book=book,
                                                           user=request.user,
                                                           pk=noteid)

        if not created and usernote.user != request.user:
            messages.error('You can only edit your own notes')
            redirect('book_page')

        usernote.type_note = type_note
        usernote.description = description
        usernote.private = private
        usernote.save()

        action = created and 'added' or 'updated'
        messages.success(request, f'Successfully {action} note')

        # reset form values
        # noteid, type_note, description, private = None, None, None, None

    # prepare book form (note form = multiple = best manual)
    if request.method == 'POST':
        book_form = UserBookForm(post)
    elif userbook:
        # make sure to bounce back previously entered form values
        book_form = UserBookForm(initial=dict(status=userbook.status,
                                              completed=userbook.completed))
    else:
        book_form = UserBookForm()

    # all notes (do last as new note might have been added)
    notes = BookNote.objects.filter(book=book)

    return render(request, 'book.html', {'book': book,
                                         'notes': notes,
                                         'userbook': userbook,
                                         # book form is via Django Form
                                         'book_form': book_form,
                                         # note form = multiple = manual
                                         })


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
