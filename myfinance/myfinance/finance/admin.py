# Register your models here.
from django.contrib import admin
# from myfinance.myapp.models import Author

# class AuthorAdmin(admin.ModelAdmin):
    # pass
# admin.site.register(Author, AuthorAdmin)

from .models import User, Account, Charge

admin.site.register(User)
admin.site.register(Account)
admin.site.register(Charge)