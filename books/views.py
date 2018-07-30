from collections import OrderedDict

from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .googlebooks import get_book_info
from .forms import UserBookForm
from .models import (UserBook, BookNote,
                    READING, COMPLETED, TO_READ)


def book_page(request, bookid):
    post = request.POST

    # get book info
    book = get_book_info(bookid)
    try:
        userbook = UserBook.objects.get(user=request.user, book=book)
    except UserBook.DoesNotExist:
        userbook = None

    # a form was submitted
    book_edit = post.get('addOrEditBook')
    note_submit = post.get('noteSubmit')

    # book form
    if book_edit:
        status = post.get('status')
        completed = post.get('completed') or None
        if completed:
            completed = timezone.datetime.strptime(completed, '%Y-%m-%d')

        # this works without pk because Userbook has max 1 entry for user+book
        userbook, created = UserBook.objects.get_or_create(book=book,
                                                           user=request.user)

        action = None
        if created:
            action = 'added'
        elif userbook.user != request.user:
            messages.error('You can only edit your own books')
            redirect('book_page')

        if post.get('deleteBook'):
            action = 'deleted'
            userbook.delete()
            userbook = None
        else:
            action = 'updated'
            userbook.status = status
            userbook.completed = completed
            userbook.save()

        messages.success(request, f'Successfully {action} book')

    # note form (need a valid userbook object!)
    elif userbook and note_submit:
        type_note = post.get('type_note')
        description = post.get('description')
        public = post.get('public') and True or False

        noteid = post.get('noteid')
        action = None
        # delete/ update
        if noteid:
            try:
                usernote = BookNote.objects.get(pk=noteid, user=request.user)
            except BookNote.DoesNotExist:
                messages.error('Note does not exist for this user')
                redirect('book_page')

            if usernote:
                if post.get('deleteNote'):
                    action = 'deleted'
                    usernote.delete()
                    usernote = None
                else:
                    action = 'updated'
                    usernote.type_note = type_note
                    usernote.description = description
                    usernote.public = public
                    usernote.save()
        # add
        else:
            action = 'added'
            usernote = BookNote(user=request.user,
                                book=book,
                                userbook=userbook,
                                type_note=type_note,
                                description=description,
                                public=public)
            usernote.save()

        messages.success(request, f'Successfully {action} note')

    # prepare book form (note form = multiple = best manual)
    if userbook:
        # make sure to bounce back previously entered form values
        book_form = UserBookForm(initial=dict(status=userbook.status,
                                              completed=userbook.completed))
    else:
        book_form = UserBookForm()

    # all notes (do last as new note might have been added)
    filter_criteria = Q(book=book) & (Q(user=request.user) | Q(public=True))
    notes = BookNote.objects.select_related('user').filter(filter_criteria)
    notes = notes.order_by('-edited').all()

    book_users = UserBook.objects.select_related('user').filter(book=book,
                                                                status=COMPLETED)

    return render(request, 'book.html', {'book': book,
                                         'notes': notes,
                                         'userbook': userbook,
                                         'book_form': book_form,
                                         'book_users': book_users})


def user_page(request, username):
    user = get_object_or_404(User, username=username)
    books = UserBook.objects.select_related('book').filter(user=user).order_by('-updated').all()

    userbooks = OrderedDict([(READING, []), (COMPLETED, []), (TO_READ, [])])
    books_pages = []
    for book in books:
        userbooks[book.status].append(book)

        if not book.done_reading:
            continue

        # only count pages on books read
        try:
            pages = int(book.book.pages) or 0
        except ValueError:
            pages = 0
        books_pages.append(pages)

    return render(request, 'user.html', {'userbooks': userbooks,
                                         'username': username,
                                         'num_books_added': len(userbooks),
                                         'num_books_done': len(books_pages),
                                         'num_pages_read': sum(books_pages)})
