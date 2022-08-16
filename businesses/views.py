from django.conf import settings as django_settings
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Business
from atm_functions.models import Balance, DigitalCurrency, DynamicUsername

from decimal import Decimal

# Create your views here.


@login_required()
def businesses(request):
    businesses = Business.objects.all()

    context = {
            'businesses': businesses
            }
            
    return render(request, 'businesses/businesses.html', context)

@login_required()
def create_business(request):

    if request.method == "GET":
        return render(request, 'businesses/create_business.html')

    if request.method == "POST":
        business_official_name = request.POST.get("business_name", None)
        business_username = request.POST.get("business_username", None).lower().replace(" ", "")
        business_system_name = business_official_name.lower()
        business_category = request.POST.get("business_category", None)
        business_price = 50      #PRICE IN CRYPTOSHARE CREDITS

        business_username = business_username.replace(" ", "")

        if DynamicUsername.objects.filter(id_username=business_username).exists():
            messages.warning(request, "Username already exists.")

            return redirect('businesses:Create')

        name_exists = Business.objects.filter(system_name=business_system_name)
        if name_exists:
            messages.info(request, "Business name already exists.")
            return redirect('businesses:Create')

        digital_currency_object = DigitalCurrency.objects.get(symbol="CSC")
        user_balance = Balance.objects.get(email = request.user, digital_currency_name = digital_currency_object)

        if user_balance.amount < business_price:
            messages.info(request, "You do not have enough funds to create a business. Please buy more CryptoShare Credits.")
            return redirect('atm_functions:Home')
        
        user_balance.amount -= Decimal(business_price)
        user_balance.save()

        new_business = Business(owner=request.user, official_name=business_official_name, system_name=business_system_name, category=business_category)
        new_business.save()

        new_username = DynamicUsername.objects.create(
            id_username = business_username,
            username_type = "BUSINESS",
            business_reference = new_business
        )

        messages.info(request, "Business created successfully.")
        return redirect('businesses:Businesses')

@login_required()
def edit_business(request):

    business_id = request.GET.get("id", None)

    if not business_id:
        return redirect('businesses:Manage')

    if request.method == "GET":
        business = Business.objects.get(id_business=business_id)

        context = {
            'business': business
        }

        return render(request, 'businesses/edit_businesses.html', context)

    return render(request, 'businesses/edit_businesses.html')


@login_required()
def manage_businesses(request):
    businesses = Business.objects.filter(owner=request.user)

    context = {
        "businesses": businesses
    }

    return render(request, 'businesses/manage_businesses.html', context)

@login_required()
def search_business(request):

    if request.method == "GET":
        businesses = Business.objects.all()

    if request.method == "POST":                
        search_option = request.POST.get("SearchOption", None)
        search_value = request.POST.get("SearchValue", None)

        if search_option == "StartsWith":
            businesses = Business.objects.filter(system_name__startswith=search_value.lower())

        elif search_option == "Contains":
            businesses = Business.objects.filter(system_name__contains=search_value.lower())

        elif search_option == "ExactMatch":
            businesses = Business.objects.filter(system_name=search_value.lower())

    context = {
        "businesses": businesses
    }

    return render(request, 'businesses/search_businesses.html', context)

def test(request):
    raise Http404()