from django.conf import settings as django_settings
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Business
from atm_functions.models import Balance, DigitalCurrency, DynamicUsername
from marketplace.models import Product, DigitalService, PurchaseHistory

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
def manage_sales(request, id_business):

    context = {}

    business = Business.objects.get(
        id_business = id_business
        )

    business_sales = PurchaseHistory.objects.filter(
        product__business = business
        )

    context["business"] = business
    context["business_sales"] = business_sales

    return render(request, 'businesses/sales/manage_sales.html', context)

    pass

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

    if not Business.objects.filter(id_business=business_id).exists():
        return redirect('businesses:Manage')

    business = Business.objects.get(id_business=business_id)

    if request.method == "GET":

        if business.system_name:
            business.system_name = business.system_name.replace(" ", "-")

        context = {
            'business': business
        }

        return render(request, 'businesses/edit_businesses.html', context)
    
    if request.method == "POST":
        
        business_id = int(request.POST.get("business_id", None))
        business_category = request.POST.get("business_category", None)
        business_logo_url = request.POST.get("business_logo", None)

        business = Business.objects.get(id_business=business_id)
        business.category = business_category
        business.logo_url = business_logo_url
        business.save()

        messages.info(request, "Business updated successfully.")
        return redirect('businesses:Manage')

    return render(request, 'businesses/edit_businesses.html')


@login_required()
def manage_businesses(request):
    businesses = Business.objects.filter(owner=request.user)

    context = {
        "businesses": businesses
    }

    return render(request, 'businesses/manage_businesses.html', context)

@login_required()
def manage_business(request, id_business = None):

    if not Business.objects.filter(id_business = id_business, owner = request.user).exists():
        raise Http404()

    context = {}

    business = Business.objects.get(id_business = id_business)

    context["business"] = business

    return render(request, 'businesses/manage_business.html', context)

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


@login_required()
def create_product(request, id_business = None):

    if not Business.objects.filter(id_business = id_business, owner = request.user).exists():
        raise Http404()

    context = {}

    business = Business.objects.get(id_business = id_business)

    if request.method == "GET":

        context["business"] = business

        return render(request, 'businesses/products/create_product.html', context)

    elif request.method == "POST":                  
        product_name = request.POST.get("product_name", None)
        product_photo_url = request.POST.get("product_photo", None)
        product_price = request.POST.get("product_price", None)
        product_description = request.POST.get("product_description", None)
        product_extra = request.POST.get("product_extra", None)

        if business.system_category == "DIGITAL_SERVICES":

            product_video_url = request.POST.get("product_video", None)
            product_calendar_url = request.POST.get("product_calendar", None)

            new_digital_service = DigitalService.objects.create(
                name = product_name,
                price = product_price,
                photo_url = product_photo_url,
                description = product_description,
                video_url = product_video_url,
                calendar_url = product_calendar_url,
                extra_url = product_extra
            )

            new_product = Product.objects.create(
                business = business,
                category = business.system_category,
                digital_service_reference = new_digital_service
            )
        
        messages.success(request, "Product created successfully.")

        return redirect('businesses:ManageBusiness', id_business=business.id_business)

@login_required()
def delete_product(request, id_business = None, id_product = None):
    if not Product.objects.filter(id_product = id_product, business__owner = request.user).exists():
        messages.error(request, "You can't do that!", extra_tags='danger')

        return redirect('businesses:ManageProduct')


    product = Product.objects.get(id_product = id_product, business__owner = request.user)

    if product.category == "DIGITAL_SERVICES":
        inner_product = product.digital_service_reference

    product.delete()

    messages.success(request, "Product deleted successfully.")

    return redirect('businesses:ManageProduct', id_business=id_business)

@login_required()
def manage_products(request, id_business = None):
    if not Business.objects.filter(id_business = id_business, owner = request.user).exists():
        raise Http404()

    context = {}

    business = Business.objects.get(id_business = id_business)

    if request.method == "GET":

        products = Product.objects.filter(business = business)

    context["business"] = business
    context["products"] = products

    return render(request, 'businesses/products/manage_products.html', context)

def test(request):
    raise Http404()