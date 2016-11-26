from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt


from finance.forms import ChargeForm, AccountForm
from finance.models import Charge, Account
from finance.random_transactions import random_transactions


def homepage(request):
    return render(request, 'finance/index.html')


@csrf_exempt
def create_account(request):
    account_form = None
    success = None

    if request.method == 'POST':
        account_form = AccountForm(request.POST)
        if account_form.is_valid():
            account = account_form.save()
            success = True
    elif request.method == 'GET':
        account_form = AccountForm()
        success = False

    context = {
        'success': success,
        'account_form': account_form,
    }

    return render(request, 'finance/create_account.html', context)


def accounts(request):
    context = {
        'accounts': Account.objects.all()
    }
    return render(request, 'finance/accounts.html', context)

def account(request, account_id):
    context= {
        'account': Account.objects.get(id=account_id),
        'charges': Charge.objects.filter(account=account_id),
    }
    return render(request, 'finance/account.html', context)

@csrf_exempt
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

    elif request.method == 'GET':
        charge_form = ChargeForm()
        success = False

    context = {
        'account': account,
        'success': success,
        'charge_form': charge_form,
    }
    return render(request, 'finance/create_charge.html', context)
