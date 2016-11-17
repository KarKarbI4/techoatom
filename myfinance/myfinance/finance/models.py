from django.db import models

# Create your models here.


class Charge(models.Model):

    value = models.DecimalField(decimal_places=2, max_digits=300)
    date = models.DateField()

    class Meta:
        db_table = 'charges'
