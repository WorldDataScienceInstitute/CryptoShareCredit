# from time import timezone
from django.conf import settings as django_settings
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, FileResponse, Http404
from django.utils import timezone
from django.db.models import Q
from django.templatetags.static import static
from django.utils import formats
from .models import User
from decimal import Decimal
from atm_functions.models import Account, Address, Balance, Cryptocurrency, DigitalCurrency, BlockchainWill, Beneficiary, TransactionA, TransactionB, WaitingList, UserAssets, StripeAccount, TransactionStripe, DynamicUsername, TransactionCredits, Contact
from businesses.models import Business
# from common.utils import currency_list
from common.utils import get_currencies_exchange_rate, calculate_credit_grade, swap_crypto_info, countries_tuples, FIAT_CURRENCIES
from common.emails import sent_funds_email, sent_funds_cryptoshare_wallet_email, deposit_funds_email, revoked_address_email, expired_transactionb_email, inprogress_transactionb_email, test_email, payment_request
from common.cryptoapis import CryptoApis
from common.cryptoapis_utils import CryptoApisUtils
from common.simpleswap import SimpleSwap
# from common.aptopayments import AptoPayments
from google_currency import convert
from coinbase.wallet.client import OAuthClient
from coinbase.wallet.error import TwoFactorRequiredError
import hashlib
import stripe
import os

import requests
import json

import cv2
from PIL import Image

def home(request):
    if not request.user.is_authenticated:
        next_url = request.GET.get('next', "atm_functions:Home")
        context = { "next_url": next_url }
        return render(request, 'atm_login.html', context)
        # return render(request, "buy_blockchain_credit_lines.html")


    return redirect('atm_functions:CheckCredit')

@login_required()
def profile(request):
    user = Account.objects.get(user = request.user)
    countries = countries_tuples

    if request.method == "GET":
        
        usernames = []

        if DynamicUsername.objects.filter(business_reference__owner = request.user).exists():
            usernames = DynamicUsername.objects.filter(business_reference__owner = request.user)

        context = {
            "user": user,
            "countries": countries,
            "usernames": usernames
        }
        return render(request, "atm_user_profile.html", context)
    
    elif request.method == "POST":
        action = request.GET.get('action','')

        if action == "BuyUsername":
            USERNAME_PRICE = 10

            cryptoshare_credits_object = DigitalCurrency.objects.get(symbol="CSC")

            user_balance = Balance.objects.get(email=request.user, digital_currency_name=cryptoshare_credits_object)

            if user_balance.amount < USERNAME_PRICE:
                messages.warning(request, "You need at least 10 CryptoShare Credits to buy a username")
                return redirect("atm_functions:Profile")

            new_username = request.POST.get('newUsername','').lower().replace(" ", "")

            if DynamicUsername.objects.filter(id_username = new_username).exists():
                messages.warning(request, "Username already exists")
                return redirect("atm_functions:Profile")
            
            previous_username = DynamicUsername.objects.get(user_reference = request.user, username_type = "USER")
            previous_username.delete()

            previous_username.id_username = new_username
            previous_username.save()

            user.system_username = new_username
            user.save()

            user_balance.amount -= Decimal(USERNAME_PRICE)
            user_balance.save()

            messages.success(request, "Username changed successfully")
            return redirect('atm_functions:Profile')
        
        elif action == "UpdateProfileInfo":
            new_first_name = request.POST.get('first_name','')
            new_last_name = request.POST.get('last_name','')
            new_country = request.POST.get('country','')
            new_birthdate = request.POST.get('birthdate','')

            user.first_name = new_first_name
            user.last_name = new_last_name
            user.country = new_country
            user.birthdate = new_birthdate

            if new_country == "US":
                state = request.POST.get('state','')
                user.state = state

            user.save()

            messages.success(request, "Profile information updated successfully")
            return redirect('atm_functions:Profile')    
        
@login_required()
def contacts(request):
    contacts = Contact.objects.filter(
        user = request.user
        )

    context = {
        "contacts": contacts
    }

    return render(request, "atm_functions/contacts/contacts.html", context)

@login_required()
def create_contact(request):
    
    if request.method == "GET":
        return render(request, "atm_functions/contacts/create_contact.html")

    if request.method == "POST":
        contact_name = request.POST.get('contact_name','')
        contact_username = request.POST.get('contact_username','').lower().replace(" ", "")

        if Contact.objects.filter(user = request.user, username = contact_username).exists():
            messages.warning(request, "Contact with that username already exists")
            return redirect("atm_functions:Contacts")
        
        if not DynamicUsername.objects.filter(id_username = contact_username, username_type = "USER").exists():
            messages.warning(request, "Invalid username, please try a different one")
            return redirect("atm_functions:Contacts")
        
        new_contact_user = DynamicUsername.objects.get(id_username = contact_username, username_type = "USER").user_reference
        Contact.objects.create(
            user = request.user,
            name = contact_name,
            username = contact_username,
            user_reference = new_contact_user
        )

        messages.success(request, "Contact created successfully")
        return redirect("atm_functions:Contacts")

    return render(request, "atm_functions/contacts/create_contact.html")

@login_required()
def delete_contact(request):
    if request.method == "GET":
        return redirect("atm_functions:Contacts")

    contact_id = request.GET.get('id','')

    if not Contact.objects.filter(id = contact_id).exists():
        messages.success(request, "An error occurred, please try again")

        return redirect("atm_functions:Contacts")
    
    contact = Contact.objects.get(id = contact_id)
    contact.delete()
    
    return redirect("atm_functions:Contacts")


# @login_required(login_url='authentication:Login')
@login_required()
def credit_grades(request):
    context = {}

    return render(request, 'credit_grades.html', context)

@login_required()
def check_balance(request):

    u = User.objects.get(
        pk = request.user.pk
        )
    # get first name
    name = u.first_name

    digital_balances = Balance.objects.filter(email=request.user, currency_type="DIGITAL").select_related("digital_currency_name")

    excluding_currencies = ["TEST_COIN","ethereum_ropsten"]
    available_crypto_currencies = Cryptocurrency.objects.all().exclude(currency_name__in=excluding_currencies).values()
    crypto_addresses = Address.objects.filter(email=request.user).exclude(currency_name__in=excluding_currencies).select_related("currency_name")
    crypto_balances = Balance.objects.filter(email=request.user, currency_type="CRYPTO").exclude(currency_name__in=excluding_currencies).select_related("currency_name")

    # currencies = {currency["symbol"]: currency for currency in available_currencies}
    crypto_currencies = {}
    for currency in available_crypto_currencies:
        crypto_currencies[currency["symbol"]] = currency
        crypto_currencies[currency["symbol"]]["has_address"] = False
        crypto_currencies[currency["symbol"]]["balance"] = 0
        crypto_currencies[currency["symbol"]]["address"] = ""


    for address in crypto_addresses:
        crypto_currencies[address.currency_name.symbol]["has_address"] = True
        crypto_currencies[address.currency_name.symbol]["address"] = address.address

    for balance in crypto_balances:
        crypto_currencies[balance.currency_name.symbol]["balance"] = balance.amount

    # savings_currencies = []
    payments_currencies = []
    erc20_tokens = []
    static_currencies = {}

    for currency in crypto_currencies.values():
        if currency["blockchain"] == "ethereum" and currency["symbol"] != "ETH":
            currency["has_address"] = True
            currency["address"] = crypto_currencies["ETH"]["address"]
            # currency["currency_name"] += " (ERC-20)"

            erc20_tokens.append(currency)

        # if currency["currency_type"] == "SAVINGS":
        #     savings_currencies.append(currency)
        if currency["currency_type"] == "PAYMENTS":
            payments_currencies.append(currency)

        if currency["currency_name"] == "Bitcoin":
            static_currencies["BTC"] = currency
        elif currency["currency_name"] == "Ethereum":
            static_currencies["ETH"] = currency

    context = {
        "name": name,
        "digital_balances": digital_balances,
        # "savings_currencies": savings_currencies,
        "payments_currencies": payments_currencies,
        "erc20_tokens": erc20_tokens,
        "static_currencies": static_currencies
    }

    return render(request, 'check_balance.html', context)

