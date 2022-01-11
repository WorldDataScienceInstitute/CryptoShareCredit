from time import timezone
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.utils import timezone
from .models import User
from decimal import Decimal
from atm_functions.models import Account, Address, Balance, Cryptocurrency, TransactionA, TransactionB
from common.utils import currency_list
from common.emails import transaction_email_sender
from common.cryptoapis import CryptoApis
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
                    accounts[account['currency']] = account['balance']['amount']
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

        #---------------------- CRYPTOAPIS ----------------------#
        cryptoapis_balances = Balance.objects.filter(email=request.user)

        context = {
            'balance': balance,
            'balance_conv': balance_conv,
            'currency': current_currency,
            'name': name,
            'wallet_conn': wallet_conn,
            'accounts': accounts,
            'cryptoapis_balances': cryptoapis_balances
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

    currencies = Balance.objects.filter(email=request.user).values("currency_name")
    #Get all wallet addresses from Cryptocurrency table that match currency_name field in currencies variable
    addresses = Cryptocurrency.objects.filter(currency_name__in=currencies)

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
    return render(request, 'borrow_selection.html', context)

def borrow_crypto(request):
    if not request.user.is_authenticated:
        return redirect('authentication:Home')
    auth_confirmation = True


    lend_offers = TransactionB.objects.filter(transaction_type="LEND", state="OPEN")

    context = {
        "authConfirmation": auth_confirmation,
        "lend_offers": lend_offers
    }

    return render(request, 'borrow_crypto.html', context)

def lend_money(request):
    if request.user.is_authenticated:
        u = User.objects.get(pk=request.user.pk)
        name = u.first_name
    else:
        name = None
    context = {'name': name}
    return render(request, 'lend_selection.html', context)

def lend_crypto(request):
    if not request.user.is_authenticated:
        return redirect('authentication:Home')
    auth_confirmation = True


    # borrow_offers = TransactionB.objects.filter(transaction_type="BORROW", state="OPEN")
    borrow_offers = TransactionB.objects.exclude(emitter=request.user).filter(transaction_type="BORROW", state="OPEN")
    # table1.objects.exclude(table2=some_param)

    context = {
        "authConfirmation": auth_confirmation,
        "borrow_offers": borrow_offers
    }

    return render(request, 'lend_crypto.html', context)

def lend_offer(request):
    if not request.user.is_authenticated:
        return redirect('authentication:Home')
    auth_confirmation = True
    context = {
        "authConfirmation": auth_confirmation
    }

    transaction_primary_id = request.GET.get('id','')

    if request.method == 'GET':
        if not transaction_primary_id:
            return redirect('atm_functions:LendMoney')
        
        transaction = TransactionB.objects.get(pk=transaction_primary_id)
        context['offer'] = transaction

        return render(request, 'lend_offer.html', context)
    
    if request.method == 'POST':
        if not transaction_primary_id:
            return HttpResponse(status=400)
        
        transaction = TransactionB.objects.get(pk=transaction_primary_id)

        balance_usdc = Balance.objects.get(email=request.user, currency_name=transaction.currency_name)
        # print(balance_usdc)
        if balance_usdc.amount < transaction.amount:
            messages.info(request, f"Insufficient balance. You can only borrow up to {balance_usdc.amount} {transaction.currency_name}.")
            return redirect('atm_functions:LendMoney')
        
        balance_usdc.amount -= transaction.amount
        balance_usdc.save()

        transaction.state = "IN PROGRESS"
        transaction.start_datetime = timezone.now()
        transaction.receptor = request.user

        transaction.save()

        messages.info(request, f"The offer with ID: {transaction.id_b} has been started.")
        return redirect('atm_functions:LendMoney')

    return render(request, 'lend_crypto.html', context)

def create_borrowing_offer(request):
    if not request.user.is_authenticated:
        return redirect('authentication:Home')
    auth_confirmation = True

    balances = Balance.objects.filter(email=request.user)
    currencies = Cryptocurrency.objects.all()

    # print(balances)
    context = {
        "authConfirmation": auth_confirmation,
        "currencies": currencies,
        "balances": balances,
        "exchange_rates": []
    }

    if request.method == 'GET':
        for balance in balances:
            if balance.currency_name.currency_name == "TEST_COIN":
                rate = {
                    "currency_name": balance.currency_name.currency_name,
                    "symbol": balance.currency_name.symbol,
                    "exchange_rate": 1
                }
                context["exchange_rates"].append(rate)
                continue
            elif balance.currency_name.currency_name == "ethereum_ropsten":
                balance.currency_name.symbol = "ETH"

            cryptoapis_client = CryptoApis()
            exchange_rate = cryptoapis_client.get_exchange_rate_by_symbols(balance.currency_name.symbol, "USD")["rate"]
            rate = {
                "currency_name": balance.currency_name.currency_name,
                "symbol": balance.currency_name.symbol,
                "exchange_rate": round(float(exchange_rate), 2)
                }
            context["exchange_rates"].append(rate)


        

        return render(request, 'create_borrowing_offer.html', context)


    if request.method == 'POST':
        currency = request.POST.get('currency').split(" ")[1]
        amount = int(request.POST.get('currency_amount'))
        currency_collateral = request.POST.get('currency_collateral').split(" ")[1]
        amount_collateral = request.POST.get('currency_amount_collateral')
        interest_rate = request.POST.get('interest_rate')

        currency_object = Cryptocurrency.objects.get(currency_name=currency)
        currency__collateral_object = Cryptocurrency.objects.get(currency_name=currency_collateral)

        collateral_balance = Balance.objects.get(email=request.user, currency_name=currency__collateral_object)
        if collateral_balance.amount < float(amount_collateral):
            messages.info(request, f"Insufficient collateral balance. You can only borrow up to {collateral_balance.amount} {currency_collateral}.")
            return redirect('atm_functions:BorrowMoney')

        collateral_balance.amount -= Decimal(float(amount_collateral))
        collateral_balance.save()

        transaction_counter = TransactionB.objects.filter(emitter=request.user).count()
        transaction_type = "BORROW"
        transaction_id = f"{str(request.user)}|{transaction_type}|{transaction_counter}|{currency}|{amount}|{currency_collateral}|{amount_collateral}|{interest_rate}"

        # print(transaction_id)

        transaction_b = TransactionB(transaction_id=transaction_id, emitter=request.user, currency_name = currency_object, currency_name_collateral = currency__collateral_object, transaction_type=transaction_type, state="OPEN", amount=amount, amount_collateral=amount_collateral, interest_rate=interest_rate)
        transaction_b.save()

        #Missing to check if the user has enough money to make the transaction - Ready
        #Missing to substract the amount from the user's balance - Ready
        
        #Missing to create a formal redirect page

        messages.success(request, "Your borrowing offer has been created")
        # print("Transaction B created")

    

    return render(request, 'create_borrowing_offer.html', context)


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

        address = form_response["address"].lower()
        currency_name = form_response["currency"]
        currency_object = Cryptocurrency.objects.get(currency_name=currency_name)

        newAddress = Address(address=address, email=email_object, currency_name=currency_object)
        newAddress.save()

        #Check if there is already a balance with that currency name for that email
        balance_exists = Balance.objects.filter(email=email_object, currency_name=currency_object)
        if not balance_exists:
            # print("Balance does not exist")
            newBalance = Balance(email=email_object, currency_name=currency_object, amount = 0)
            newBalance.save()


        messages.info(request, "Address registered successfully.")


        # addresses = Address.objects.all()
        # print(addresses)
        
    #USDC, USDT, DAI, LITECOIN, BITCOIN, BITCOIN CASH, ETHEREUM, CARDANO
    return render(request, 'register_address.html', context)

    # return HttpResponse(status=200)

@csrf_exempt
# @require_POST
def confirmed_transactions(request):
    if request.method == 'GET':
        return redirect('atm_functions:CheckBalance')
    elif request.method == 'POST':
        request_reader =request.META.get('wsgi.input')

        # bpayload = request_reader.stream.read1()  # UNCOMMENT FOR LOCAL TESTING
        bpayload = request_reader.read() #UNCOMMENT FOR PRODUCTION
        payload = bpayload.decode("utf-8")

        start = payload.index("{")
        end = payload.rindex("}") + 1

        response = json.loads(payload[start:end])
        
        response_data = response["data"]["item"]

        amount = response_data["amount"]
        transaction_id = response_data["transactionId"]

        cryptoapis_client = CryptoApis()
        transaction_details = cryptoapis_client.get_transaction_details_by_transactionid(response_data["blockchain"], response_data["network"], transaction_id)
        sender_address = transaction_details["senders"][0]["address"].lower()
        # fee = transaction_details["fee"]["amount"]
        # print(sender_address)

        sender_object = Address.objects.get(address=sender_address)
        if response_data["network"] == "ropsten":
            currency_symbol_object = Cryptocurrency.objects.get(currency_name="ethereum_ropsten")
        else:
            currency_symbol_object = Cryptocurrency.objects.get(symbol=response_data["unit"])
        sender_currency_balance = Balance.objects.get(email=sender_object.email, currency_name=currency_symbol_object)
        
        sender_currency_balance.amount += Decimal(amount)
        sender_currency_balance.save()

        transactionA = TransactionA(transaction_id=transaction_id, email=sender_object.email, address=sender_object, currency_name=currency_symbol_object, transaction_type="DEPOSIT", state="APPROVED",amount=amount)
        transactionA.save()

        # print(response)
        
        # print(payload.decode("utf-8"))
        return HttpResponse("Webhook received!")

    return HttpResponse(status=200)

@csrf_exempt
def test_receiver(request):
    request_reader =request.META.get('wsgi.input')

    # data = {
    #     "request": str(dir(request_reader)),
    #     "request_dict": str(request_reader.__dict__),
    #     "buf_dir": str(dir(request_reader.buf)),
    #     "buf_dict": str(request_reader.buf.__dict__),
    #     "reader_dir": str(dir(request_reader.reader)),
    #     "reader_dict": str(request_reader.reader.__dict__)
    # }


    # print(str(dir(request_reader)))
    
    bpayload = request_reader.read()
    payload = bpayload.decode("utf-8")

    start = payload.index("{")
    end = payload.rindex("}") + 1

    response = json.loads(payload[start:end])
    
    return HttpResponse(str(response))

    # return HttpResponse(str(data))
    # return HttpResponse(str(request_reader.buf.__dict__))