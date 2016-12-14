from django.conf.urls import url

from finance.views import (account, accounts, create_account,
                           create_charge, homepage, login_view, logout_view,
                           profile, register_view, view_amount)

urlpatterns = [
    url(r'^$', homepage, name='homepage'),
    url(r'^accounts/$', accounts, name='accounts'),
    url(r'^accounts/new/$', create_account, name='create_account'),
    url(r'^accounts/(?P<account_id>\d+)/$', account, name='account'),
    url(r'^accounts/(?P<account_id>\d+)/amount/$',
        view_amount, name='account_total'),
    url(r'^accounts/(?P<account_id>\d+)/charges/new/$',
        create_charge, name='create_charge'),
    url(r'^login/$', login_view, name='login'),
    url(r'^register/$', register_view, name='register'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^profile/$', profile, name='profile'),
]