@login_required()
def cryptoshare_wallet(request):
    if not request.user.is_authenticated:
        return redirect('authentication:Home')

    context = {
        "address_confirmations": [
                                {
                                    "currency_name": "Litecoin",
                                    "blockchain": "litecoin",
                                    "symbol": "LTC",
                                    "type": "PAYMENTS",
                                    "has_address": False
                                },
                                {
                                    "currency_name": "Bitcoin Cash",
                                    "blockchain": "bitcoin-cash",
                                    "symbol": "BCH",
                                    "type": "PAYMENTS",
                                    "has_address": False
                                },
                                {
                                    "currency_name": "Dash",
                                    "blockchain": "dash",
                                    "symbol": "DASH",
                                    "type": "PAYMENTS",
                                    "has_address": False
                                },
                                {
                                    "currency_name": "Zcash",
                                    "blockchain": "zcash",
                                    "symbol": "ZEC",
                                    "type": "PAYMENTS",
                                    "has_address": False
                                },
                                {
                                    "currency_name": "XRP",
                                    "blockchain": "xrp",
                                    "symbol": "XRP",
                                    "type": "PAYMENTS",
                                    "has_address": False
                                },
                                {
                                    "currency_name": "Bitcoin",
                                    "blockchain": "bitcoin",
                                    "symbol": "BTC",
                                    "type": "SAVINGS",
                                    "has_address": False
                                },
                                {
                                    "currency_name": "Dogecoin",
                                    "blockchain": "dogecoin",
                                    "symbol": "DOGE",
                                    "type": "PAYMENTS",
                                    "has_address": False
                                },
                                {
                                    "currency_name": "Ethereum",
                                    "blockchain": "ethereum",
                                    "symbol": "ETH",
                                    "type": "SAVINGS",
                                    "has_address": False
                                }
                                ],
        "savings_addresses": [],
        "payments_addresses": []
    }

    currencies_addresses = Address.objects.filter(email=request.user).select_related("currency_name")

    for address in currencies_addresses:
        #Changing address blockchain for displaying in frontend
        if address.currency_name.currency_name == "Litecoin":
            context["address_confirmations"][0]["has_address"] = True

        elif address.currency_name.currency_name == "Bitcoin Cash":
            context["address_confirmations"][1]["has_address"] = True

        elif address.currency_name.currency_name == "Dash":
            context["address_confirmations"][2]["has_address"] = True
        
        elif address.currency_name.currency_name == "Zcash":
            context["address_confirmations"][3]["has_address"] = True
        
        elif address.currency_name.currency_name == "XRP":
            context["address_confirmations"][4]["has_address"] = True

        elif address.currency_name.currency_name == "Bitcoin":
            context["address_confirmations"][5]["has_address"] = True

        elif address.currency_name.currency_name == "Dogecoin":
            context["address_confirmations"][6]["has_address"] = True

        elif address.currency_name.currency_name == "Ethereum":
            context["address_confirmations"][7]["has_address"] = True

        if address.currency_name.currency_type == "SAVINGS":
            context["savings_addresses"].append(address)
        elif address.currency_name.currency_type == "PAYMENTS":
            context["payments_addresses"].append(address)

    # context["addresses"] = currencies_addresses

    return render(request, 'cryptoshare_wallet.html', context)

@login_required()
def buy_crypto(request):

    context = {
    }

    return render(request, 'buy_crypto.html', context)

@login_required()
def buy_crypto_widget(request):
    addresses_objects = Address.objects.filter(email=request.user)
    erc20_objects = Cryptocurrency.objects.filter(blockchain="ethereum")

    API_KEY = os.environ['ONRAMPER_PRODUCTION_KEY']
    if addresses_objects.count() != 0:
        available_cryptos = []
    else:
        available_cryptos = ["BTC", "LTC", "BCH", "DASH", "XRP", "ZEC", "DOGE", "ETH", "USDC", "USDT", "WBTC"]

    addresses = {
                "BTC": "",
                "LTC": "",
                "BCH": "",
                "DASH": "",
                "XRP": "",
                "ZEC": "",
                "DOGE": "",
                "ETH": "",
                "USDC": "",
                "USDT": "",
                "WBTC": "",
                }
    
    for address in addresses_objects:
        if address.currency_name.symbol in addresses:
            available_cryptos.append(address.currency_name.symbol)
            addresses[address.currency_name.symbol] = address.address

    if addresses["ETH"] != "":
        for currency in erc20_objects:
            if currency.symbol in addresses:
                available_cryptos.append(currency.symbol)
                addresses[currency.symbol] = addresses["ETH"]

    context = {
            "available_cryptos": available_cryptos,
            "addresses": addresses,
            "API_KEY": API_KEY
            }

    return render(request, 'buy_crypto_widget.html', context)

@login_required()
def stripe_checkout(request):
    products = {
        "CSC_50": "price_1LTEObD9Xw88IvYZXih30PQ7",
        "CSC_100": "price_1LTEObD9Xw88IvYZ2ZEXtNv4",
        "CSC_600": "price_1LTEObD9Xw88IvYZohyrJAv0",
        "CSC_10-000": "price_1LTEObD9Xw88IvYZFlsOuvUG",
        "CSC_60-000": "price_1LTEObD9Xw88IvYZKII7Utwo",
        "CSC_100-000": "price_1LTEObD9Xw88IvYZUJulNN0V",
        "CSC_600-000": "price_1LTEObD9Xw88IvYZKwCFMtpu",
    }

    products_amount = {
        "CSC_50": 50,
        "CSC_100": 100,
        "CSC_600": 600,
        "CSC_10-000": 10000,
        "CSC_60-000": 60000,
        "CSC_100-000": 100000,
        "CSC_600-000": 600000,
    }

    test_products = {
        "CSC_50": "price_1LR4IbD9Xw88IvYZrogp5Vrf",
        "CSC_100": "price_1LTEVdD9Xw88IvYZluunChSz",
        "CSC_600": "price_1LTEXMD9Xw88IvYZoCJMup5S",
        "CSC_10-000": "price_1LTHXzD9Xw88IvYZWxIqfrZc",
        "CSC_60-000": "price_1LTHYUD9Xw88IvYZkbhaPeOU",
        "CSC_100-000": "price_1LTHYID9Xw88IvYZNbrEnHnq",
        "CSC_600-000": "price_1LTHYmD9Xw88IvYZ2R1QiPkt",
    }

    selected_product = request.GET.get('product','')

    if selected_product in products:
        product = products[selected_product]
        amount = products_amount[selected_product]
    else:
        messages.error(request, "Invalid product, please try again.", extra_tags='danger')
        return redirect("atm_functions:BuyCredit")

    user_stripe_account = StripeAccount.objects.get(user=request.user)
    customer_id = user_stripe_account.stripe_customer_id
    # customer_id = "cus_MBbhOsQob9vTIp"

    stripe.api_key = os.environ['STRIPE_SECRET_KEY']


    session = stripe.checkout.Session.create(
        success_url = "https://cryptoshareapp.com/atm/StripeCheckoutResult/?result=success&product=" + selected_product,
        cancel_url = "https://cryptoshareapp.com/atm/StripeCheckoutResult/?result=cancel&product=" + selected_product,
        line_items = [
            {
            "price": product,
            "quantity": 1,
            },
        ],
        mode = "payment",
        customer = customer_id
    )

    payment_intent = session.payment_intent

    stripe_transaction = TransactionStripe.objects.create(
        stripe_account = user_stripe_account,
        payment_intent = payment_intent,
        amount = amount,
        transaction_type = "BUY",
        transaction_type_internal = "payment_intent.processing",
        transaction_state = "IN PROGRESS")

    return redirect(session.url)

def stripe_checkout_result(request):
    result = request.GET.get('result','')
    product = request.GET.get('product','')

    products_amount = {
        "CSC_50": 50,
        "CSC_100": 100,
        "CSC_600": 600,
        "CSC_10-000": 10000,
        "CSC_60-000": 60000,
        "CSC_100-000": 100000,
        "CSC_600-000": 600000,
    }

    if result == "success":
        messages.success(request, f"Processing payment of {products_amount[product]} CryptoShare Credits", extra_tags='success')
        return redirect("atm_functions:Home")
    elif result == "cancel":
        messages.error(request, "Payment cancelled!", extra_tags='danger')
        return redirect("atm_functions:Home")
    else:
        return redirect("atm_functions:Home")



@login_required
def estate_net_worth(request):

    if request.method == "GET":
        user_data = Account.objects.get(user=request.user)

        context = {
            "net_worth": user_data.net_worth
        }

        return render(request, 'estate_net_worth.html', context)


    return render(request, 'estate_net_worth.html')

