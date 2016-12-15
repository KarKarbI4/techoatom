import json
from calendar import month_abbr
from datetime import datetime
from decimal import Decimal, getcontext

from dateutil.relativedelta import relativedelta
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.messages import error
from django.core.exceptions import PermissionDenied
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_POST, require_GET


from finance.forms import (AccountForm, ChargeForm, LoginForm, ProfileForm,
                           RegisterForm)
from finance.models import Account, Charge, Month, User
from finance.random_transactions import random_transactions

from smtplib import SMTP_SSL
from email import encoders
import os
from email.mime.text import MIMEText

def isOwnerOrAdmin(f):

    @login_required
    def wrapper(request, account_id, *args, **kwargs):
        if Account.objects.get(id=account_id).owner != request.user or (not request.user.is_staff):
            raise PermissionDenied
        return f(request, account_id, *args, **kwargs)
    return wrapper

def OwnerOrAdmin2(f):

    @login_required
    def wrapper(request, account_id, *args, **kwargs):
        if Account.objects.get(id=account_id).owner != request.user or (not request.user.is_staff):
            raise PermissionDenied
        return f(request, account_id, *args, **kwargs)
    return wrapper



def homepage(request):
    return render(request, 'finance/index.html')


def logout_view(request):
    logout(request)
    return(redirect(reverse('charges:homepage')))


@csrf_exempt
@require_http_methods(['GET', 'POST'])
def login_view(request):
    login_form = LoginForm()
    next_url = None

    if request.method == "GET" and request.GET.get('next', None) is not None:
        next_url = request.GET['next']

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                if request.POST.get('next', None):
                    print("Next url: {}".format(request.POST.get('next')))
                    return redirect(request.POST['next'])
                return redirect(reverse('charges:accounts'))
            error(request, 'Wrong username or password!')

    context = {
        'login_form': login_form,
        'next': next_url,
    }

    return render(request, 'finance/login.html', context=context)


def send_email(user_email):
    message = 'Thanks you for selecting our service !!!'
    address = 'coolfinanceteam@yandex.ru'
    address_to = user_email
    msg = MIMEText(message)
    msg['From'] = address
    msg['To'] = address_to
    smtp = SMTP_SSL()
    smtp.connect('smtp.yandex.ru')
    smtp.login(address, 'qwerty12345')
    smtp.sendmail(address, address_to, msg.as_string())
    smtp.quit()

@csrf_exempt
def register_view(request):
    if request.method == "GET":
        register_form = RegisterForm()

    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            user = authenticate(username=register_form.cleaned_data[
                'username'], password=register_form.cleaned_data['password'])
            print(dir(register_form))
            send_email(request.POST['email'])
            if not user:
                error(request, 'Wrong username or password!')
                return redirect(reverse('charges:login'))
            login(request, user)
            return redirect(reverse('charges:accounts'))

    context = {
        'register_form': register_form
    }

    return render(request, 'finance/register.html', context=context)


@require_http_methods(['POST', 'GET'])
@login_required
@csrf_exempt
def profile(request, name):
    profile = User.objects.get(username=name)
    profile_form = ProfileForm(
        request.POST or None, request.FILES or None, instance=profile)
    success = None

    if request.method == "POST":
        if profile_form.is_valid():
            profile_form.save()
            success = True
        else:
            success = False

    context = {
        'profile_form': profile_form,
        'success': success,
        'profile': profile,
        
    }
    return render(request, 'finance/profile.html', context=context)


@login_required
@isOwnerOrAdmin
def view_amount(request, account_id):
    total = Account.objects.get(id=account_id).total
    context = {
        'total': total,
    }
    return render(request, 'finance/view_account_total.html', context=context)


@login_required
@isOwnerOrAdmin
def remove_charge(request, account_id, charge_id):
    charge = Charge.objects.get(id=charge_id)
    acc = Account.objects.get(id=account_id)
    charge.delete()
    return redirect(reverse('charges:account', kwargs={'account_id': acc.id}))

@login_required
@isOwnerOrAdmin
def edit_charge(request, account_id, charge_id):
    charge = Charge.objects.get(id=charge_id)
    acc = Account.objects.get(id=account_id)
    charge_form = ChargeForm(
        request.POST or None, request.FILES or None, instance=charge)
    success = None
    if request.method == 'POST':
        if charge_form.is_valid():
            charge_form.save()
            success = True
            return redirect(reverse('charges:account', kwargs={'account_id': acc.id}) + '?success=True')
        else:
            success = False
    context = {
        'success': success,
        'charge_form': charge_form,
        'charge': charge,
        'account': acc,
    }
    return render(request, 'finance/edit_charge.html', context)






