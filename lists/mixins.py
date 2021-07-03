from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse


class OwnerRequiredMixin:
    """
    Making sure that only owners can update their objects.
    See https://stackoverflow.com/a/18176411
    """
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        obj = self.get_object()
        if obj.user != self.request.user:
            messages.error(self.request, "You are not the owner of this list")
            return HttpResponseRedirect(reverse('lists-view'))
        return super().dispatch(request, *args, **kwargs)
