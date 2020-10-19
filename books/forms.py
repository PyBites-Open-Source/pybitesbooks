from django import forms
from django.forms import ModelForm

from .models import UserBook, BookNote


class DateInput(forms.DateInput):
    input_type = 'text'


class UserBookForm(ModelForm):

    # def __init__(self, *args, **kwargs):
    #    super().__init__(*args, **kwargs)

    class Meta:
        model = UserBook
        fields = ['status', 'completed']
        widgets = {
            'completed': DateInput(),
        }
