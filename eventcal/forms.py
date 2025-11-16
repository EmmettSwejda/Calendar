from django.forms import ModelForm
from django import forms
from eventcal.models import CalendarConfig


# The form to get the calendar link
class CalendarConfigForm(ModelForm):
    url = forms.TextInput()
    class Meta:
        model = CalendarConfig
        fields = ['url']