from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt


from finance.forms import ChargeForm
from finance.models import Charge
from finance.random_transactions import random_transactions


def homepage(request):
    return render(request, 'finance/index.html')


def charges(request):
    charges_in = []
    charges_off = []
    for charge in Charge.objects.all():
        if charge.value > 0:
            charges_in.append(charge)
        else:
            charges_off.append(charge)

    context = {
        'charges_in': charges_in,
        'charges_off': charges_off
    }
    return render(request, 'finance/charges.html', context)


@csrf_exempt
def create_charge(request):
    charge_form = None
    success = None

    if request.method == 'POST':
        charge_form = ChargeForm(request.POST)
        if charge_form.is_valid():
            charge = charge_form.save()
            success = True

    if request.method == 'GET':
        charge_form = ChargeForm()
        success = False

    context = {
        'success': success,
        'charge_form': charge_form,
    }
    return render(request, 'finance/create_charge.html', context)
