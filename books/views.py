import csv
from collections import OrderedDict, namedtuple
from datetime import date, datetime
from io import StringIO

from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import pytz

from .goodreads import (BookImportStatus,
                        GOOGLE_TO_GOODREADS_READ_STATUSES)
from .googlebooks import get_book_info
from .forms import UserBookForm, ImportBooksForm
from .models import (Book, UserBook, BookNote, ImportedBook,
                     READING, COMPLETED, TO_READ)
from .tasks import retrieve_google_books
from goal.models import Goal
from lists.models import UserList

MIN_NUM_BOOKS_SHOW_SEARCH = 20
TO_ADD = BookImportStatus.TO_BE_ADDED.name
NOT_FOUND = BookImportStatus.COULD_NOT_FIND.name
REQUIRED_GOODREADS_FIELDS = (
    "Title", "Author", "Exclusive Shelf",
    "Date Read", "Date Added", "Book Id"
)
UserStats = namedtuple('UserStats', ["num_books_added",
                                     "num_books_done",
                                     "num_pages_read"])


def book_page(request, bookid):
    post = request.POST

    # get book info
    book = get_book_info(bookid)
    userbook = None
    if request.user.is_authenticated:
        try:
            userbook = UserBook.objects.get(user=request.user, book=book)
        except UserBook.DoesNotExist:
            pass

    # a form was submitted
    book_edit = post.get('addOrEditBook')
    note_submit = post.get('noteSubmit')

    # book form
    if book_edit:
        status = post.get('status')
        completed = post.get('completed') or None

        userlists = post.getlist("userlists[]", [])
        booklists = UserList.objects.filter(name__in=userlists)

        if completed:
            completed = timezone.datetime.strptime(completed, '%Y-%m-%d')

        # this works without pk because Userbook has max 1 entry for user+book
        userbook, created = UserBook.objects.get_or_create(book=book,
                                                           user=request.user)
        userbook.booklists.set(booklists)

        action = None
        if created:
            action = 'added'
        elif userbook.user != request.user:
            messages.error(request, 'You can only edit your own books')
            return redirect('book_page')

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
                messages.error(request, 'Note does not exist for this user')
                return redirect('book_page')

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
        book_form = UserBookForm(
            initial=dict(status=userbook.status,
                         completed=userbook.completed))
    else:
        book_form = UserBookForm()

    # all notes (do last as new note might have been added)
    book_notes = BookNote.objects.select_related('user')
    if request.user.is_authenticated:
        filter_criteria = (
            Q(book=book) & (Q(user=request.user) | Q(public=True))
        )
        notes = book_notes.filter(filter_criteria)
    else:
        notes = book_notes.filter(book=book, public=True)
    notes = notes.order_by('-edited').all()

    book_users = UserBook.objects.select_related('user').filter(
        book=book, status=COMPLETED)

    user_lists = []
    if request.user.is_authenticated:
        user_lists = UserList.objects.filter(user=request.user)

    userbook_lists = {}
    if userbook:
        userbook_lists = {ul.name for ul in userbook.booklists.all()}

    book_on_lists = [
        ul.userlist.name for ul in
        UserBook.booklists.through.objects.select_related(
            'userbook__book'
        ).filter(userbook__book=book)
    ]

    return render(request, 'book.html', {'book': book,
                                         'notes': notes,
                                         'userbook': userbook,
                                         'userbook_lists': userbook_lists,
                                         'book_form': book_form,
                                         'book_users': book_users,
                                         'user_lists': user_lists,
                                         'book_on_lists': book_on_lists})


def get_user_goal(user):
    try:
        goal = Goal.objects.get(year=date.today().year,
                                user=user,
                                number_books__gt=0)
    except Goal.DoesNotExist:
        goal = None
    return goal


def group_userbooks_by_status(books):
    userbooks = OrderedDict(
        [(READING, []), (COMPLETED, []), (TO_READ, [])])
    for book in books:
        userbooks[book.status].append(book)
    return userbooks


def get_num_pages_read(books):
    return sum(
        int(book.book.pages) if str(book.book.pages).isdigit() else 0
        for book in books if book.done_reading)


