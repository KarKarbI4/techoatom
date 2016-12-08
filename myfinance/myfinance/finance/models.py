from django.conf.auth.models import User
from django.db import models


# Create your models here.


class Account(models.Model):

    name = models.CharField(max_length=20)
    card_num = models.CharField(max_length=16, default='000000000000')
    total = models.DecimalField(decimal_places=2, max_digits=1000, default=0)
    owner = models.ForeignKey(User, related_name='account')

    class Meta:
        db_table = 'accounts'


class Charge(models.Model):

    value = models.DecimalField(decimal_places=2, max_digits=300)
    date = models.DateField()
    account = models.ForeignKey(Account, related_name='charge')

    class Meta:
        db_table = 'charges'
