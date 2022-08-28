from multiprocessing import context
from django.conf import settings as django_settings
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import Http404

from businesses.models import Business
from atm_functions.models import Balance, DigitalCurrency, DynamicUsername
from .models import Product

from decimal import Decimal

def marketplace(request):
    context = {}

    products = Product.objects.all().select_related("digital_service_reference")

    print(products)

    for p in products: print(p.__dict__)

    context["products"] = products

    return render(request, 'marketplace/marketplace.html', context)

def product_info(request, id_product = None):
    context = {}

    if not Product.objects.filter(id_product = id_product).exists():
        raise Http404()

    product_info = Product.objects.get(id_product = id_product)
    product_info.object_reference = None

    if product_info.category == "CONSULTATIONS":
        # product_info.object_reference = product_info.consultations_reference
        product_info.object_reference = product_info.digital_service_reference

    elif product_info.category == "DIGITAL_SERVICE":
        product_info.object_reference = product_info.digital_service_reference


    context["product"] = product_info
    return render(request, 'marketplace/product_info.html', context)