@login_required
def edit_estate_net_worth(request):
    def update_asset(asset_id, asset_name, asset_worth, asset_extrafield = None):
        asset = UserAssets.objects.get(pk=asset_id)
        asset.name = asset_name
        asset.worth = asset_worth

        if asset_extrafield is not None:
            asset.extra_field = asset_extrafield
        
        asset.save()

    if request.method == "GET":

        bank = UserAssets.objects.filter(email=request.user, type="BANK")
        real_estate = UserAssets.objects.filter(email=request.user, type="REAL_ESTATE")
        insurance = UserAssets.objects.filter(email=request.user, type="INSURANCE")
        cryptocurrency = UserAssets.objects.filter(email=request.user, type="CRYPTOCURRENCY")
        nft = UserAssets.objects.filter(email=request.user, type="NFT")
        stock = UserAssets.objects.filter(email=request.user, type="STOCK")
        startup = UserAssets.objects.filter(email=request.user, type="STARTUP_INVESTMENT")
        jewelry = UserAssets.objects.filter(email=request.user, type="JEWELRY")
        car = UserAssets.objects.filter(email=request.user, type="CAR")
        #net worth information
        user_data = Account.objects.get(user=request.user)

        context = {
            "banks": bank,
            "real_estates": real_estate,
            "insurances": insurance,
            "cryptocurrencies": cryptocurrency,
            "nfts": nft,
            "stocks": stock,
            "startups": startup,
            "jewelries": jewelry,
            "cars": car,
            "currencies":FIAT_CURRENCIES,
            "net_worth": user_data.net_worth
        }

        return render(request, 'estate_net_worth_edit.html', context)        

    bank_ids = request.POST.getlist("asset_bank_id")
    bank_names = request.POST.getlist("asset_bank", None)
    bank_worths = request.POST.getlist("asset_bank-worth", None)

    real_estate_ids = request.POST.getlist("asset_real_estate_id")
    real_estate_names = request.POST.getlist("asset_real-estate", None)
    real_estate_worths = request.POST.getlist("asset_real-estate-worth", None)

    insurance_ids = request.POST.getlist("asset_insurance_id")
    insurance_names = request.POST.getlist("asset_insurance", None)
    insurance_worths = request.POST.getlist("asset_insurance-worth", None)

    cryptocurrency_ids = request.POST.getlist("asset_cryptocurrency_id")
    cryptocurrency_names = request.POST.getlist("asset_cryptocurrency", None)
    cryptocurrency_worths = request.POST.getlist("asset_cryptocurrency-worth", None)

    nft_ids = request.POST.getlist("asset_nft_id")
    nft_names = request.POST.getlist("asset_nft", None)
    nft_worths = request.POST.getlist("asset_nft-worth", None)

    stock_ids = request.POST.getlist("asset_stock_id")
    stock_names = request.POST.getlist("asset_stock", None)
    stock_worths = request.POST.getlist("asset_stock-worth", None)
    stock_extrafield = request.POST.getlist("asset_stock-extradata", None)

    startup_ids = request.POST.getlist("asset_startup_id")
    startup_names = request.POST.getlist("asset_startup", None)
    startup_worths = request.POST.getlist("asset_startup-worth", None)
    startup_extrafield = request.POST.getlist("asset_startup-extradata", None)

    jewelry_ids = request.POST.getlist("asset_jewelry_id")
    jewelry_names = request.POST.getlist("asset_jewelry", None)
    jewelry_worths = request.POST.getlist("asset_jewelry-worth", None)

    car_ids = request.POST.getlist("asset_car_id")
    car_names = request.POST.getlist("asset_car", None)
    car_worths = request.POST.getlist("asset_car-worth", None)
    car_extrafield = request.POST.getlist("asset_car-extradata", None)

    net_worth = 0

    for index, item in enumerate(bank_ids):
        if not bank_names[index] or not bank_worths[index]:
            continue

        asset_type = "BANK"
        if item:
            update_asset(item, bank_names[index], bank_worths[index])
        else:
            asset_bank = UserAssets.objects.create(
                email=request.user,
                type=asset_type,
                name=bank_names[index],
                worth=bank_worths[index]
            )
    
        net_worth += float(bank_worths[index])
    
    for index, item in enumerate(real_estate_ids):
        if not real_estate_names[index] or not real_estate_worths[index]:
            continue

        asset_type = "REAL_ESTATE"
        if item:
            update_asset(item, real_estate_names[index], real_estate_worths[index])
        else:
            asset_real_estate = UserAssets.objects.create(
                email=request.user,
                type=asset_type,
                name=real_estate_names[index],
                worth=real_estate_worths[index]
            )
        
        net_worth += float(real_estate_worths[index])
    
    for index, item in enumerate(insurance_ids):
        if not insurance_names[index] or not insurance_worths[index]:
            continue

        asset_type = "INSURANCE"
        if item:
            update_asset(item, insurance_names[index], insurance_worths[index])
        else:
            asset_insurance = UserAssets.objects.create(
                email=request.user,
                type=asset_type,
                name=insurance_names[index],
                worth=insurance_worths[index]
            )

        net_worth += float(insurance_worths[index])
    
    for index, item in enumerate(cryptocurrency_ids):
        if not cryptocurrency_names[index] or not cryptocurrency_worths[index]:
            continue

        asset_type = "CRYPTOCURRENCY"
        if item:
            update_asset(item, cryptocurrency_names[index], cryptocurrency_worths[index])
        else:
            asset_cryptocurrency = UserAssets.objects.create(
                email=request.user,
                type=asset_type,
                name=cryptocurrency_names[index],
                worth=cryptocurrency_worths[index]
            )

        net_worth += float(cryptocurrency_worths[index])
    
    for index, item in enumerate(nft_ids):
        if not nft_names[index] or not nft_worths[index]:
            continue

        asset_type = "NFT"
        if item:
            update_asset(item, nft_names[index], nft_worths[index])
        else:
            asset_nft = UserAssets.objects.create(
                email=request.user,
                type=asset_type,
                name=nft_names[index],
                worth=nft_worths[index]
            )

        net_worth += float(nft_worths[index])
    
    for index, item in enumerate(stock_ids):
        if not stock_names[index] or not stock_worths[index]:
            continue

        asset_type = "STOCK"
        if item:
            update_asset(item, stock_names[index], stock_worths[index], stock_extrafield[index])
        else:
            asset_stock = UserAssets.objects.create(
                email=request.user,
                type=asset_type,
                name=stock_names[index],
                worth=stock_worths[index],
                extra_field=stock_extrafield[index]
            )

        net_worth += float(stock_worths[index])
    
    for index, item in enumerate(startup_ids):
        if not startup_names[index] or not startup_worths[index]:
            continue

        asset_type = "STARTUP_INVESTMENT"
        if item:
            update_asset(item, startup_names[index], startup_worths[index], startup_extrafield[index])
        else:
            asset_startup = UserAssets.objects.create(
                email=request.user,
                type=asset_type,
                name=startup_names[index],
                worth=startup_worths[index],
                extra_field=startup_extrafield[index]
            )

        net_worth += float(startup_worths[index])

    for index, item in enumerate(jewelry_ids):
        if not jewelry_names[index] or not jewelry_worths[index]:
            continue

        asset_type = "JEWELRY"
        if item:
            update_asset(item, jewelry_names[index], jewelry_worths[index])
        else:
            asset_jewelry = UserAssets.objects.create(
                email=request.user,
                type=asset_type,
                name=jewelry_names[index],
                worth=jewelry_worths[index]
            )

        net_worth += float(jewelry_worths[index])
    
    for index, item in enumerate(car_ids):
        if not car_names[index] or not car_worths[index]:
            continue

        asset_type = "CAR"
        if item:
            update_asset(item, car_names[index], car_worths[index], car_extrafield[index])
        else:
            asset_car = UserAssets.objects.create(
                email=request.user,
                type=asset_type,
                name=car_names[index],
                worth=car_worths[index],
                extra_field=car_extrafield[index]
            )

        net_worth += float(car_worths[index])

    account = Account.objects.get(user=request.user)
    account.net_worth = net_worth
    account.save()

    return redirect('atm_functions:EditEstateNetWorth')

@login_required()
def insurance(request):

    return render(request, 'insurance.html')

@login_required()
def buy_security(request):

    return render(request, 'buy_security.html')

@login_required()
def crypto_news(request):
    url = "https://crypto-pulse.p.rapidapi.com/news"

    headers = {
        "X-RapidAPI-Host": "crypto-pulse.p.rapidapi.com",
        'X-RapidAPI-Key': '61a3b3ec9cmsh439f2a2ab87ea93p1491b9jsn78f11f47eb7e'
    }

    news = requests.request("GET", url, headers=headers).json()

    context = {
        "news_list": news
    }

    return render(request, 'crypto_news.html', context)

@login_required()
def swap_crypto(request):
    if request.method == "GET":

        # swap_transactions = TransactionC.objects.filter(email=request.user)

        # context = {
        #             "swap_transactions": swap_transactions
        # }

        # return render(request, 'swap_crypto.html', context)
        return render(request, 'swap_crypto.html')

    # # return HttpResponseRedirect(f"https://simpleswap.io/exchange?id={}")
    # currency_from = request.POST.get("sendCrypto")
    # currency_to = request.POST.get("getCrypto")
    # address_to = request.POST.get("receiverAddress")
    # user_refund_address = request.POST.get("refundAddress")
    # user_refund_extra_id = request.POST.get("refundAddressED", None)
    # amount = request.POST.get("sendingAmount")
    # extra_id_to = request.POST.get("extraData", None)

    # estimated_amount = request.POST.get("approximateAmount")

    # simpleswap_client = SimpleSwap()

    # try:
    #     if not user_refund_extra_id:
    #         response = simpleswap_client.create_new_exchange(currency_from, currency_to, address_to, user_refund_address, user_refund_extra_id, amount)
    #     else:
    #         response = simpleswap_client.create_new_exchange(currency_from, currency_to, address_to, user_refund_address, user_refund_extra_id, amount, extra_id_to)
    # except:
    #     messages.info(request, "Something went wrong. Please try again.")
    #     return redirect('atm_functions:SwapCrypto')

    # # print(response)
    # try:
    #     TransactionC.objects.create(transaction_id=response["id"], email=request.user, crypto_id_from=currency_from, crypto_id_to=currency_to, address_destination=address_to, address_destination_ed=extra_id_to, address_refund=user_refund_address, address_refund_ed=user_refund_extra_id, amount=amount, amount_estimated=response["amount_to"])
    # except:
    #     messages.info(request, "Something went wrong. Please try again.")
    #     return redirect('atm_functions:SwapCrypto')

    # messages.info(request, "Your swap request was completed successfully!")

    return redirect('atm_functions:SwapCrypto')


@login_required()
def buy_credit(request):
    if request.user.is_authenticated:
        u = User.objects.get(pk=request.user.pk)
        name = u.first_name
    else:
        name = None
    context = {'name': name}
    return render(request, 'buy_credit.html', context)

@login_required()
def atm_settings(request):
    if request.user.is_authenticated:
        u = User.objects.get(pk=request.user.pk)
        name = u.first_name
    else:
        name = None
    if request.method == "POST":
        request.session['currency'] = request.POST.get('currency')
        return redirect('atm_functions:Home')
    context = {
        # 'currency_list': currency_list,
        'name': name
    }
    return render(request, 'atm_settings.html', context)

@login_required()
def connect_wallet(request):
    if request.session['wallet_conn']:
        messages.info(request, "Your Coinbase account has already been connected.")
        return redirect('atm_functions:Home')

    if request.user.is_authenticated:
        u = User.objects.get(pk=request.user.pk)
        name = u.first_name
    else:
        name = None
    context = {'name': name}
    # print(request.session['wallet_conn'])

    return render(request, 'connect_wallet.html', context)

