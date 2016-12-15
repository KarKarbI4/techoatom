from django.conf.urls import url

from finance.views import (account, accounts, create_account,
                           create_charge, homepage, login_view, logout_view,
                           profile, register_view, view_amount, edit_account, remove_account, edit_charge, remove_charge)

urlpatterns = [
    url(r'^$', homepage, name='homepage'),
    url(r'^accounts/$', accounts, name='accounts'),
    url(r'^accounts/new/$', create_account, name='create_account'),
    url(r'^accounts/(?P<account_id>\d+)/$', account, name='account'),
    url(r'^accounts/(?P<account_id>\d+)/amount/$',
        view_amount, name='account_total'),
    
    url(r'^accounts/(?P<account_id>\d+)/edit/$',
        edit_account, name='edit_account'),
    url(r'^accounts/(?P<account_id>\d+)/remove/$',
    remove_account, name='remove_account'),

    url(r'^accounts/(?P<account_id>\d+)/charges/(?P<charge_id>\d+)/edit/$',
        edit_charge, name='edit_charge'),
    url(r'^accounts/(?P<account_id>\d+)/charges/(?P<charge_id>\d+)/remove/$',
        remove_charge, name='remove_charge'),
    url(r'^accounts/(?P<account_id>\d+)/charges/new/$',
        create_charge, name='create_charge'),
    url(r'^login/$', login_view, name='login'),
    url(r'^register/$', register_view, name='register'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^profile/(?P<name>\w+)/$', profile, name='profile'),
    # url(r'^profile/(?P<name>\d+)/$', profile, name='profile'),
]