from datetime import datetime
from datetime import date

from django import forms
from django.forms import ModelForm
from finance.models import Charge
from django.core.exceptions import ValidationError


class ChargeForm(ModelForm):

    class Meta:
        model = Charge
        fields = ['value', 'date']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('value') < 0 and \
                cleaned_data.get('date') > date.today():
            self.add_error(
                'date', 'Charges off are not supported for future days. Please, try again.')
        return cleaned_data
