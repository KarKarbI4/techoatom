# Register your models here.
from django.contrib import admin
from .models import User, Account, Charge
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # def get_readonly_fields(self, request, obj=None):
    #     if obj:
    #         return self.readonly_fields + ('username',)
    #     return self.readonly_fields
    list_display = ('username','first_name', 'last_name', 'email', 'phone_number', 'address')
    search_fields = ('username','first_name', 'last_name', 'email', 'phone_number', 'address')
    list_filter = ('username',)
    list_display_links = ('first_name', 'last_name', 'email', 'phone_number', 'address')
    list_max_show_all = 10
    list_per_page = 5

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('owner',)
        return self.readonly_fields
    list_display = ('name', 'card_num', 'total', 'owner')
    search_fields = ('name', 'card_num', 'total', 'owner__username')
    list_filter = ('name', 'card_num', 'total', 'owner')
    list_display_links = ('name', 'card_num', 'total',)
    list_max_show_all = 10
    list_per_page = 5

@admin.register(Charge)
class ChargeAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('account',)
        return self.readonly_fields
    list_display = ('value', 'date', 'account')
    search_fields = ('value', 'date', 'account__name')
    list_filter = ('value', 'date', 'account')
    list_display_links = ('value', 'date')
    list_max_show_all = 10
    list_per_page = 5