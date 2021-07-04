from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.utils.text import slugify

from books.models import UserBook
from books.views import MIN_NUM_BOOKS_SHOW_SEARCH
from .models import UserList
from .mixins import OwnerRequiredMixin


class UserListListView(ListView):
    model = UserList


class UserListDetailView(DetailView):
    model = UserList
    slug_field = 'name'
    slug_url_kwarg = 'name'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        list_id = self.get_object().id
        books_on_list = UserBook.objects.select_related(
            "book"
        ).filter(
            booklists__id=list_id
        ).order_by("book__title")
        context['books_on_list'] = books_on_list
        context['min_num_books_show_search'] = MIN_NUM_BOOKS_SHOW_SEARCH
        return context


class UserListCreateView(CreateView):
    model = UserList
    fields = ['name']
    success_url = reverse_lazy('lists-view')

    def form_valid(self, form):
        form.instance.name = slugify(form.instance.name)
        if UserList.objects.filter(name=form.instance.name).count() > 0:
            form.add_error('name', 'This list already exists')
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
