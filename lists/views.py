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
        books_on_list = UserBook.objects.select_related(
            "book"
        ).filter(
            booklists__id=obj.id
        ).order_by("book__title")
        context['books_on_list'] = books_on_list
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
