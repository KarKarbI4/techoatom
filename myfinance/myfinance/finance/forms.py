import re
from datetime import date, datetime
from django import forms

from django.core.exceptions import ValidationError
from django.forms import ModelForm

from finance.models import Account, Charge, User
from finance.validators import StripToNumbers, ValidateLuhnChecksum, ValidateCharacters


class ChargeForm(ModelForm):

    class Meta:
        model = Charge
        fields = ['value', 'date']

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        value = cleaned_data.get('value')
        if value == 0:
            self.add_error('value', 'Charge value must be not a zero')
        if not date:
            self.add_error('date', 'Please, specify correct date in format yyyy-mm-dd.')
        if value < 0 and date > date.today():
            self.add_error(
                'date', 'Charges off are not supported for future days. Please, try again.')
        return cleaned_data


class AccountForm(ModelForm):

    def clean_card_num(self):
        card_num = self.cleaned_data['card_num']
        if not ValidateCharacters(card_num):
            raise forms.ValidationError('Can only contain numbers and spaces.')
        card_num = StripToNumbers(card_num)
        if not ValidateLuhnChecksum(card_num):
            raise forms.ValidationError('Not a valid credit card number.')
        return card_num

    class Meta:
        model = Account
        fields = ['name', 'card_num', 'total']


class LoginForm(ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password']


class RegisterForm(ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())
    password_confirm = forms.CharField(
        required=True, widget=forms.PasswordInput(), label="Confirm password")

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('password_confirm'):
            self.add_error(
                'password_confirm', 'Passwords should match.')
        return cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'phone_number', 'address']


class ProfileForm(ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'address']
