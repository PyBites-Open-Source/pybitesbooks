from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .models import UserList


class UserListListView(ListView):
    model = UserList


class UserListCreateView(LoginRequiredMixin, CreateView):
    model = UserList
    fields = ['name']
    success_url = reverse_lazy('lists-view')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UserListUpdateView(UpdateView):
    model = UserList
    fields = ['name']
    success_url = reverse_lazy('lists-view')


class UserListDeleteView(DeleteView):
    model = UserList
    success_url = reverse_lazy('lists-view')