@login_required()
def approve_wallet(request):
    code = request.GET.get('code','')

    if code:
        # POST request template
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': os.environ['COINBASE_CLIENT_ID'],
            'client_secret': os.environ['COINBASE_CLIENT_SECRET'],
            'redirect_uri': "https://www.cryptoshareapp.com/atm/ApproveWallet/"
            # 'redirect_uri': "https://7361-2806-2f0-9020-ac47-e598-e859-b8ca-e292.ngrok.io/atm/ApproveWallet/"
        }

        # POST request to get access token
        response = requests.post(
            'https://api.coinbase.com/oauth/token', data=data).json()

        # print(response)
        request.session['access_token'] = response['access_token']
        request.session['refresh_token'] = response['refresh_token']
        request.session['wallet_conn'] = True

        coinbase_client = OAuthClient(
            request.session['access_token'], request.session['refresh_token'])

        user_data = coinbase_client.get_current_user()
        context = {'user_name': user_data.name}

        return render(request, 'approve_wallet.html', context)
    else:
        return redirect('atm_functions:ConnectWallet')

@login_required()
def disconnect_wallet(request):

    coinbase_client = OAuthClient(
        request.session['access_token'], request.session['refresh_token'])
    coinbase_client.revoke()

    request.session['wallet_conn'] = False
    request.session['access_token'] = None
    request.session['refresh_token'] = None

    return redirect('atm_functions:ConnectWallet')

@login_required()
def transfer_money(request):
    if not request.user.is_authenticated:
        return redirect('authentication:Home')

    context = {}
    
    return render(request, 'transfer_selection.html', context)

@login_required()
def send_cryptoshare_wallet(request):
    if not request.user.is_authenticated:
        return redirect('authentication:Home')
    
    context = {}

    # messages.info(request, "XRP, Ethereum, and ERC-20 tokens are currently not supported for sending funds.")

    balances = Balance.objects.filter(email=request.user, currency_name__isnull=False)
    context['balances'] = balances
    
    return render(request,'send_cryptoshare_wallet.html', context)

@login_required()
def transfer_credits(request):
    context = {}

    historical_transactions = TransactionCredits.objects.filter(
        Q(sender_user = request.user, transaction_type = "REQUEST", transaction_state = "PENDING") |
        Q(receiver_user = request.user, transaction_type = "REQUEST", transaction_state = "PENDING")
        ).order_by("-creation_datetime")

    context["historical_transactions"] = historical_transactions

    return render(request,'atm_functions/payments/cryptoshare_credits_selection.html', context)

@login_required()
def send_cryptoshare_credits(request):
    context = {}

    contacts = Contact.objects.filter(
        user = request.user
        )

    historical_transactions = TransactionCredits.objects.filter(
        Q(sender_user = request.user, transaction_type = "TRANSFER") |
        Q(receiver_user = request.user, transaction_type = "TRANSFER")
        ).order_by("-creation_datetime")

    cryptoshare_credits_object = DigitalCurrency.objects.get(symbol="CSC")

    balance = Balance.objects.filter(
        email = request.user,
        digital_currency_name = cryptoshare_credits_object
    )

    context['balances'] = balance
    context['historical_transactions'] = historical_transactions
    context['contacts'] = contacts

    return render(request,'send_cryptoshare_credits.html', context)

@login_required()
def request_cryptoshare_credits(request):
    context = {}

    if request.method == "GET":

        contacts = Contact.objects.filter(
            user = request.user
            )
        
        context['contacts'] = contacts

        return render(request,'atm_functions/payments/request_cryptoshare_credits.html', context)
    
    elif request.method == "POST":
        form_response = request.POST

        action = request.GET.get("action", "")

        
        if action == "request":

            receiverForm = form_response["receiverForm"]

            amount = form_response["request_amount"]
            note = form_response.get("note", None)
            
            cryptoshare_credits_object = DigitalCurrency.objects.get(symbol="CSC")

            #MISSING BUSINESS SENDING CREDITS IMPLEMENTATION
            receiver_account = Account.objects.get(
                user = request.user
            )

            if receiverForm == "username":
                payer_username = form_response["payer_user"].lower().replace(" ", "")

            elif receiverForm == "contact":
                payer_contact_id = form_response["user_contact"]
                payer_user_object = Contact.objects.get(
                    id = payer_contact_id
                    ).user_reference

                payer_username = DynamicUsername.objects.get(
                    user_reference = payer_user_object
                    ).id_username

            if DynamicUsername.objects.filter(id_username = payer_username).exists():
                payer_username_object = DynamicUsername.objects.get(id_username = payer_username)
            else:
                messages.warning(request, "Invalid username. Please try again.")
                return redirect('atm_functions:SendCryptoShareCredits')
            
            if payer_username_object.username_type == "BUSINESS":
                business = payer_username_object.business_reference
                payer_user = business.owner
            elif payer_username_object.username_type == "USER":
                payer_user = payer_username_object.user_reference
            
            if payer_user == request.user:
                messages.info(request, "You can't request credits to yourself.")
                return redirect('atm_functions:RequestCryptoShareCredits')
                
            TransactionCredits.objects.create(
                sender_user = payer_user,
                sender_username = payer_username,
                receiver_user = request.user,
                receiver_username = receiver_account.system_username,
                digital_currency_name = cryptoshare_credits_object,
                transaction_type = "REQUEST",
                transaction_state = "PENDING",
                amount = amount,
                note = note
            )

            payment_request(str(payer_user))

        elif action == "cancel":

            transaction_id = request.GET.get("id", "")
            
            if not TransactionCredits.objects.filter(id_transaction = transaction_id).exists():
                messages.warning(request, "Invalid transaction. Please try again.")
                return redirect('atm_functions:TransferCredits')

            transaction = TransactionCredits.objects.get(id_transaction = transaction_id)

            if transaction.receiver_user != request.user:
                messages.warning(request, "You can't do this!")
                return redirect('atm_functions:TransferCredits')
            
            transaction.transaction_state = "CANCELLED"
            transaction.save()

            messages.info(request, "Transaction cancelled.")
            return redirect('atm_functions:TransferCredits')

        elif action == "deny":

            transaction_id = request.GET.get("id", None)

            if not TransactionCredits.objects.filter(id_transaction = transaction_id).exists():
                messages.warning(request, "Invalid transaction. Please try again.")
                return redirect('atm_functions:TransferCredits')

            transaction = TransactionCredits.objects.get(id_transaction = transaction_id)

            if transaction.sender_user != request.user:
                messages.warning(request, "You can't do this!")
                return redirect('atm_functions:TransferCredits')
            
            transaction.transaction_state = "DENIED"
            transaction.save()

            messages.info(request, "Transaction denied.")

            return redirect('atm_functions:TransferCredits')

        elif action == "accept":

            transaction_id = request.GET.get("id", None)

            if not TransactionCredits.objects.filter(id_transaction = transaction_id).exists():
                messages.warning(request, "Invalid transaction. Please try again.")
                return redirect('atm_functions:TransferCredits')
            
            transaction = TransactionCredits.objects.get(id_transaction = transaction_id)

            if transaction.sender_user != request.user:
                messages.warning(request, "You can't do this!")
                return redirect('atm_functions:TransferCredits')
            
            cryptoshare_credits_object = DigitalCurrency.objects.get(symbol="CSC")

            transaction.transaction_state = "COMPLETED"

            sender_balance = Balance.objects.get(
                email = transaction.sender_user,
                digital_currency_name = cryptoshare_credits_object
            )

            receiver_balance = Balance.objects.get(
                email = transaction.receiver_user,
                digital_currency_name = cryptoshare_credits_object
            )

            sender_balance.amount -= transaction.amount
            receiver_balance.amount += transaction.amount
            sender_balance.save()
            receiver_balance.save()
            transaction.save()

            messages.info(request, "Transaction completed.")

            return redirect('atm_functions:TransferCredits')
        
        return render(request,'atm_functions/payments/request_cryptoshare_credits.html', context)




    return render(request,'atm_functions/payments/request_cryptoshare_credits.html', context)

@login_required()
def send_coinbase_wallet(request):

    if not request.session['wallet_conn']:
        # Temporary redirect to connect wallet while CryptoApis implementation is in progress.
        messages.info(request, "You must connect your Coinbase account to send money.")
        return redirect('atm_functions:ConnectWallet')

    accounts = {}
    coinbase_client = OAuthClient(
        request.session['access_token'], request.session['refresh_token'])
    all_accounts = coinbase_client.get_accounts()["data"]

    # Get into dict only the accounts that have a balance greater than 0
    for account in all_accounts:
        if float(account['balance']['amount']) > 0:
            accounts[account['currency']] = {
                'balance': account['balance']['amount'],
                'id': account['id']
            }

    user_data = coinbase_client.get_current_user()

    context = {
        'user_name': user_data.name,
        'accounts': accounts
    }

    return render(request, 'send_money.html', context)

