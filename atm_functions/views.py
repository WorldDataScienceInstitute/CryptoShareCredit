from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from .models import User
from django.db.models import F
from atm_functions.models import Account, Address, Cryptocurrency
from common.utils import currency_list
from common.emails import transaction_email_sender
from google_currency import convert
from coinbase.wallet.client import OAuthClient
from coinbase.wallet.error import TwoFactorRequiredError

import os
import requests
import json


def check_balance(request):

    accounts = {}

    if 'wallet_conn' in request.session:
        if request.session['wallet_conn']:
            wallet_conn = request.session['wallet_conn']

            coinbase_client = OAuthClient(
                request.session['access_token'], request.session['refresh_token'])
            all_accounts = coinbase_client.get_accounts()["data"]

            # Get into dict only the accounts that have a balance greater than 0
            for account in all_accounts:
                if float(account['balance']['amount']) > 0:
                    accounts[account['currency']
                             ] = account['balance']['amount']
        else:
            wallet_conn = False
    else:
        wallet_conn = False

    current_currency = request.session['currency'] if 'currency' in request.session else 'USD'
    if request.user.is_authenticated:
        # get account details for user
        u = User.objects.get(pk=request.user.pk)

        # get first name
        name = u.first_name

        # convert balance to user's selected currency
        balance = 0
        if current_currency == 'USD':
            balance_conv = balance
        else:
            balance_conv = 0 if balance == 0 else json.loads(convert('USD', current_currency, balance))['amount']
        context = {
            'balance': balance,
            'balance_conv': balance_conv,
            'currency': current_currency,
            'name': name,
            'wallet_conn': wallet_conn,
            'accounts': accounts
        }
    else:
        context = {
            'name': None,
            'wallet_conn': wallet_conn,
            'accounts': accounts
        }
    return render(request, 'check_balance.html', context)


def withdraw_money(request):
    # set user selected currency
    # if not set, default to USD
    current_currency = request.session['currency'] if 'currency' in request.session else 'USD'

    # check if user is logged in to set authorization level
    if request.user.is_authenticated:
        u = User.objects.get(pk=request.user.pk)
    # test balance for.. testing
    balance = 100
    context = {
        'current_currency': current_currency,
        'currency_dict': currency_list,
        'balance': balance
    }
    if request.method == 'POST':
        withdraw_amt = int(request.POST.get('withdraw'))
        # get user balance
        if balance == 0:
            messages.info(request, "You have no money to withdraw.")
        # get withdrawal amount once user submits

            # check if user is trying to withdraw more than balance
            if withdraw_amt > balance:
                messages.info(request, f"Insufficient balance. You can only withdraw up to {balance} USD.")
                return render(request, 'withdraw_money.html', context)

            # user successfully withdraws money
            else:
                return redirect('atm_functions:TyWithdraw')

    return render(request, 'withdraw_money.html', context)


def deposit_selection(request):

    if request.user.is_authenticated:
        u = User.objects.get(pk=request.user.pk)
        name = u.first_name
    else:
        name = None
    context = {'name': name}
    return render(request, 'deposit_selection.html', context)


def deposit_money(request):
    if request.user.is_authenticated:
        u = User.objects.get(pk=request.user.pk)
        name = u.first_name
    else:
        name = None
    context = {'name': name}
    if request.method == 'POST':
        return redirect('atm_functions:SelectBank', context)
    else:
        return render(request, 'deposit_money.html', context)

def deposit_crypto(request):
    if not request.user.is_authenticated:
        return redirect('authentication:Home')
    auth_confirmation = True

    currencies = Address.objects.filter(email=request.user).values("currency_name")
    #Get all wallet addresses from Cryptocurrency table that match currency_name field in currencies variable
    addresses = Cryptocurrency.objects.filter(currency_name__in=currencies)

    # print(addresses)
    for address in addresses:
        print(address.blockchain)

    context = {
        "authConfirmation": auth_confirmation,
        "addresses": addresses
    }

    return render(request, 'deposit_crypto.html', context)

def bank(request):
    if request.user.is_authenticated:
        u = User.objects.get(pk=request.user.pk)
        name = u.first_name
    else:
        name = None
    context = {'name': name}
    return render(request, 'bank.html', context)


def ty_withdraw(request):
    if request.user.is_authenticated:
        u = User.objects.get(pk=request.user.pk)
        name = u.first_name
    else:
        name = None
    context = {'name': name}
    return render(request, 'ty_withdraw.html', context)


def ty_deposit(request):
    if request.user.is_authenticated:
        u = User.objects.get(pk=request.user.pk)
        name = u.first_name
    else:
        name = None
    context = {'name': name}
    return render(request, 'ty_deposit.html', context)


def borrow_money(request):
    if request.user.is_authenticated:
        u = User.objects.get(pk=request.user.pk)
        name = u.first_name
    else:
        name = None
    context = {'name': name}
    return render(request, 'borrow_money.html', context)


def lend_money(request):
    if request.user.is_authenticated:
        u = User.objects.get(pk=request.user.pk)
        name = u.first_name
    else:
        name = None
    context = {'name': name}
    return render(request, 'lend_money.html', context)


