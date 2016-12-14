from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models, transaction
from django.db.models import Func

# Create your models here.


class CardNumValidator:

    CREDIT_CARD_RE = r'^(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\\d{3})\d{11})$'

    def __init__(self, message="Please, specify valid card number."):
        self.message = message
        self.validator = RegexValidator(
            regex=CardNumValidator.CREDIT_CARD_RE, message=self.message)

    def __call__(self, card_num):
        return self.validator(card_num)


class User(AbstractUser):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    # validators should be a list
    phone_number = models.CharField(max_length=16, validators=[
                                    phone_regex], blank=True)
    address = models.CharField(max_length=256, blank=True)


class Account(models.Model):

    name = models.CharField(max_length=20)
    card_num = models.CharField(
        max_length=16, default='000000000000', validators=[CardNumValidator], unique=True)
    total = models.DecimalField(decimal_places=2, max_digits=1000, default=0)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='accounts')

    @transaction.atomic
    def make_charge(self, charge):
        self.total += charge.value
        self.save()

    class Meta:
        db_table = 'accounts'

    def __str__(self):
        return str(self.name)


class Charge(models.Model):

    value = models.DecimalField(decimal_places=2, max_digits=300)
    date = models.DateField()
    account = models.ForeignKey(Account, related_name='charges')

    def save(self, *args, **kwargs):
        self.account.make_charge(self)
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'charges'

    def __str__(self):
        return str(self.value)


class Month(Func):
    function = 'EXTRACT'
    template = '%(function)s(MONTH from %(expressions)s)'
    output_field = models.IntegerField()