@login_required()
def send_money_confirmation(request):
    form_response = request.POST

    if not form_response:
        return redirect('atm_functions:TransferMoney')

    wallet_confirmation = request.GET.get('wallet','')

    if wallet_confirmation == "coinbase":

        coinbase_client = OAuthClient(request.session['access_token'], request.session['refresh_token'])

        recipient_account = form_response["recipientUser"]
        account_info = form_response["sendingAccount"].split(" ")
        account_id = account_info[0]
        account_currency = account_info[1]
        amount = str(form_response["sendingAmount"])

        authCode = request.POST.get("authCode")
        # print(form_response)
        # print(authCode)
        if authCode:
            # print("Authcode detected")
            authcode = form_response['authCode']
            try:
                tx = coinbase_client.send_money(
                    account_id,
                    to = recipient_account,
                    amount = amount,
                    currency = account_currency,
                    two_factor_token = authcode
                )

                # print(tx)
                messages.info(request, "Money sent successfully.")

                user_data = coinbase_client.get_current_user()

                sender_email = user_data.email
                concept = tx["details"]["header"]
                tx_amount = tx["amount"]
                tx_native_amount = tx["native_amount"]
                tx_state = tx["details"]["health"]
                receiver_email = tx["to"]["email"]
                creation_date  = tx["created_at"]

                sent_funds_email(sender_email, concept, tx_amount, tx_native_amount, tx_state, creation_date, receiver_email)
                
                return redirect('atm_functions:CheckCredit')
            except Exception as e:
                # print(e)
                messages.info(request, "Invalid authorization code. Please try again.")
                return redirect('atm_functions:TransferMoney')

        else:
            # fa_code = form_response["authCode"]
            try:
                tx = coinbase_client.send_money(
                    account_id,
                    to=recipient_account,
                    amount=amount,
                    currency=account_currency
                )
                # print(tx)
                messages.info(request, "Money sent successfully.")
                return redirect('atm_functions:CheckCredit')

            except TwoFactorRequiredError:
                context = {
                    "recipientUser": recipient_account,
                    "sendingAccount": form_response["sendingAccount"],
                    "sendingAmount": amount
                }
                messages.info(request, "Two factor authentication required.")
                return render(request, '2fa_token.html', context)
                # return redirect('atm_functions:TransferMoney')
            except Exception as e:
                # print(e)
                messages.info(request, "Error sending money. Please try again.")
                return redirect('atm_functions:TransferMoney')

    elif wallet_confirmation == "cryptoshare":
        wallet_currencies = {
                            "Litecoin": True,
                            "Dash": True,
                            "Zcash": True,
                            "Bitcoin Cash": True,
                            "Bitcoin": True,
                            "Dogecoin": True
        }

        address_currencies = {
                            "XRP": True,
                            "Ethereum": True,
                            "USD Coin": True,
                            "Thether": True
        }

        sending_account = form_response["sendingAccount"].split("|")
        sending_currency = sending_account[0]
        sending_blockchain = sending_account[1]

        # if sending_currency in address_currencies:
        #     # messages.info(request, "XRP and Ethereum are currently not supported for sending funds.")
        #     return redirect('atm_functions:SendCryptoShareWallet')

        pre_amount = form_response["sendingAmount"]
        amount = str(float(form_response["sendingAmount"]) * 0.99)
        recipient_address = form_response["recipientUser"]

        currency_object = Cryptocurrency.objects.get(currency_name=sending_currency)
        balance_object = Balance.objects.get(email=request.user, currency_name=currency_object)
        sending_address_object = Address.objects.get(currency_name=currency_object, email=request.user)

        if float(balance_object.amount) < float(amount):
            messages.info(request, "Insufficient funds.")
            return redirect('atm_functions:SendCryptoShareWallet')

        cryptoapis_client = CryptoApis()

        is_valid_address = cryptoapis_client.is_valid_address(sending_blockchain, "mainnet", recipient_address)
        if not is_valid_address:
            messages.info(request, "Invalid address. Please try again.")
            return redirect('atm_functions:SendCryptoShareWallet')

        if sending_currency in wallet_currencies:
            transaction_response = cryptoapis_client.generate_coins_transaction_from_wallet(sending_blockchain, "mainnet", recipient_address, amount)
            # print(request)
        else:
        # elif sending_currency in address_currencies:
            transaction_response = cryptoapis_client.generate_coins_transaction_from_address(sending_blockchain, "mainnet",sending_address_object.address ,recipient_address, amount)
        # print(request)
        if sending_currency in wallet_currencies:
            total_transaction_amount = transaction_response["totalTransactionAmount"]
        else:
            total_transaction_amount = transaction_response["recipients"][0]["amount"]
            
        transaction_id = transaction_response["transactionRequestId"]

        balance_object.amount -= Decimal(pre_amount)
        balance_object.save()

        transaction_a = TransactionA(transaction_id=transaction_id, email=request.user, address=sending_address_object, currency_name=currency_object, transaction_type="WITHDRAWAL", state="PENDING", amount=amount, internal_state="WAITING_FOR_APPROVAL")
        transaction_a.save()
        # print(sending_blockchain, sending_currency, amount, recipient_address)

        sent_funds_cryptoshare_wallet_email(str(transaction_a.email), "SENT FUNDS REQUEST", transaction_a.currency_name.currency_name ,transaction_a.amount, "PENDING", transaction_a.creation_datetime, receiver=recipient_address)
        calculate_credit_grade(request.user)

        messages.success(request, "Your withdrawal request has been created")

        return redirect('atm_functions:CheckCredit')

    elif wallet_confirmation == "credits":
        # sending_account = form_response["sendingAccount"].split("|")
        amount = float(form_response["sendingAmount"])
        receiverForm = request.POST.get('receiverForm')

        if receiverForm == "username":
            recipient_username = form_response["recipient_user"].lower().replace(" ", "")
        elif receiverForm == "contact":
            recipient_contact_id = form_response["user_contact"]
            recipient_user_object = Contact.objects.get(id=recipient_contact_id).user_reference

            recipient_username = DynamicUsername.objects.get(
                user_reference = recipient_user_object
                ).id_username

        cryptoshare_credits_object = DigitalCurrency.objects.get(symbol="CSC")

        #MISSING BUSINESS SENDING CREDITS IMPLEMENTATION
        sender_account = Account.objects.get(
            user = request.user
            )


        if DynamicUsername.objects.filter(id_username = recipient_username).exists():
            recipient_username_object = DynamicUsername.objects.get(id_username = recipient_username)
        else:
            messages.warning(request, "Invalid username. Please try again.")
            return redirect('atm_functions:SendCryptoShareCredits')
        
        if recipient_username_object.username_type == "BUSINESS":
            business = recipient_username_object.business_reference
            recipient_user = business.owner
        elif recipient_username_object.username_type == "USER":
            recipient_user = recipient_username_object.user_reference
        
        if recipient_user == request.user:
            messages.info(request, "You can't send credits to yourself.")
            return redirect('atm_functions:SendCryptoShareCredits')

        sender_balance = Balance.objects.get(
            email=request.user, 
            digital_currency_name = cryptoshare_credits_object
            )

        if sender_balance.amount < amount:
            messages.warning(request, "Insufficient funds.")
            return redirect('atm_functions:SendCryptoShareCredits')

        receiver_balance = Balance.objects.get(
            email=recipient_user, 
            digital_currency_name = cryptoshare_credits_object
            )

        sender_balance.amount -= Decimal(amount)
        sender_balance.save()
        receiver_balance.amount += Decimal(amount)
        receiver_balance.save()

        TransactionCredits.objects.create(
            sender_user = request.user,
            sender_username = sender_account.system_username,
            receiver_user = recipient_user,
            receiver_username = recipient_username,
            digital_currency_name = cryptoshare_credits_object,
            transaction_type = "TRANSFER",
            transaction_state = "COMPLETED",
            amount = amount
        )


        messages.success(request, "Your transfer has been completed.")
        
        return redirect('atm_functions:Home')

    else:
        return redirect('atm_functions:Home')

@login_required()
def my_addresses(request):
    if not request.user.is_authenticated:
        return redirect('authentication:Home')
    addresses = Address.objects.filter(email=request.user)
    auth_confirmation = True

    context = {
            'authConfirmation': auth_confirmation, 
            'addresses': addresses
            }
    return render(request, 'my_addresses.html', context)

@login_required()
def my_transactions(request):
    if not request.user.is_authenticated:
        return redirect('authentication:Home')
    auth_confirmation = True
    
    #Deposit Transactions
    deposit_transactions = TransactionA.objects.filter(email=request.user, transaction_type = "DEPOSIT")

    #Deposit Transactions
    withdrawal_transactions = TransactionA.objects.filter(email=request.user, transaction_type = "WITHDRAWAL")

    context = {
            "authConfirmation": auth_confirmation,
            "deposit_transactions": deposit_transactions,
            "withdrawal_transactions": withdrawal_transactions
            }

    return render(request, 'my_transactions.html', context)

@login_required()
def generate_address(request):
    blockchain = request.GET.get('blockchain','')
    network = request.GET.get('network','')
    currency = request.GET.get('currency','')

    currency_object = Cryptocurrency.objects.get(currency_name=currency)
    email_object = request.user

    if not blockchain or not network or not currency:
        messages.info(request, "Invalid option, please try again.")
        return redirect('atm_functions:Home')
    
    #Check if there is already a balance with that currency name for that email
    balance_exists = Balance.objects.filter(email=email_object, currency_name=currency_object)
    if not balance_exists:
        new_balance = Balance(email=email_object, currency_name=currency_object, amount = 0)
        new_balance.save()

    cryptoapis_utils = CryptoApisUtils()

    address, error = cryptoapis_utils.generate_address(request.user, currency_object, register_function = True)
    if error is not None:
        messages.info(request, error)
        return redirect('atm_functions:Home')
    
    messages.info(request, "Address generated successfully.")

    return redirect('atm_functions:Home')