@login_required
@isOwnerOrAdmin
def remove_account(request, account_id):
    acc = Account.objects.get(id=account_id)
    acc.delete()
    return redirect(reverse('charges:accounts'))


@login_required
@isOwnerOrAdmin
def edit_account(request, account_id):
    acc = Account.objects.get(id=account_id)
    account_form = AccountForm(
        request.POST or None, request.FILES or None, instance=acc)
    success = None

    if request.method == 'POST':
        if account_form.is_valid():
            account_form.save()
            success = True
            return redirect(reverse('charges:accounts') + '?success=True')
        else:
            success = False

    context = {
        'success': success,
        'account_form': account_form,
        'title': 'Edit Account',
        'account': acc,
    }
    return render(request, 'finance/edit_account.html', context)


@login_required
def accounts(request):
    accs = Account.objects.filter(owner=request.user)
    success = request.GET.get('success', None)

    paginator = Paginator(accs, 10,  orphans=10)
    page = request.GET.get('page')
    try:
        accounts = paginator.page(page)
    except PageNotAnInteger:
        accounts = paginator.page(1)
    except EmptyPage:
        accounts = paginator.page(paginator.num_pages)

    context = {
        'accounts': accounts,
        'success': success,
    }

    return render(request, 'finance/accounts.html', context)


@login_required
@csrf_exempt
def create_account(request):
    account_form = None
    success = None

    if request.method == 'POST':
        account_form = AccountForm(request.POST)
        if account_form.is_valid():
            account = account_form.save(commit=False)
            account.owner = request.user
            account.save()
            success = True
            return redirect(reverse('charges:accounts') + '?success=True')
    elif request.method == 'GET':
        account_form = AccountForm()
        success = False

    context = {
        'success': success,
        'account_form': account_form,
    }

    return render(request, 'finance/create_account.html', context)


def get_hist_data(charges):
    end_date = datetime.today()
    m = end_date.month
    start_date = end_date - relativedelta(months=12, days=end_date.day - 1)

    latest_year_charges = charges.filter(date__range=[start_date, end_date])
    agg_data = latest_year_charges.annotate(month=Month('date')).values(
        'month').annotate(total=Sum('value')).order_by('month')

    getcontext().prec = 3

    hist_values = [[month_abbr[(i + m - 1) % 12 + 1], 0.0]
                   for i in range(1, 13)]

    for rec in agg_data:
        hist_values[(rec['month'] + m - 1) % 12][1] = float(rec['total'])
    hist_header = [['Month', 'Total']]
    hist_data = hist_header + hist_values
    hist_json = json.dumps(hist_data)
    return hist_json


@require_GET
@isOwnerOrAdmin
@login_required
def account(request, account_id):
    success = request.GET.get('success', None)

    charges = Charge.objects.filter(account=account_id)

    hist_json = get_hist_data(charges)

    paginator = Paginator(charges, 10, orphans=10)
    page = request.GET.get('page')
    try:
        charges = paginator.page(page)
    except PageNotAnInteger:
        charges = paginator.page(1)
    except EmptyPage:
        charges = paginator.page(paginator.num_pages)

    context = {
        'account': Account.objects.get(id=account_id),
        'charges': charges,
        'hist_data': hist_json,
        'success': success
    }

    return render(request, 'finance/account.html', context)


@isOwnerOrAdmin
@login_required
def create_charge(request, account_id):
    charge_form = None
    success = None
    account = Account.objects.get(id=account_id)
    if request.method == 'POST':
        charge_form = ChargeForm(request.POST)
        if charge_form.is_valid():
            charge = charge_form.save(commit=False)
            charge.account = account
            charge.save()
            success = True
            return redirect(reverse('charges:account', kwargs={'account_id': account_id}) + '?success=True')
        else:
            success = False
    elif request.method == 'GET':
        charge_form = ChargeForm()

    context = {
        'account': account,
        'success': success,
        'charge_form': charge_form,
    }
    return render(request, 'finance/create_charge.html', context)