def earn_money(request):
    if request.user.is_authenticated:
        u = User.objects.get(pk=request.user.pk)
        name = u.first_name
    else:
        name = None
    context = {'name': name}
    return render(request, 'earn_money.html', context)


def shop(request):
    if request.user.is_authenticated:
        u = User.objects.get(pk=request.user.pk)
        name = u.first_name
    else:
        name = None
    context = {'name': name}
    return render(request, 'atm_shop.html', context)


def atm_settings(request):
    if request.user.is_authenticated:
        u = User.objects.get(pk=request.user.pk)
        name = u.first_name
    else:
        name = None
    if request.method == 'POST':
        request.session['currency'] = request.POST.get('currency')
        return redirect('atm_functions:CheckBalance')
    context = {
        'currency_list': currency_list,
        'name': name
    }
    return render(request, 'atm_settings.html', context)


def connect_wallet(request):
    if request.session['wallet_conn']:
        messages.info(request, "Your Coinbase account has already been connected.")
        return redirect('atm_functions:CheckBalance')

    if request.user.is_authenticated:
        u = User.objects.get(pk=request.user.pk)
        name = u.first_name
    else:
        name = None
    context = {'name': name}
    # print(request.session['wallet_conn'])

    return render(request, 'connect_wallet.html', context)


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


def disconnect_wallet(request):

    coinbase_client = OAuthClient(
        request.session['access_token'], request.session['refresh_token'])
    coinbase_client.revoke()

    request.session['wallet_conn'] = False
    request.session['access_token'] = None
    request.session['refresh_token'] = None

    return redirect('atm_functions:ConnectWallet')


def send_money(request):

    if not request.session['wallet_conn']:
        # Temporary redirect to connect wallet while CryptoApis implementation is in progress.
        messages.info(
            request, "You must connect your Coinbase account to send money.")
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


def send_money_confirmation(request):

    # request.POST.get('code','')
    form_response = request.POST

    if not form_response:
        return redirect('atm_functions:SendMoney')

    coinbase_client = OAuthClient(request.session['access_token'], request.session['refresh_token'])

    recipient_account = form_response["recipientUser"]
    account_info = form_response["sendingAccount"].split(" ")
    account_id = account_info[0]
    account_currency = account_info[1]
    amount = form_response["sendingAmount"]

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

            transaction_email_sender(sender_email, concept, tx_amount, tx_native_amount, tx_state, creation_date, receiver_email)
            
            return redirect('atm_functions:CheckBalance')
        except Exception as e:
            # print(e)
            messages.error(request, "Invalid authorization code. Please try again.")
            return redirect('atm_functions:SendMoney')

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
            return redirect('atm_functions:CheckBalance')

        except TwoFactorRequiredError:
            context = {
                "recipientUser": recipient_account,
                "sendingAccount": form_response["sendingAccount"],
                "sendingAmount": amount
            }
            messages.info(request, "Two factor authentication required.")
            return render(request, '2fa_token.html', context)
            # return redirect('atm_functions:SendMoney')
        except Exception as e:
            # print(e)
            messages.info(request, "Error sending money. Please try again.")
            return redirect('atm_functions:SendMoney')

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

    pass


def register_address(request):
    if not request.user.is_authenticated:
        return redirect('authentication:Home')

    # print(request.user)

    currencies = Cryptocurrency.objects.all()
    auth_confirmation = True

    context = {'authConfirmation': auth_confirmation, 
                'currencies': currencies
                }

    if request.method == 'GET':
        return render(request, 'register_address.html', context)


    if request.method == 'POST':
        form_response = request.POST
        email_object = request.user
        # email_object = Account.objects.get(user= email)

        address = form_response["address"]
        currency_name = form_response["currency"]
        currency_object = Cryptocurrency.objects.get(currency_name=currency_name)

        newAddress = Address(address=address, email=email_object, currency_name=currency_object)
        newAddress.save()

        # addresses = Address.objects.all()
        # print(addresses)
        
    #USDC, USDT, DAI, LITECOIN, BITCOIN, BITCOIN CASH, ETHEREUM, CARDANO

    print(request)
    return render(request, 'register_address.html', context)

    # return HttpResponse(status=200)

@csrf_exempt
# @require_POST
def confirmed_transactions(request):
    # if request.user.is_authenticated:
    #     u = User.objects.get(pk=request.user.pk)
    #     name = u.first_name
    # else:
    #     return redirect('authentication:Home')
    
    #USDC, USDT, DAI, LITECOIN, BITCOIN, BITCOIN CASH, ETHEREUM, CARDANO
    # form_response = request.POST
    # print(request.META)
    # print(dict(request.POST.items()))
    # print(request.headers)

    # print(dict(request.POST.items()))

    # stream = request.META['wsgi.input']
    # print(stream.read())
    # body = request.body.decode('utf-8')
    # print(body)
    

    # test = request.POST
    # print(test)

    if request.method == 'POST':
        print("Data received from Webhook is: ", request.body)
        return HttpResponse("Webhook received!")
    # print(data)
    # print(form_response["data"])
    return HttpResponse(status=200)