@login_required()
def blockchain_wills(request):

    if request.method == "POST":
        digital_currency_object = DigitalCurrency.objects.get(symbol="CSC")
        user_balance = Balance.objects.get(email = request.user, digital_currency_name = digital_currency_object)

        blockchain_will_price = 100      #PRICE IN CRYPTOSHARE CREDITS

        if user_balance.amount < blockchain_will_price:
            messages.info(request, "You do not have enough funds to create a business. Please buy more CryptoShare Credits.")
            return redirect('atm_functions:Home')
            
        user_balance.amount -= Decimal(blockchain_will_price)
        user_balance.save()
        blockchain_will = BlockchainWill.objects.create(email= request.user, status="NOT COMPLETED")
        beneficiary = Beneficiary(will_percentage=100)
        beneficiary.save()
        beneficiary.blockchain_wills.add(blockchain_will)

        return redirect(reverse('atm_functions:RegisterBlockchainWill')+f"?id={blockchain_will.id_w}")
    if request.method == "GET":
        blockchain_wills = BlockchainWill.objects.filter(email=request.user)
        context = {
            "blockchain_wills": blockchain_wills
        }
        return render(request, 'blockchain_wills.html', context)

    return render(request, 'blockchain_wills.html')

@login_required()
def register_blockchain_will(request):

    will_id = request.GET.get('id','')

    if not will_id:
        messages.info(request, "Invalid request, please try again.")
        return redirect('atm_functions:BlockchainWills')
    else:
        blockchain_will = BlockchainWill.objects.get(id_w=will_id)
        if blockchain_will.email != request.user:

            messages.info(request, "Invalid request, please try again.")
            return redirect('atm_functions:BlockchainWills')

    if request.method == "GET":
        beneficiary = Beneficiary.objects.filter(blockchain_wills__in = [blockchain_will])
        if beneficiary:
            beneficiary = beneficiary[0]
        else:
            # beneficiary = Beneficiary(
            #                             full_legal_name = "",
            #                             birthdate = "",
            #                             birth_country = "",
            #                             relationship = "",
            #                             associated_email1 = "",
            #                             associated_email2 = "",
            #                             will_percentage = 100,
            #                             selfie_photo_url = ""
            #                         )
            beneficiary = None

        countries = countries_tuples

        context = {
            "blockchain_will": blockchain_will,
            "beneficiary": beneficiary,
            "beneficiary_relationships": ["Wife", "Husband", "Life Partner", "Child", "Friend", "Other"],
            "countries": countries
        }
        return render(request, 'blockchain_will_edit.html', context)

    grantor_fullname = request.POST.get("grantor_fullname", None)
    grantor_birthdate = request.POST.get("grantor_birthdate", None)
    grantor_country = request.POST.get("grantor_country", None)
    grantor_email_1 = request.POST.get("grantor_email_1", None)
    grantor_email_2 = request.POST.get("grantor_email_2", None)
    grantor_email_3 = request.POST.get("grantor_email_3", None)
    grantor_selfie_photo_url = request.POST.get("grantor_selfie_photo", None)
    grantor_id_document_url = request.POST.get("grantor_id_document", None)

    blockchain_will.full_legal_name = grantor_fullname
    if grantor_birthdate:
        blockchain_will.birthdate = grantor_birthdate
    blockchain_will.birth_country = grantor_country
    blockchain_will.associated_email1 = grantor_email_1
    blockchain_will.associated_email2 = grantor_email_2
    blockchain_will.associated_email3 = grantor_email_3
    blockchain_will.selfie_photo_url = grantor_selfie_photo_url
    blockchain_will.document_id_url = grantor_id_document_url

    #BENEFICIARY

    beneficiary_id = request.POST.get("beneficiary_id", None)
    beneficiary_fullname = request.POST.get("beneficiary_fullname", None)
    beneficiary_birthdate = request.POST.get("beneficiary_birthdate", None)
    beneficiary_country = request.POST.get("beneficiary_country", None)
    beneficiary_relationship = request.POST.get("beneficiary_relationship", None)
    beneficiary_email_1 = request.POST.get("beneficiary_email_1", None)
    beneficiary_email_2 = request.POST.get("beneficiary_email_2", None)
    beneficiary_selfie_photo_url = request.POST.get("beneficiary_selfie_photo", None)

    beneficiary = Beneficiary.objects.get(pk=int(beneficiary_id))
    beneficiary.full_legal_name = beneficiary_fullname
    if beneficiary_birthdate:
        beneficiary.birthdate = beneficiary_birthdate
    beneficiary.birth_country = beneficiary_country
    beneficiary.relationship = beneficiary_relationship
    beneficiary.associated_email1 = beneficiary_email_1
    beneficiary.associated_email2 = beneficiary_email_2
    beneficiary.selfie_photo_url = beneficiary_selfie_photo_url
    beneficiary.save()

    save_will = request.GET.get('save_will','')

    if not save_will:
        # cryptoapis_client = CryptoApis()
        # transaction_response = cryptoapis_client.generate_coins_transaction_from_wallet("dash", "mainnet", "Xh1daZF6rafvc2gieJXzhr71wQtzuvk6C3", "1", data=f"CryptoShare Blockchain Will - {blockchain_will.id_w}|{str(blockchain_will.email)}")
        # transaction_id = transaction_response["transactionRequestId"]

        blockchain_will.status = "ACTIVE"
        blockchain_will.transaction_id = blockchain_will.id_w
        messages.info(request, "Blockchain Will successfully created.")


    blockchain_will.save()

    if save_will:
        json_response = {
            "beneficiary_id": beneficiary.id
        }
        if not beneficiary_id:
            json_response["status"] = "NEW_BENEFICIARY",
        else:
            json_response["status"] = "SUCCESS"

        return HttpResponse(json.dumps(json_response), content_type="application/json")

    return redirect('atm_functions:BlockchainWills')

