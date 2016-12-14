# Register your models here.
from django.contrib import admin

from .models import User, Account, Charge

admin.site.register(User)
admin.site.register(Account)
admin.site.register(Charge)