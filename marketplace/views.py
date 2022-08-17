from django.conf import settings as django_settings
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import Http404

from businesses.models import Business
from atm_functions.models import Balance, DigitalCurrency, DynamicUsername

from decimal import Decimal

def test(request):
    return redirect('atm_functions:Home')