@login_required()
def certificate_blockchain_will(request, id = None):
    def write_text(image, text, FONT, textsize, x, y):

        textX = (x - textsize[0]) // 2
        textY = (y + textsize[1]) // 2

        cv2.putText(image, text, (textX, textY), FONT, 1, (0, 0, 0), 1, cv2.LINE_AA)

    def generate_certificate(name, transactionId, innerTransactionId, date):
        template_url = os.path.join(django_settings.BASE_DIR, 'static/pdf_templates/Will_Certificate_Template.jpg')
        temp_certificates = os.path.join(django_settings.BASE_DIR, 'static/temp_certificates')
        new_certificate = f"{temp_certificates}/{name.strip()}.pdf"

        certificate_template_image = cv2.imread(template_url)
        FONT = cv2.FONT_HERSHEY_DUPLEX

        text = name.strip()

        textsize_name = cv2.getTextSize(text, FONT, 1, 0)[0]
        textsize = cv2.getTextSize(text, FONT, 0.5, 0)[0]

        coordinates = [
            [180 * 2, 1020 * 2],
            [540 * 2, 1180 * 2],
            [100 * 2, 1590 * 2],
            [1040 * 2, 1830 * 2],
        ]

        write_text(certificate_template_image, transactionId.strip(), FONT, textsize, coordinates[0][0], coordinates[0][1])
        write_text(certificate_template_image, date.strip(), FONT, textsize, coordinates[1][0], coordinates[1][1])
        write_text(certificate_template_image, innerTransactionId.strip(), FONT, textsize, coordinates[2][0], coordinates[2][1])
        write_text(certificate_template_image, name.strip(), FONT, textsize_name, coordinates[3][0], coordinates[3][1])

        cv2_path = f"{temp_certificates}/{name.strip()}.jpg"
        cv2.imwrite(cv2_path, certificate_template_image)

        img = Image.open(f"{temp_certificates}/{name.strip()}.jpg")
        img = img.convert("RGB")
        img.save(new_certificate, format="PDF")

        return new_certificate

    if id is None:
        return redirect('atm_functions:BlockchainWills')

    user = request.user
    user_name = user.first_name + " " + user.last_name
    blockchain_will = BlockchainWill.objects.get(pk=id)

    if blockchain_will.email != request.user or blockchain_will.status != "ACTIVE":
        return redirect('atm_functions:BlockchainWills')

    if blockchain_will.transaction_id is None:
        blockchain_will.transaction_id = "18b513a31bc8381ca73258b98229c8661d562ae92e30df81936aa398c74e3118"

    url = generate_certificate(user_name, blockchain_will.transaction_id, f"{id}|{blockchain_will.transaction_id}", f"{formats.date_format(blockchain_will.creation_datetime, 'DATETIME_FORMAT')} UTC")

    try:
        return FileResponse(open(url, 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()
   

def get_credit_grade(request):
    user = Account.objects.get(user = request.user)

    test = {
        "credit_grade": user.credit_grade
    }
    return HttpResponse(json.dumps(test), content_type="application/json")

def get_currencies_balance_widget(request):
    user = request.user

    symbols = [
        "BTC",
        "ETH",
        "USDC",
        "DASH",
        "LTC"
    ]
    balances = Balance.objects.filter(email= user, currency_name__symbol__in = symbols).select_related('currency_name')

    cryptoshare_credits_balance = Balance.objects.filter(email=user, digital_currency_name__symbol = "CSC").select_related("digital_currency_name")[0]
    response = {}

    for balance in balances:
        currency = {
            "symbol": balance.currency_name.symbol,
            "balance": round(float(balance.amount), 2)
        }
        response[balance.currency_name.symbol] = currency
    
    response[cryptoshare_credits_balance.digital_currency_name.symbol] = {
        "symbol": cryptoshare_credits_balance.digital_currency_name.symbol,
        "balance": round(float(cryptoshare_credits_balance.amount), 0)
    }
    return HttpResponse(json.dumps(response), content_type="application/json")

# @csrf_exempt
def simpleswap_api(request):
    if request.method == "GET":
        return HttpResponse(status=400)

    request_type = request.GET.get('type','')
    if not request_type:
        return HttpResponse(status=400)

    simpleswap_client = SimpleSwap()

    accepted_pairs = {
                        "BTC": "Bitcoin",
                        "ETH": "Ethereum",
                        "LTC": "Litecoin",
                        "BCH": "Bitcoin Cash",
                        "ZEC": "Zcash",
                        "XRP": "XRP",
                        "DASH": "Dash",
                        "DOGE": "Dogecoin",
                        "LINK": "Chainlink (ERC-20)",
                        "SHIB": "SHIBA INU (ERC-20)",
                        "BAT": "Basic Attention Token (ERC-20)",
                        "USDC": "USD Coin (ERC-20)",
                        "USDTERC20": "Tether (ERC-20)",
                        "WBTC": "Wrapped Bitcoin (ERC-20)",
                        "MKR": "Maker (ERC-20)"
    }

    if request_type == "CURRENCY_EXCHANGE_PAIRS":
        symbol = request.POST.get('symbol','')

        currency_exchange_pairs = simpleswap_client.get_exchange_pairs_for_currency(symbol)
        pairs = {}

        for pair in currency_exchange_pairs:
            if pair.upper() in accepted_pairs:
                pairs[pair.upper()] = accepted_pairs[pair.upper()]

        return HttpResponse(json.dumps(pairs), content_type="application/json")

    elif request_type == "ESTIMATED_EXCHANGE_AMOUNT":
        currency_from = request.POST.get('currency_from','')
        currency_to = request.POST.get('currency_to','')
        amount = request.POST.get('amount','')

        estimated_exchange_amount = simpleswap_client.get_estimated_exchange_amount(currency_from, currency_to, amount)

        return HttpResponse(json.dumps(estimated_exchange_amount), content_type="application/json")

    elif request_type == "MINIMAL_EXCHANGE_AMOUNT":
        currency_from = request.POST.get('currency_from','')
        currency_to = request.POST.get('currency_to','')

        currency_data = swap_crypto_info[currency_to]
        
        minimal_exchange_amount = simpleswap_client.get_minimal_exchange_amount(currency_from, currency_to)

        response = {
                    "minimal_exchange_amount": minimal_exchange_amount,
                    "currency_data": currency_data
        }

        return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def register_waitlist_email(request):
    email = request.POST.get('UserEmail','')

    WaitingList.objects.create(email=email)

    return redirect ('authentication:Email')

@csrf_exempt
def stripe_webhook(request):
    response_body = json.loads(request.body)

    if response_body['type'] != "payment_intent.succeeded":
        return HttpResponse(status=200)

    customer_id = response_body["data"]["object"]["customer"]
    bought_amount = response_body["data"]["object"]["amount"]
    payment_intent = response_body["data"]["object"]["id"]
    transaction_type = response_body['type']

    # stripe_customer_object = StripeAccount.objects.get(stripe_customer_id="cus_MBazDa7gq6ZfbH")
    stripe_customer_object = StripeAccount.objects.get(stripe_customer_id=customer_id)
    stripe_transaction = TransactionStripe.objects.get(payment_intent=payment_intent)

    cryptoshare_credits_object = DigitalCurrency.objects.get(symbol="CSC")

    user_balance = Balance.objects.get(email=stripe_customer_object.user, digital_currency_name=cryptoshare_credits_object)
    user_balance.amount += stripe_transaction.amount
    user_balance.save()

    stripe_transaction.transaction_state = "COMPLETED"
    stripe_transaction.transaction_type_internal = transaction_type
    stripe_transaction.save()

    # MISSING TO SEND EMAIL TO USER

    return HttpResponse(status=200)

@csrf_exempt
def update_exchange_rates(request):
    if request.method == "POST":
        return HttpResponse(status=400)

    currencies = Cryptocurrency.objects.all()

    querystring_options ={
                        "ETH": "ethereum",
                        "LTC": "litecoin",
                        "BCH": "bitcoin-cash",
                        "DASH": "dash",
                        "ZEC": "zcash",
                        "USDC": "usd-coin",
                        "USDT": "tether",
                        "WBTC": "bitcoin",
                        "BTC": "bitcoin",
                        "XRP": "ripple",
                        "DOGE": "dogecoin",
                        "BAT": "basic-attention-token",
                        "LINK": "chainlink",
                        "SHIB": "shiba-inu",
                        "MKR": "maker",
                        "XAUT": "tether-gold",
                        }

    ids = []

    for option in querystring_options.values():
        ids.append(option)

    url = f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(ids)}&vs_currencies=usd&include_market_cap=false&include_24hr_vol=false&include_24hr_change=false&include_last_updated_at=false"
    # ids = 'ethereum,litecoin,bitcoin-cash,dash,zcash,usd-coin,tether,bitcoin,bitcoin,ripple,dogecoin'
    # url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd&include_market_cap=false&include_24hr_vol=false&include_24hr_change=false&include_last_updated_at=false"

    response = requests.get(url).json()
    
    for currency in currencies:
        if currency.symbol == "TEST" or currency.currency_name == "ethereum_ropsten":
            continue
        
        try:
            coingecko_id = querystring_options[currency.symbol]

            exchange_rate = response[coingecko_id]["usd"]
            currency.exchange_rate = exchange_rate
            currency.save()
        except:
            print(f"{coingecko_id} not found in coingecko")
    
    return HttpResponse(status=200)

@csrf_exempt
def daily_routine(request):
    if request.method == "GET":
        checksum = "482f9e2ed75e9df2fbd2753d17a0285460abea29840302ab10619efeff66fcba"
        key = request.GET.get('key','')

        if key == "":
            return HttpResponse(status=400)
        elif checksum != hashlib.sha256(key.encode('utf-8')).hexdigest():
            return HttpResponse(status=400)

        # <------------ DEACTIVATE UNUSED ADDRESSES ------------>
        # test_user = User.objects.get(pk=88)

        # to_delete_addresses = Address.objects.filter(expiration_datetime__date__lte=timezone.now().date(), email=test_user)[0:1]
        to_delete_addresses = Address.objects.filter(expiration_datetime__date__lte=timezone.now().date())
        for address in to_delete_addresses:
            email = str(address.email)

            address.email = None

            #SEND NOTIFICATION EMAIL

            try:
                revoked_address_email(email, address.address, address.currency_name.currency_name, address.currency_name.blockchain)
            except:
                continue
            
            address.expiration_datetime = None
            address.save()
        # <------------ DEACTIVATE UNUSED ADDRESSES ------------>      

        # <------------ FINISH EXPIRED TRANSACTIONS ------------>
        to_delete_transactionsb = TransactionB.objects.filter(Q(end_datetime__date__lte=timezone.now().date()) & Q(state="IN PROGRESS"))
        for transaction in to_delete_transactionsb:
            transaction.state = "EXPIRED"

            interest_rate = transaction.interest_rate

            if interest_rate == 5:
                days_to_pay = 15
            elif interest_rate == 10:
                days_to_pay = 30
            elif interest_rate == 15:
                days_to_pay = 60
            elif interest_rate == 20:
                days_to_pay = 90

            if transaction.transaction_type == "BORROW":
                borrower_user = transaction.emitter
                lender_user = transaction.receptor

            elif transaction.transaction_type == "LEND":
                borrower_user = transaction.receptor
                lender_user = transaction.emitter

            expired_transactionb_email(
                                    str(borrower_user), 
                                    "BORROWER", 
                                    transaction.id_b, 
                                    transaction.currency_name.currency_name, 
                                    transaction.currency_name_colllateral.currency_name, 
                                    transaction.amount, 
                                    transaction.amount_collateral, 
                                    transaction.interest_rate, 
                                    days_to_pay, 
                                    transaction.start_datetime.date(), 
                                    transaction.end_datetime.date()
                                    )

            expired_transactionb_email(
                                    str(lender_user), 
                                    "LENDER", 
                                    transaction.id_b, 
                                    transaction.currency_name.currency_name, 
                                    transaction.currency_name_colllateral.currency_name, 
                                    transaction.amount, 
                                    transaction.amount_collateral, 
                                    transaction.interest_rate, 
                                    days_to_pay, 
                                    transaction.start_datetime.date(), 
                                    transaction.end_datetime.date()
                                    )

            # < ----------------------------------- ACCREDITATION OF COLLATERAL  ----------------------------------- >

            currency_collateral_object = transaction.currency_collateral
            currency_collateral_amount = transaction.amount_collateral

            try:
                collateral_balance = Balance.objects.get(email=lender_user, currency_name=currency_collateral_object)
            except:
                collateral_balance = Balance(email=lender_user, currency_name=currency_collateral_object, amount = 0)

            if transaction.currency_name_collateral.currency_name == "XRP":
                cryptoapis_client = CryptoApis()

                sender_address = Address.objects.get(email=borrower_user, currency_name=currency_collateral_object)
                address_exists = Address.objects.filter(email=lender_user, currency_name=currency_collateral_object)

                if not address_exists:
                    number_of_addresses = Address.objects.filter(currency_name=currency_collateral_object).count()
                    # < ----------------------------------- HERE MISSING ERROR EXCEPTION HANDLING ----------------------------------- >
                    # < ----------------------------------- HERE MISSING ERROR EXCEPTION HANDLING ----------------------------------- >
                    deposit_address = cryptoapis_client.generate_deposit_address(currency_collateral_object.blockchain, currency_collateral_object.network, number_of_addresses)

                    newAddress = Address(address=deposit_address, email=lender_user, currency_name=currency_collateral_object, expiration_datetime = None)
                    newAddress.save()

                    cryptoapis_client.generate_coin_subscription(currency_collateral_object.blockchain, currency_collateral_object.network, deposit_address)
                    # < ----------------------------------- HERE MISSING ERROR EXCEPTION HANDLING ----------------------------------- >
                    # < ----------------------------------- HERE MISSING ERROR EXCEPTION HANDLING ----------------------------------- >
                else:
                    deposit_address = address_exists[0].address

                transaction_response = cryptoapis_client.generate_coins_transaction_from_address(
                                                                                                currency_collateral_object.blockchain, 
                                                                                                "mainnet",
                                                                                                sender_address.address, 
                                                                                                deposit_address, 
                                                                                                currency_collateral_amount)
            else:
                collateral_balance.amount += currency_collateral_amount
            
            collateral_balance.save()
            transaction.save()
            # < ----------------------------------- ACCREDITATION OF COLLATERAL  ----------------------------------- >

        # <------------ FINISH EXPIRED TRANSACTIONS ------------>  
        return HttpResponse(status=200)
    elif request.method == "POST":
        return HttpResponse(status=500)
    pass

@csrf_exempt
def confirmations_coin_transactions(request):
    if request.method == "GET":
        return redirect('authentication:Home')
    
    elif request.method == "POST":
        if ("Transfer-Encoding" in request.headers) and (request.headers["Transfer-Encoding"] == "chunked"):
            request_reader = request.META.get('wsgi.input')

            # bpayload = request_reader.stream.read1()  # UNCOMMENT FOR LOCAL TESTING ENVIRRONMENT
            bpayload = request_reader.read() #UNCOMMENT FOR PRODUCTION ENVIRONMENT
        else:
            bpayload = request.body

        payload = bpayload.decode("utf-8")

        start = payload.index("{")
        end = payload.rindex("}") + 1

        response = json.loads(payload[start:end])

        reference_id = response["referenceId"]
        data = response["data"]
        event = data["event"]

        transaction = TransactionA.objects.get(transaction_id=reference_id)
        transaction.internal_state = event

        receiver_user = User.objects.get(username=transaction.email)
        currency_object = transaction.currency_name


        if event == "TRANSACTION_REQUEST_APPROVAL":
            pass
        elif event == "TRANSACTION_REQUEST_BROADCASTED":
            pass
        elif event == "TRANSACTION_REQUEST_MINED":
            transaction.state = "APPROVED"
            sent_funds_cryptoshare_wallet_email(str(transaction.email), "COMPLETED SENT FUNDS", transaction.currency_name.currency_name ,transaction.amount, "APPROVED", transaction.creation_datetime)

        elif event == "TRANSACTION_REQUEST_REJECTION":
            transaction.state = "REJECTED"

        elif event == "TRANSACTION_REQUEST_FAIL":
            transaction.state = "FAILED"

        if event == "TRANSACTION_REQUEST_REJECTION" or event == "TRANSACTION_REQUEST_FAIL":
            balance_object = Balance.objects.get(email=receiver_user, currency_name=currency_object)
            balance_object.amount += transaction.amount
            balance_object.save()

            sent_funds_cryptoshare_wallet_email(str(transaction.email), f"{transaction.state} SENT FUNDS", transaction.currency_name.currency_name ,transaction.amount, "APPROVED", transaction.creation_datetime)
        
        transaction.save()
        
    return HttpResponse(status=200)

@csrf_exempt
# @require_POST
def confirmed_coin_transactions(request):
    if request.method == "GET":
        return redirect('atm_functions:Home')
    elif request.method == "POST":
        if ("Transfer-Encoding" in request.headers) and (request.headers["Transfer-Encoding"] == "chunked"):
            request_reader = request.META.get('wsgi.input')

            # bpayload = request_reader.stream.read1()  # UNCOMMENT FOR LOCAL TESTING ENVIRRONMENT
            bpayload = request_reader.read() #UNCOMMENT FOR PRODUCTION ENVIRONMENT
        else:
            bpayload = request.body

        payload = bpayload.decode("utf-8")

        start = payload.index("{")
        end = payload.rindex("}") + 1

        response = json.loads(payload[start:end])
        
        response_data = response["data"]["item"]

        if response_data["direction"] == "incoming":
            commission = 1 - 0.01

            amount = response_data["amount"]
            transaction_id = response_data["transactionId"]

            # if response_data["blockchain"] == "ethereum":
            #     cryptoapis_client = CryptoApis()
            #     transaction_details = cryptoapis_client.get_transaction_details_by_transactionid(response_data["blockchain"], response_data["network"], transaction_id)
            #     sender_address = transaction_details["senders"][0]["address"]
            # else:
            #     sender_address = response_data["address"]
            
            sender_address = response_data["address"]

            if response_data["blockchain"] == "ethereum":
                sender_address = sender_address.lower()

            # fee = transaction_details["fee"]["amount"]
            # print(sender_address)

            sender_object = Address.objects.get(address=sender_address)
            if response_data["network"] == "ropsten":
                currency_symbol_object = Cryptocurrency.objects.get(currency_name="ethereum_ropsten")
            else:
                try:
                    currency_symbol_object = Cryptocurrency.objects.get(symbol=response_data["unit"])
                except:
                    return HttpResponse("Webhook received!")
            
            sender_currency_balance = Balance.objects.get(email=sender_object.email, currency_name=currency_symbol_object)
            
            sender_currency_balance.amount += Decimal(amount) * Decimal(commission)
            sender_currency_balance.save()
            try:
                transactionA = TransactionA(transaction_id=transaction_id, email=sender_object.email, address=sender_object, currency_name=currency_symbol_object, transaction_type="DEPOSIT", state="APPROVED",amount=amount)
                transactionA.save()
            except:
                sender_currency_balance.amount -= Decimal(amount) * Decimal(commission)
                sender_currency_balance.save()
                return HttpResponse("Webhook received!")

            tx_currency = {
                "currency_name": currency_symbol_object.currency_name,
                "symbol": currency_symbol_object.symbol,
            }

            transaction_intern_id = str(transactionA.id_a) + "|" + transaction_id 
            creation_date = timezone.now()
            deposit_funds_email(str(sender_object.email), transaction_intern_id, response_data["blockchain"], response_data["network"] ,amount, tx_currency, sender_address, creation_date)

            sender_object.expiration_datetime = None
            sender_object.save()

            calculate_credit_grade(sender_object.email)

        # print(response)
        # print(payload.decode("utf-8"))
        return HttpResponse("Webhook received!")

    return HttpResponse(status=200)

@csrf_exempt
def confirmed_token_transactions(request):
    if request.method == "GET":
        return redirect('atm_functions:Home')
    elif request.method == "POST":

        # ETHEREUM_DEPOSIT_ADDRESS = "0x70568e1a620468a49136aee7febd357bb9469b2c"
        commission = 1 - 0.01

        if ("Transfer-Encoding" in request.headers) and (request.headers["Transfer-Encoding"] == "chunked"):
            request_reader = request.META.get('wsgi.input')

            # bpayload = request_reader.stream.read1()  # UNCOMMENT FOR LOCAL TESTING ENVIRRONMENT
            bpayload = request_reader.read() #UNCOMMENT FOR PRODUCTION ENVIRONMENT
        else:
            bpayload = request.body

        payload = bpayload.decode("utf-8")

        start = payload.index("{")
        end = payload.rindex("}") + 1

        response = json.loads(payload[start:end])
        response_data = response["data"]["item"]

        blockchain = response_data["blockchain"]
        transaction_id = response_data["transactionId"]

        token_info = response_data["token"]
        amount = token_info["amount"]
        token_symbol = token_info["symbol"]

        # cryptoapis_client = CryptoApis()
        # transaction_details = cryptoapis_client.get_transaction_details_by_transactionid(response_data["blockchain"], response_data["network"], transaction_id)
        # sender_address = transaction_details["senders"][0]["address"]
        sender_address = response_data["address"]


        sender_object = Address.objects.get(address=sender_address)
        currency_symbol_object = Cryptocurrency.objects.get(symbol=token_symbol, blockchain=blockchain)

        try:
            sender_currency_balance = Balance.objects.get(email=sender_object.email, currency_name=currency_symbol_object)
        except:
            sender_currency_balance = Balance(currency_name=currency_symbol_object, email=sender_object.email, amount=0)
        
        sender_currency_balance.amount += Decimal(amount) * Decimal(commission)
        sender_currency_balance.save()
        try:
            transactionA = TransactionA(transaction_id=transaction_id, email=sender_object.email, address=sender_object, currency_name=currency_symbol_object, transaction_type="DEPOSIT", state="APPROVED",amount=amount)
            transactionA.save()
        except:
            sender_currency_balance.amount -= Decimal(amount) * Decimal(commission)
            sender_currency_balance.save()
            return HttpResponse("Webhook received!")

        tx_currency = {
            "currency_name": currency_symbol_object.currency_name,
            "symbol": currency_symbol_object.symbol,
        }

        transaction_intern_id = str(transactionA.id_a) + "|" + transaction_id 
        creation_date = timezone.now()
        deposit_funds_email(str(sender_object.email), transaction_intern_id, response_data["blockchain"], response_data["network"] ,amount, tx_currency, sender_address, creation_date)

        # print(response)
        # print(payload.decode("utf-8"))
        return HttpResponse("Webhook received!")





    return HttpResponse(status=200)


@csrf_exempt
def test_receiver(request):


    test_email("albertonavarreteramirez@gmail.com")

    
    return HttpResponse(status=200)