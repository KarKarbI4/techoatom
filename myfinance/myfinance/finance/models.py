from django.db import models

# Create your models here.


class Account(models.Model):

    total = models.DecimalField(decimal_places=2, max_digits=1000)

    class Meta:
        db_table = 'accounts'


class Charge(models.Model):

    value = models.DecimalField(decimal_places=2, max_digits=300)
    date = models.DateField()
    account = models.ForeignKey(Account, related_name='charge')

    class Meta:
        db_table = 'charges'
