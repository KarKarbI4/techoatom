from datetime import datetime
from datetime import date

from django import forms
from django.core.exceptions import ValidationError

class ChargeForm(forms.Form):
    value = forms.DecimalField(label='Value', required=True)
    date = forms.DateField(label='Date', required=True)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('value') < 0 and \
        cleaned_data.get('date') > date.today():
            self.add_error('date', 'Charge off are not supported for future days')
        return cleaned_data