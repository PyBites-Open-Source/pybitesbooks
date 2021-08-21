from django import forms
from django.forms import ModelForm

from .models import UserBook


class DateInput(forms.DateInput):
    input_type = 'text'


class ImportBooksForm(forms.Form):
    file = forms.FileField()


class UserBookForm(ModelForm):

    class Meta:
        model = UserBook
        fields = ['status', 'completed', 'booklists']
        widgets = {
            'completed': DateInput(),
        }
