from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.messages import error
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods

from finance.forms import AccountForm, ChargeForm, LoginForm, RegisterForm, ProfileForm
from finance.models import Account, Charge
from finance.random_transactions import random_transactions


def check_owner(f):

    @login_required
    def wrapper(request, account_id, *args, **kwargs):
        if Account.objects.get(id=account_id).owner != request.user:
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
            error(request, 'Wrong credentials!')

    context = {
        'login_form': login_form,
        'next': next_url,
    }

    return render(request, 'finance/login.html', context=context)


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
            if not user:
                error(request, 'Wrong credentials!')
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
def profile(request):
    profile_form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user)
    success = None

    if request.method == "POST":
        if profile_form.is_valid():
            profile_form.save()
            success = True
        else:
            success = False

    context = {
        'profile_form': profile_form,
        'success': success
    }
    return render(request, 'finance/profile.html', context=context)

@login_required
@check_owner
def view_amount(request, account_id):
    total = Account.objects.get(id=account_id).total
    context = {
        'total': total,
    }
    return render(request, 'finance/view_account_total.html', context=context)


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
    elif request.method == 'GET':
        account_form = AccountForm()
        success = False

    context = {
        'success': success,
        'account_form': account_form,
    }

    return render(request, 'finance/create_account.html', context)


@login_required
def accounts(request):
    context = {
        'accounts': Account.objects.all()
    }
    return render(request, 'finance/accounts.html', context)


@login_required
def account(request, account_id):
    context = {
        'account': Account.objects.get(id=account_id),
        'charges': Charge.objects.filter(account=account_id),
    }
    return render(request, 'finance/account.html', context)


@login_required
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
            charge = charge.save()
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
