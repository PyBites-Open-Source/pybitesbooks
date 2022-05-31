from collections import defaultdict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.utils.text import slugify
from decouple import config, Csv

from books.models import UserBook
from books.views import MIN_NUM_BOOKS_SHOW_SEARCH
from .models import UserList
from .mixins import OwnerRequiredMixin

MAX_NUM_USER_LISTS, MAX_NUM_ADMIN_LISTS = 10, 100
ADMIN_USERS = set(config('ADMIN_USERS', cast=Csv()))


def get_max_books(request):
    if request.user.username in ADMIN_USERS:
        return MAX_NUM_ADMIN_LISTS
    return MAX_NUM_USER_LISTS


class UserListListView(ListView):
    model = UserList

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        max_num_user_lists, num_lists_left = 0, 0
        if self.request.user.is_authenticated:
            max_num_user_lists = get_max_books(self.request)
            num_user_lists = UserList.objects.filter(
                user=self.request.user).count()
            num_lists_left = max_num_user_lists - num_user_lists
        context['num_lists_left'] = num_lists_left
        context['max_num_user_lists'] = max_num_user_lists
        return context


class UserListDetailView(DetailView):
    model = UserList
    slug_field = 'name'
    slug_url_kwarg = 'name'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        user_books = UserBook.objects.select_related(
            "book", "user"
        ).order_by("book__title")

        # TODO: deduplicate
        # users_by_bookid needs all user_books
        users_by_bookid = defaultdict(set)
        for ub in user_books:
            bookid = ub.book.bookid
            users_by_bookid[bookid].add(ub.user)

        # ... hence this filter should go after that
        user_books = user_books.filter(
            booklists__id=obj.id)

        users_by_bookid_sorted = {
            bookid: sorted(
                users,
                key=lambda user: user.username.lower()
            )
            for bookid, users in users_by_bookid.items()
        }

        books_by_category = defaultdict(list)
        # make sure books are only added once
        books_done = set()
        for ub in user_books:
            for category in ub.book.categories.all():
                if ub.book in books_done:
                    continue
                # only order by high level category
                category = category.name.split(" / ")[0].title()
                books_by_category[category].append(ub.book)
                books_done.add(ub.book)

        books_by_category_sorted = sorted(
            books_by_category.items()
        )

        context['user_books'] = user_books
        context['users_by_bookid'] = users_by_bookid_sorted
        context['books_by_category'] = books_by_category_sorted

        context['min_num_books_show_search'] = MIN_NUM_BOOKS_SHOW_SEARCH
        is_auth = self.request.user.is_authenticated
        context['is_me'] = is_auth and self.request.user == obj.user
        return context


class UserListCreateView(LoginRequiredMixin, CreateView):
    model = UserList
    fields = ['name']
    success_url = reverse_lazy('lists-view')

    def form_valid(self, form):
        form.instance.name = slugify(form.instance.name)
        user_lists = UserList.objects
        if user_lists.filter(name=form.instance.name).count() > 0:
            form.add_error('name', 'This list already exists')
            return self.form_invalid(form)
        max_num_user_lists = get_max_books(self.request)
        if user_lists.filter(user=self.request.user).count() > max_num_user_lists:
            form.add_error(
                'name',
                f'You can have {max_num_user_lists} lists at most')
            return self.form_invalid(form)
        form.instance.user = self.request.user
        return super().form_valid(form)


class UserListUpdateView(OwnerRequiredMixin, UpdateView):
    model = UserList
    fields = ['name']
    success_url = reverse_lazy('lists-view')

    def form_valid(self, form):
        form.instance.name = slugify(form.instance.name)
        old_value = UserList.objects.get(pk=self.object.pk).name
        # this if is there in case user saves existing value without change
        if old_value != form.instance.name:
            if UserList.objects.filter(name=form.instance.name).count() > 0:
                form.add_error('name', 'This list already exists')
                return self.form_invalid(form)
        return super().form_valid(form)


class UserListDeleteView(OwnerRequiredMixin, DeleteView):
    model = UserList
    success_url = reverse_lazy('lists-view')
