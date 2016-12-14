from django.conf.urls import url
from finance.views import hist

urlpatterns = [
    url(r'^hist$', hist, name='hist'),  
    ]