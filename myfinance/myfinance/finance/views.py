from django.shortcuts import render
from django.http import HttpResponse

from finance.utils import get_html, gen_table

def homepage(request):
    title = 'Homepage'
    body = '''
    <h1>Welcome to Myfinance Homepage!</h1>
    <a href='charges/'>My charges</a>
    '''
    html = get_html(title, body)
    return HttpResponse(html)

# Create your views here.
def charges(request):
    title = 'My Charges'
    body = "<a href='/'>Homepage</a>\n"
    body += gen_table()
    html = get_html(title, body)
    return HttpResponse(html)