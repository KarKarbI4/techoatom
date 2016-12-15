from calendar import month_abbr
from datetime import datetime
from decimal import Decimal, getcontext

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models, transaction
from django.db.models import Func, Sum

from finance.validators import ValidateCreditCard
# Create your models here.


class User(AbstractUser):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    # validators should be a list
    phone_number = models.CharField(max_length=16, validators=[
                                    phone_regex], blank=False)
    address = models.CharField(max_length=256, blank=True)


class Account(models.Model):

    name = models.CharField(max_length=20)
    card_num = models.CharField(
        max_length=16, default='000000000000', validators=[ValidateCreditCard], unique=True)
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

    def __str__(self):
        return str(self.name)

    def get_hist_data(charges):
        end_date = datetime.today()
        m = end_date.month
        start_date = end_date - relativedelta(months=12, days=end_date.day - 1)

        latest_year_charges = charges.filter(
            date__range=[start_date, end_date])
        agg_data = latest_year_charges.annotate(month=Month('date')).values(
            'month').annotate(total=Sum('value')).order_by('month')

        getcontext().prec = 3

        hist_values = [[month_abbr[(i + m - 1) % 12 + 1], 0.0]
                       for i in range(1, 13)]

        for rec in agg_data:
            hist_values[(rec['month'] + m - 1) % 12][1] = float(rec['total'])
        return hist_values


class Charge(models.Model):

    value = models.DecimalField(decimal_places=2, max_digits=300, default="1")
    date = models.DateField(default=datetime.today())
    account = models.ForeignKey(Account, related_name='charges')

    class Meta:
        db_table = 'charges'

    def __str__(self):
        return str(self.value)

class Month(Func):
    function = 'EXTRACT'
    template = '%(function)s(MONTH from %(expressions)s)'
    output_field = models.IntegerField()
