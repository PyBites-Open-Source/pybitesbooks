from django import forms
from django.forms import ModelForm

from .models import UserBook, BookNote


class UserBookForm(ModelForm):

    # def __init__(self, *args, **kwargs):
    #    super().__init__(*args, **kwargs)

    class Meta:
        model = UserBook
        fields = ['status', 'completed']
        completed = forms.DateTimeField()
