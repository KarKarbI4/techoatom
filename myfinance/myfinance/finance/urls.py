from django.conf.urls import url
from finance.views import homepage, charges

urlpatterns = [
    url(r'^$', homepage),
    url(r'^charges/$', charges),
]