def user_page(request, username):
    user = get_object_or_404(User, username=username)
    user_books = UserBook.objects.select_related('book').filter(
        user=user)

    completed_books_this_year, perc_completed = [], 0
    goal = get_user_goal(user)

    if goal is not None:
        completed_books_this_year = UserBook.objects.filter(
            user=user, status=COMPLETED, completed__year=goal.year
        )

        if goal.number_books > 0:
            perc_completed = int(
                completed_books_this_year.count() / goal.number_books * 100)

    is_me = request.user.is_authenticated and request.user == user
    share_goal = goal and (goal.share or is_me)

    grouped_user_books = group_userbooks_by_status(user_books)

    user_stats = UserStats(num_books_added=len(user_books),
                           num_books_done=len(grouped_user_books[COMPLETED]),
                           num_pages_read=get_num_pages_read(user_books))
    user_lists = UserList.objects.filter(user=user)

    return render(request, 'user.html',
                  {'grouped_user_books': grouped_user_books,
                   'username': username,
                   'user_stats': user_stats,
                   'goal': goal,
                   'share_goal': share_goal,
                   'completed_books_this_year': completed_books_this_year,
                   'perc_completed': perc_completed,
                   'min_books_search': MIN_NUM_BOOKS_SHOW_SEARCH,
                   'is_me': is_me,
                   'user_lists': user_lists})


@xframe_options_exempt
def user_page_widget(request, username):
    user = get_object_or_404(User, username=username)
    books = UserBook.objects.select_related('book').filter(
        user=user, status='c')
    return render(request, 'widget.html', {'books': books})


@login_required
def user_favorite(request):
    user = request.user
    book = request.GET.get('book')
    checked = True if request.GET.get('checked') == "true" else False
    userbook = UserBook.objects.get(user__username=user, book__bookid=book)
    userbook.favorite = checked
    userbook.save()
    return JsonResponse({"status": "success"})


def _is_valid_csv(file_content,
                  required_fields=REQUIRED_GOODREADS_FIELDS):
    reader = csv.DictReader(
        StringIO(file_content), delimiter=',')
    header = next(reader)
    return all(field in header for field in required_fields)


@login_required
def import_books(request):
    is_preview = request.path.endswith("preview")
    post = request.POST
    files = request.FILES
    import_form = ImportBooksForm()
    imported_books = []

    if "delete_import" in post:
        num_deleted, _ = ImportedBook.objects.filter(
            user=request.user).delete()
        msg = f"Deleted import ({num_deleted} books)"
        messages.success(request, msg)
        return redirect('books:import_books')

    elif "save_import_submit" in post:
        books_to_add = post.getlist("books_to_add")
        read_statuses = post.getlist("read_statuses")
        dates = post.getlist("dates")

        user_books = []
        for bookid, read_status, read_date in zip(
            books_to_add, read_statuses, dates
        ):
            completed_dt = pytz.utc.localize(
                datetime.strptime(read_date, '%Y-%m-%d'))
            book = Book.objects.filter(
                bookid=bookid).order_by("inserted").last()
            user_books.append(
                UserBook(
                    user=request.user,
                    book=book,
                    status=read_status,
                    completed=completed_dt
                )
            )
        UserBook.objects.bulk_create(user_books)

        # delete the cached items
        ImportedBook.objects.filter(user=request.user).delete()

        messages.success(request, f"{len(user_books)} books inserted")
        return redirect('user_page', username=request.user.username)

    elif "import_books_submit" in post:
        import_form = ImportBooksForm(post, files)
        if import_form.is_valid():
            file_content = (
                files['file'].read().decode('utf-8')
            )
            if not _is_valid_csv(file_content):
                error = (
                    "Sorry, the provided csv file does "
                    "not match the goodreads format ("
                    "required fields: "
                    f"{', '.join(REQUIRED_GOODREADS_FIELDS)})"
                )
                messages.error(request, error)
                return redirect('books:import_books')

            username = request.user.username

            retrieve_google_books.delay(
                file_content, username)

            msg = ("Thanks, we're processing your goodreads csv file. "
                   "We'll notify you by email when you can select "
                   "books for import into your PyBites Books account.")
            messages.success(request, msg)
            return redirect('books:import_books')

    elif is_preview:
        imported_books = ImportedBook.objects.filter(
            user=request.user).order_by('title')
        num_add_books = imported_books.filter(
            book_status=TO_ADD).count()
        if num_add_books == 0:
            error = "No new books to be imported"
            messages.error(request, error)
            return redirect('books:import_books')

    context = {
        "import_form": import_form,
        "imported_books": imported_books,
        "not_found": NOT_FOUND,
        "to_add": TO_ADD,
        "all_read_statuses": GOOGLE_TO_GOODREADS_READ_STATUSES.items(),
    }
    return render(request, 'import_books.html', context)
