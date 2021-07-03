from django import forms
from django.forms import ModelForm

from .models import UserBook


class DateInput(forms.DateInput):
    input_type = 'text'


class UserBookForm(ModelForm):

    class Meta:
        model = UserBook
        fields = ['status', 'completed']
        widgets = {
            'completed': DateInput(),
        }
