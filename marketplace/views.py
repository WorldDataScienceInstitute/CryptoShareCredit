from multiprocessing import context
from django.conf import settings as django_settings
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import Http404

from businesses.models import Business
from atm_functions.models import Balance, DigitalCurrency, DynamicUsername, Notification
from common.emails import sale_owner_notification
from .models import Product, PurchaseHistory

from decimal import Decimal

@login_required()
def marketplace(request):
    context = {}

    products = Product.objects.all().select_related("digital_service_reference")

    # for p in products: print(p.__dict__)

    context["products"] = products

    return render(request, 'marketplace/marketplace.html', context)

@login_required()
def product_info(request, id_product = None):
    context = {}

    if not Product.objects.filter(id_product = id_product).exists():
        raise Http404()

    product_info = Product.objects.get(id_product = id_product)
    product_info.object_reference = None

    # <-------------------- THIS NEEDS TO BE IN A UTILITY FUNCTION -------------------->
    # <-------------------- THIS NEEDS TO BE IN A UTILITY FUNCTION -------------------->
    # <-------------------- THIS NEEDS TO BE IN A UTILITY FUNCTION -------------------->
    if product_info.category == "CONSULTATIONS":
        # product_info.object_reference = product_info.consultations_reference
        product_info.object_reference = product_info.digital_service_reference #Missing to create consultations object

    elif product_info.category == "DIGITAL_SERVICES":
        product_info.object_reference = product_info.digital_service_reference

    # <-------------------- THIS NEEDS TO BE IN A UTILITY FUNCTION -------------------->
    # <-------------------- THIS NEEDS TO BE IN A UTILITY FUNCTION -------------------->
    # <-------------------- THIS NEEDS TO BE IN A UTILITY FUNCTION -------------------->

    context["product"] = product_info
    return render(request, 'marketplace/product_info.html', context)

@login_required()
def buy_product(request, id_product = None):
    if not Product.objects.filter(id_product = id_product).exists():
        raise Http404()

    if request.method == "GET":
        return redirect('marketplace:ProductInfo', id_product = id_product)

    context = {}
    
    product = Product.objects.get(id_product = id_product)

    if product.business.owner == request.user:
        messages.error(request, "You can't buy your own products", extra_tags='danger')
        return redirect('marketplace:ProductInfo', id_product = id_product)

    # <-------------------- THIS NEEDS TO BE IN A UTILITY FUNCTION -------------------->
    # <-------------------- THIS NEEDS TO BE IN A UTILITY FUNCTION -------------------->
    # <-------------------- THIS NEEDS TO BE IN A UTILITY FUNCTION -------------------->
    if product.category == "CONSULTATIONS":
        # product_info.object_reference = product_info.consultations_reference
        product.object_reference = product.digital_service_reference #Missing to create consultations object

    elif product.category == "DIGITAL_SERVICES":
        product.object_reference = product.digital_service_reference

    # <-------------------- THIS NEEDS TO BE IN A UTILITY FUNCTION -------------------->
    # <-------------------- THIS NEEDS TO BE IN A UTILITY FUNCTION -------------------->
    # <-------------------- THIS NEEDS TO BE IN A UTILITY FUNCTION -------------------->

    product_price = product.object_reference.price

    user_object = request.user
    cryptoshare_credits_object = DigitalCurrency.objects.get(symbol="CSC")

    user_balance = Balance.objects.get(email = user_object, digital_currency_name = cryptoshare_credits_object)

    if user_balance.amount < product_price:
        messages.error(request, "You don't have enough CSC to buy this product.", extra_tags='danger')
        return redirect('marketplace:ProductInfo', id_product = id_product)
    
    user_balance.amount -= Decimal(product_price)
    user_balance.save()

    if product.category == "DIGITAL_SERVICES":
        purchase_state = "PENDING"
        success_message = "You have successfully bought this digital service, the seller will contact you soon."
    elif product.category == "CONSULTATIONS":
        purchase_state = "PENDING"
        success_message = "You have successfully bought this consultation, the seller will contact you soon."

    else:
        purchase_state = "COMPLETED"
        success_message = "You have successfully bought this product."

    purchase_registry = PurchaseHistory.objects.create(
        product = product,
        user = user_object,
        state = purchase_state,
        paid_price = product_price
    )

    # sale_owner_notification(sender_email, business_name, id_business, id_product, date, client_email)
    sale_owner_notification(
        sender_email = str(product.business.owner),
        business_name = product.business.official_name,
        id_business = product.business.id_business,
        id_product = product.id_product,
        date = purchase_registry.creation_datetime,
        client_email = str(user_object)
    )

    Notification.objects.create(
                user = product.business.owner,
                notification_lob = "BUSINESS",
                notification_type = "SALE",
                notification_state = "PENDING",
                description = f"You just got sold a product / service from your {product.business.official_name} business."
            )

    messages.success(request, success_message)
    return redirect('marketplace:PurchaseHistory')

@login_required()
def purchases_history(request):

    context = {}

    purchases_history = PurchaseHistory.objects.filter(user = request.user)
    context["purchases_history"] = purchases_history

    return render(request, 'marketplace/purchase_history.html', context)

    pass