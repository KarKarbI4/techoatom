from django.conf.urls import url
from finance.views import homepage, charges, create_charge

urlpatterns = [
    url(r'^$', homepage, name='homepage'),
    url(r'^charges/$', charges, name='charges'),
    url(r'^create_charge/$', create_charge, name='create_charge'),
]