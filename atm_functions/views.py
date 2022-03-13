# from time import timezone
from multiprocessing import context
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Q
from .models import User
from decimal import Decimal
from atm_functions.models import Account, Address, Balance, Cryptocurrency, TransactionA, TransactionB
from common.utils import currency_list
from common.emails import sent_funds_email, sent_funds_cryptoshare_wallet_email, deposit_funds_email
from common.cryptoapis import CryptoApis
from common.aptopayments import AptoPayments
from google_currency import convert
from coinbase.wallet.client import OAuthClient
from coinbase.wallet.error import TwoFactorRequiredError

import hmac
import hashlib

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

def cryptoshare_wallet(request):
    if not request.user.is_authenticated:
        return redirect('authentication:Home')
    auth_confirmation = True

    context = {
        "authConfirmation": auth_confirmation,
        "address_confirmations": [
                                {
                                    "currency_name": "Litecoin",
                                    "blockchain": "litecoin",
                                    "symbol": "LTC",
                                    "has_address": False
                                },
                                {
                                    "currency_name": "Bitcoin Cash",
                                    "blockchain": "bitcoin-cash",
                                    "symbol": "BCH",
                                    "has_address": False
                                },
                                {
                                    "currency_name": "Dash",
                                    "blockchain": "dash",
                                    "symbol": "DASH",
                                    "has_address": False
                                },
                                {
                                    "currency_name": "Zcash",
                                    "blockchain": "zcash",
                                    "symbol": "ZEC",
                                    "has_address": False
                                },
                                {
                                    "currency_name": "XRP",
                                    "blockchain": "xrp",
                                    "symbol": "XRP",
                                    "has_address": False
                                }
                                ]
    }
    
    iframe = request.GET.get('iframe','')
    if iframe:
        context["iframe"] = True

    currencies = Address.objects.filter(email=request.user).values("currency_name")
    currencies_addresses = Address.objects.filter(email=request.user)

    currencies_dict = {}
    for currency in currencies_addresses:
        currencies_dict[currency.currency_name.currency_name] = currency.address
    #Get all wallet addresses from Cryptocurrency table that match currency_name field in currencies variable
    addresses = Cryptocurrency.objects.filter(currency_name__in=currencies)
    context["addresses"] = addresses

    for address in addresses:
        # print(address.__dict__)
        if address.currency_name == "Litecoin":
            address.wallet_address = currencies_dict["Litecoin"]
            context["address_confirmations"][0]["has_address"] = True

        elif address.currency_name == "Bitcoin Cash":
            address.wallet_address = currencies_dict["Bitcoin Cash"]
            context["address_confirmations"][1]["has_address"] = True

        elif address.currency_name == "Dash":
            address.wallet_address = currencies_dict["Dash"]
            context["address_confirmations"][2]["has_address"] = True
        
        elif address.currency_name == "Zcash":
            address.wallet_address = currencies_dict["Zcash"]
            context["address_confirmations"][3]["has_address"] = True
        
        elif address.currency_name == "XRP":
            address.wallet_address = currencies_dict["XRP"]
            context["address_confirmations"][4]["has_address"] = True

    return render(request, 'cryptoshare_wallet.html', context)

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

    iframe = request.GET.get('iframe','')
    if iframe:
        context["iframe"] = True

    return render(request, 'borrow_crypto.html', context)

def borrow_crypto_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('authentication:Home')
    auth_confirmation = True


    context = {
        "authConfirmation": auth_confirmation
    }

    return render(request, 'borrow_crypto_dashboard.html', context)

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

        try:
            balance_usdc = Balance.objects.get(email=request.user, currency_name=transaction.currency_name)
        except:
            messages.info(request, "You do not have a balance in USDC, please make a deposit before accepting a offer.")
            return redirect('atm_functions:LendCrypto')
        # print(balance_usdc)
        if balance_usdc.amount < transaction.amount:
            messages.info(request, f"Insufficient balance. You can only borrow up to {float(balance_usdc.amount)} {transaction.currency_name.currency_name}.")
            return redirect('atm_functions:LendCrypto')
        
        balance_usdc.amount -= transaction.amount
        balance_usdc.save()

        transaction.state = "IN PROGRESS"
        transaction.start_datetime = timezone.now()
        transaction.receptor = request.user

        transaction.save()

        emitter = transaction.emitter
        emitter_balance = Balance.objects.get(email=emitter, currency_name=transaction.currency_name)
        emitter_balance.amount += transaction.amount
        emitter_balance.save()

        messages.info(request, f"The offer with ID: {transaction.id_b} has been started.")
        return redirect('atm_functions:LendMoney')

    return render(request, 'lend_crypto.html', context)

def create_borrowing_offer(request):
    if not request.user.is_authenticated:
        return redirect('authentication:Home')
    auth_confirmation = True

    context = {
        "authConfirmation": auth_confirmation
    }

    iframe = request.GET.get('iframe','')
    if iframe:
        context["iframe"] = True

    if request.method == 'GET':
        context["exchange_rates"] = []

        # currencies = Cryptocurrency.objects.filter(Q(symbol='USDC') | Q(symbol='USDT') | Q(symbol='WBTC'))

        # balances = list(Balance.objects.filter(email=request.user, currency_name__in=currencies))

        # if len(balances) != 3:
        #     missing_currencies = {'USDC', 'USDT', 'WBTC'} - {balance.currency_name.symbol for balance in balances}

        #     for currency in missing_currencies:
        #         balance = Balance(email=request.user, currency_name=Cryptocurrency.objects.get(symbol=currency), amount=0)
        #         balances.append(balance)
                
        # # context["currencies"] = currencies
        # context["balances"] = balances

        cryptoapis_client = CryptoApis()

        # for balance in balances:
        #     if balance.currency_name.currency_name == "TEST_COIN":
        #         rate = {
        #             "currency_name": balance.currency_name.currency_name,
        #             "symbol": balance.currency_name.symbol,
        #             "exchange_rate": 1
        #         }
        #         context["exchange_rates"].append(rate)
        #         continue
        #     elif balance.currency_name.currency_name == "ethereum_ropsten":
        #         balance.currency_name.symbol = "ETH"

        #     exchange_rate = cryptoapis_client.get_exchange_rate_by_symbols(balance.currency_name.symbol, "USD")["rate"]
        #     rate = {
        #         "currency_name": balance.currency_name.currency_name,
        #         "symbol": balance.currency_name.symbol,
        #         "exchange_rate": round(float(exchange_rate), 2)
        #         }
        #     context["exchange_rates"].append(rate)

        exchange_rate_ltc = cryptoapis_client.get_exchange_rate_by_symbols("LTC", "USD")["rate"]
        rate_ltc = {
            "currency_name": "Litecoin",
            "symbol": "LTC",
            "exchange_rate": round(float(exchange_rate_ltc), 2)
        }

        exchange_rate_bch = cryptoapis_client.get_exchange_rate_by_symbols("BCH", "USD")["rate"]
        rate_bch = {
            "currency_name": "Bitcoin Cash",
            "symbol": "BCH",
            "exchange_rate": round(float(exchange_rate_bch), 2)
        }

        exchange_rate_dash = cryptoapis_client.get_exchange_rate_by_symbols("DASH", "USD")["rate"]
        rate_dash = {
            "currency_name": "Dash",
            "symbol": "DASH",
            "exchange_rate": round(float(exchange_rate_dash), 2)
        }

        exchange_rate_zec = cryptoapis_client.get_exchange_rate_by_symbols("ZEC", "USD")["rate"]
        rate_zec = {
            "currency_name": "Zcash",
            "symbol": "ZEC",
            "exchange_rate": round(float(exchange_rate_zec), 2)
        }

        exchange_rate_xrp = cryptoapis_client.get_exchange_rate_by_symbols("XRP", "USD")["rate"]
        rate_xrp = {
            "currency_name": "XRP",
            "symbol": "XRP",
            "exchange_rate": round(float(exchange_rate_xrp), 2)
        }

        context["exchange_rates"].append(rate_ltc)
        context["exchange_rates"].append(rate_bch)
        context["exchange_rates"].append(rate_dash)
        context["exchange_rates"].append(rate_zec)        
        context["exchange_rates"].append(rate_xrp)        

        return render(request, 'create_borrowing_offer.html', context)

    elif request.method == 'POST':
        currency = request.POST.get('currency').split(" ")[0]
        amount = float(request.POST.get('currency_amount'))
        currency_collateral = request.POST.get('currency_collateral').split(" ")[0]
        amount_collateral = request.POST.get('currency_amount_collateral')
        interest_rate = request.POST.get('interest_rate')

        if currency_collateral == "NotSelected":
            messages.info(request, "Please select a collateral currency.")
            return redirect('atm_functions:CreateBorrowingOffer')
        
        if amount_collateral == "":
            messages.info(request, "Collateral amount invalid, please try again")
            return redirect('atm_functions:CreateBorrowingOffer')

        currency_object = Cryptocurrency.objects.get(symbol=currency)
        currency_collateral_object = Cryptocurrency.objects.get(symbol=currency_collateral)

        try:
            currency_balance = Balance.objects.get(email=request.user, currency_name=currency_object)
        except:
            new_currency_balance = Balance(email=request.user, currency_name=currency_object, amount = 0)
            new_currency_balance.save()

        try:
            collateral_balance = Balance.objects.get(email=request.user, currency_name=currency_collateral_object)
        except:
            collateral_balance = Balance(email=request.user, currency_name=currency_collateral_object, amount = 0)
        # print(collateral_balance.__dict__, amount_collateral)
        if collateral_balance.amount < float(amount_collateral):
            messages.info(request, f"Insufficient collateral balance. You can only borrow up to {float(collateral_balance.amount)} {currency_collateral}.")
            return redirect('atm_functions:CreateBorrowingOffer')

        collateral_balance.amount -= Decimal(float(amount_collateral))
        collateral_balance.save()

        transaction_counter = TransactionB.objects.filter(emitter=request.user).count()
        transaction_type = "BORROW"
        transaction_id = f"{str(request.user)}|{transaction_type}|{transaction_counter}|{currency}|{amount}|{currency_collateral}|{amount_collateral}|{interest_rate}"

        # print(transaction_id)

        transaction_b = TransactionB(transaction_id=transaction_id, emitter=request.user, currency_name = currency_object, currency_name_collateral = currency_collateral_object, transaction_type=transaction_type, state="OPEN", amount=amount, amount_collateral=amount_collateral, interest_rate=interest_rate)
        transaction_b.save()
        
        #Missing to create a formal redirect page

        messages.success(request, "Your borrowing offer has been created")
        # print("Transaction B created")
        return redirect('atm_functions:LendCrypto')

    return render(request, 'create_borrowing_offer.html', context)

def remove_borrowing_offer(request):
    if request.method == 'POST':
        offer_id = request.POST.get('offerID')

        offer = TransactionB.objects.get(id_b=offer_id)

        if offer.state != "OPEN":
            # messages.error(request, "Something went wrong, please try again later")
            return HttpResponse(status=405)
        
        emitter_id = offer.emitter_id
        emitter_object = User.objects.get(pk=emitter_id)

        currency_collateral_object = offer.currency_name_collateral

        balance_object = Balance.objects.get(email=emitter_object, currency_name=currency_collateral_object)
        balance_object.amount += offer.amount_collateral
        balance_object.save()
        
        offer.state = "CANCELED"
        offer.save()
        # print(offer.__dict__)
        # messages.success(request, "Your borrowing offer has been removed")

        return HttpResponse(status=200)
    return redirect('atm_functions:MyTransactions')

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
    if not request.user.is_authenticated:
        return redirect('authentication:Home')

    context = {}
    
    return render(request, 'send_selection.html', context)

def send_cryptoshare_wallet(request):
    if not request.user.is_authenticated:
        return redirect('authentication:Home')
    
    context = {}

    messages.info(request, "XRP, Ethereum, and ERC-20 tokens are currently not supported for sending funds.")

    balances = Balance.objects.filter(email=request.user)
    context['balances'] = balances
    
    return render(request,'send_cryptoshare_wallet.html', context)

def send_coinbase_wallet(request):

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
    form_response = request.POST

    if not form_response:
        return redirect('atm_functions:SendMoney')

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

    elif wallet_confirmation == "cryptoshare":
        wallet_currencies = {
                            "Litecoin": True,
                            "Dash": True,
                            "Zcash": True,
                            "Bitcoin Cash": True
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


        amount = form_response["sendingAmount"]
        recipient_address = form_response["recipientUser"]

        currency_object = Cryptocurrency.objects.get(currency_name=sending_currency)
        balance_object = Balance.objects.get(email=request.user, currency_name=currency_object)
        sending_address_object = Address.objects.get(currency_name=currency_object, email=request.user)

        if balance_object.amount < float(amount):
            messages.error(request, "Insufficient funds.")
            return redirect('atm_functions:SendCryptoShareWallet')

        cryptoapis_client = CryptoApis()

        is_valid_address = cryptoapis_client.is_valid_address(sending_blockchain, "mainnet", recipient_address)
        if not is_valid_address:
            messages.info(request, "Invalid address. Please try again.")
            return redirect('atm_functions:SendCryptoShareWallet')

        # if sending_currency in wallet_currencies:
        #     transaction_response = cryptoapis_client.generate_coins_transaction_from_wallet(sending_blockchain, "mainnet", recipient_address, amount)
        #     print(request)
        # elif sending_currency in address_currencies:
        transaction_response = cryptoapis_client.generate_coins_transaction_from_address(sending_blockchain, "mainnet",sending_address_object.address ,recipient_address, amount)
        # print(request)

        # total_transaction_amount = transaction_response["totalTransactionAmount"]
        total_transaction_amount = transaction_response["recipients"][0]["amount"]
        transaction_id = transaction_response["transactionRequestId"]

        balance_object.amount -= Decimal(total_transaction_amount)
        balance_object.save()

        transaction_a = TransactionA(transaction_id=transaction_id, email=request.user, address=sending_address_object, currency_name=currency_object, transaction_type="WITHDRAWAL", state="PENDING", amount=amount, internal_state="WAITING_FOR_APPROVAL")
        transaction_a.save()
        # print(sending_blockchain, sending_currency, amount, recipient_address)

        sent_funds_cryptoshare_wallet_email(str(transaction_a.email), "SENT FUNDS REQUEST", transaction_a.currency_name.currency_name ,transaction_a.amount, "APPROVED", transaction_a.creation_datetime, receiver=recipient_address)

        messages.success(request, "Your withdrawal request has been created")

        return redirect('atm_functions:CheckBalance')
    else:
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

def my_transactions(request):
    if not request.user.is_authenticated:
        return redirect('authentication:Home')
    auth_confirmation = True
    
    #Transactions
    transactions = TransactionA.objects.filter(email=request.user)

    #Loans
    opened_offers = TransactionB.objects.filter(emitter = request.user, state = "OPEN")
    accepted_offers = TransactionB.objects.filter(Q(receptor=request.user) | Q(emitter=request.user), state = "IN PROGRESS") 

    context = {
            "authConfirmation": auth_confirmation,
            "transactions": transactions,
            "opened_offers": opened_offers,
            "accepted_offers": accepted_offers
            }

    return render(request, 'my_transactions.html', context)

# <--------------------------------  CURRENTLY NOT ACTIVE --------------------------------------------->
# <--------------------------------  CURRENTLY NOT ACTIVE --------------------------------------------->
def my_loans(request):
    if not request.user.is_authenticated:
        return redirect('authentication:Home')
    auth_confirmation = True

    # loans = TransactionB.objects.filter(Q(emmiter = request.user) | Q(receiver = request.user))
    opened_offers = TransactionB.objects.filter(emitter = request.user, state = "OPEN")
    accepted_offers = TransactionB.objects.filter(Q(receptor=request.user) | Q(emitter=request.user), state = "IN PROGRESS") 


    context = {
            "authConfirmation": auth_confirmation,
            "opened_offers": opened_offers,
            "accepted_offers": accepted_offers
            }

    return render(request, 'my_loans.html', context)
# <--------------------------------  CURRENTLY NOT ACTIVE --------------------------------------------->
# <--------------------------------  CURRENTLY NOT ACTIVE --------------------------------------------->

def register_address(request):
    if not request.user.is_authenticated:
        return redirect('authentication:Home')


    currencies = Cryptocurrency.objects.all()
    auth_confirmation = True

    context = {'authConfirmation': auth_confirmation, 
                'currencies': currencies
                }

    iframe = request.GET.get('iframe','')
    if iframe:
        context["iframe"] = True


    if request.method == 'GET':
        return render(request, 'register_address.html', context)


    if request.method == 'POST':
        form_response = request.POST
        email_object = request.user
        # email_object = Account.objects.get(user= email)

        address = form_response["address"]
        # address = form_response["address"].lower()

        if address.isspace():
            messages.info(request, "Invalid address. Please try again.")
            return redirect('atm_functions:RegisterAddress')

        currency_details = form_response["currency"].split("|")
        currency_name = currency_details[0]
        currency_blockchain = currency_details[1]
        currency_network = currency_details[2]

        if currency_blockchain == "ethereum":
            address = address.lower()

        cryptoapis_client = CryptoApis()
        # print(f"Blockchain {currency_blockchain} , Network {currency_network} , Address {address}")
        is_valid_address = cryptoapis_client.is_valid_address(currency_blockchain, currency_network, address)
        if not is_valid_address:
            messages.info(request, "Invalid address. Please try again.")
            return redirect('atm_functions:RegisterAddress')

        currency_object = Cryptocurrency.objects.get(currency_name=currency_name)

        newAddress = Address(address=address, email=email_object, currency_name=currency_object)
        newAddress.save()

        #Check if there is already a balance with that currency name for that email
        balance_exists = Balance.objects.filter(email=email_object, currency_name=currency_object)
        if not balance_exists:
            # print("Balance does not exist")
            new_balance = Balance(email=email_object, currency_name=currency_object, amount = 0)
            new_balance.save()


        messages.info(request, "Address registered successfully.")


        # addresses = Address.objects.all()
        # print(addresses)
        
    #USDC, USDT, DAI, LITECOIN, BITCOIN, BITCOIN CASH, ETHEREUM, CARDANO
    return render(request, 'register_address.html', context)

def generate_address(request):
    blockchain = request.GET.get('blockchain','')
    network = request.GET.get('network','')
    currency = request.GET.get('currency','')

    currency_object = Cryptocurrency.objects.get(currency_name=currency)
    email_object = request.user

    if not blockchain or not network or not currency:
        messages.info(request, "Invalid option, please try again.")
        return redirect('atm_functions:CryptoShareWallet')
    
    #Check if there is already an address for that currency name for that email
    address_exists = Address.objects.filter(email=request.user, currency_name=currency_object)
    if address_exists:
        messages.info(request, "Address already exists.")
        return redirect('atm_functions:CryptoShareWallet')

    #Check if there is already a balance with that currency name for that email
    balance_exists = Balance.objects.filter(email=email_object, currency_name=currency_object)
    if not balance_exists:
        new_balance = Balance(email=email_object, currency_name=currency_object, amount = 0)
        new_balance.save()
    
    available_addresses = Address.objects.filter(currency_name=currency_object, email=None)
    if len(available_addresses) != 0:
        address = available_addresses[0]
        address.email = request.user
        address.save()
        # print(address)
        messages.info(request, "Address generated successfully.")
        return redirect('atm_functions:CryptoShareWallet')


    cryptoapis_client = CryptoApis()

    # Get current number of addresses for that currency
    number_of_addresses = Address.objects.filter(currency_name=currency).count()

    try:
        deposit_address = cryptoapis_client.generate_deposit_address(blockchain, network, number_of_addresses)
    except:
        messages.info(request, "Error generating address. Please try again.")
        return redirect('atm_functions:CryptoShareWallet')

    if blockchain != "xrp":
        newAddress = Address(address=deposit_address, email=email_object, currency_name=currency_object)
    else:
        newAddress = Address(address=deposit_address, email=email_object, currency_name=currency_object, expiration_datetime = None)
    newAddress.save()

    try:
        cryptoapis_client.generate_coin_subscription(blockchain, network, deposit_address)
    except:
        newAddress.email = None
        newAddress.save()
        messages.info(request, "Error generating address, please contact support")
        return redirect('atm_functions:CryptoShareWallet')

    
    messages.info(request, "Address generated successfully.")

    return redirect('atm_functions:CryptoShareWallet')

    # return HttpResponse(status=200)

def card_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('authentication:Home')

    auth_confirmation = True
    context = {"authConfirmation": auth_confirmation,
                "start_auth": False,
                "finish_auth": False,
                "has_card": False,
                "aptopayments_auth_info": {
                                            "verification_id": "None"
                }
            }
    
    if "aptopayments_verification_id" in request.session:
        context["aptopayments_auth_info"]["verification_id"] = request.session["aptopayments_verification_id"]
    else:
        if request.POST.get("start_auth",""):
            country_code = request.POST["country_code"]
            phone_number = request.POST["phone_number"]

            aptopayments_client = AptoPayments()

            verification = aptopayments_client.start_phone_verification_process(country_code, phone_number)
            try:
                if verification["status"] != "pending":
                    messages.info(request, "Error starting verification process. Please try again.")
                    return redirect('atm_functions:CardDashboard')
            except:
                messages.info(request, "Error starting verification process. Please try again.")
                return redirect('atm_functions:CardDashboard')

            context["start_auth"] = True
            context["aptopayments_auth_info"]["verification_id"] = verification["verification_id"]        


        elif request.POST.get("finish_auth",""):
            code = request.POST["code"]
            verification_id = request.POST["verification_id"]

            aptopayments_client = AptoPayments()

            complete_verification = aptopayments_client.complete_verification_process(code, verification_id)

            try:
                if complete_verification["status"] != "passed":
                    messages.info(request, "Error finishing verification process. Please try again.")
                    return redirect('atm_functions:CardDashboard')
            except:
                messages.error(request, "Error finishing verification process. Please try again.")
                return redirect('atm_functions:CardDashboard')

            print(complete_verification)

            login_data = aptopayments_client.login_user(verification_id)
            print(login_data)

            request.session["aptopayments_verification_id"] = verification_id
            context["aptopayments_auth_info"]["verification_id"] = verification_id


    return render(request, 'card_dashboard.html', context)

def aptopayments_create_user(request):
    if not request.user.is_authenticated:
        return redirect('authentication:Home')

    context = {"authConfirmation": True}

    iframe = request.GET.get('iframe','')
    if iframe:
        context["iframe"] = True
        
        verification_id = request.GET.get('verification_id','')
        context["verification_id"] = verification_id

    if request.method == "GET":

        return render(request, 'aptopayments_create_user.html', context)
    
    if request.method == "POST":
        verification_id = request.POST.get('verification_id','')

        first_name = request.POST.get('first_name','')
        last_name = request.POST.get('last_name','')
        email = request.POST.get('email','')
        country_code = request.POST.get('country_code','')
        phone_number = request.POST.get('phone_number','')
        birthday = request.POST.get('birthday','')
        street_address = request.POST.get('street_one','')
        street_address_2 = request.POST.get('street_two','')
        city = request.POST.get('city','')
        state = request.POST.get('state','')
        postal_code = request.POST.get('postal_code','')
        country = request.POST.get('country','')

        aptopayments_client = AptoPayments()

        print(verification_id, first_name, last_name, email, country_code, phone_number, birthday, street_address, street_address_2, city, state, postal_code, country)

        try:
            request_test = aptopayments_client.create_user(email, verification_id, country_code, phone_number, birthday, first_name, last_name, street_address, street_address_2, city, state, postal_code, country)
        except:
            print("ERROOOOOOOR")
        
        print(request_test)

        html = """
            <!DOCTYPE html>
            <head>
            <title>Form submitted</title>
            <script type='text/javascript'>window.parent.location.href += "?test=Testing";</script>
            <script type='text/javascript'>window.parent.location.reload();</script>
            </head>
            <body></body></html>
            """
        return HttpResponse(html)


    return render(request, 'aptopayments_create_user.html', context)

@csrf_exempt
def confirmations_coin_transactions(request):
    if request.method == 'GET':
        return redirect('authentication:Home')
    
    elif request.method == 'POST':
        request_reader = request.META.get('wsgi.input')
        # print(request.headers)

        bpayload = request_reader.stream.read1()  # UNCOMMENT FOR LOCAL TESTING ENVIRRONMENT
        # bpayload = request_reader.read() #UNCOMMENT FOR PRODUCTION ENVIRONMENT

        payload = bpayload.decode("utf-8")

        start = payload.index("{")
        end = payload.rindex("}") + 1

        response = json.loads(payload[start:end])

        reference_id = response["reference_Id"]
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
        
    return HttpResponse(status=200)

@csrf_exempt
# @require_POST
def confirmed_coin_transactions(request):
    if request.method == 'GET':
        return redirect('atm_functions:CheckBalance')
    elif request.method == 'POST':
        request_reader = request.META.get('wsgi.input')
        # print(request.headers)

        # bpayload = request_reader.stream.read1()  # UNCOMMENT FOR LOCAL TESTING ENVIRRONMENT
        bpayload = request_reader.read() #UNCOMMENT FOR PRODUCTION ENVIRONMENT

        payload = bpayload.decode("utf-8")

        start = payload.index("{")
        end = payload.rindex("}") + 1

        response = json.loads(payload[start:end])
        
        response_data = response["data"]["item"]

        if response_data["direction"] == "incoming":
            amount = response_data["amount"]
            transaction_id = response_data["transactionId"]

            if response_data["blockchain"] == "ethereum":
                cryptoapis_client = CryptoApis()
                transaction_details = cryptoapis_client.get_transaction_details_by_transactionid(response_data["blockchain"], response_data["network"], transaction_id)
                sender_address = transaction_details["senders"][0]["address"]
            else:
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
            
            sender_currency_balance.amount += Decimal(amount)
            sender_currency_balance.save()
            try:
                transactionA = TransactionA(transaction_id=transaction_id, email=sender_object.email, address=sender_object, currency_name=currency_symbol_object, transaction_type="DEPOSIT", state="APPROVED",amount=amount)
                transactionA.save()
            except:
                sender_currency_balance.amount -= Decimal(amount)
                sender_currency_balance.save()
                return HttpResponse("Webhook received!")

            tx_currency = {
                "currency_name": currency_symbol_object.currency_name,
                "symbol": currency_symbol_object.symbol,
            }

            transaction_intern_id = str(transactionA.id_a) + "|" + transaction_id 
            creation_date = timezone.now()
            deposit_funds_email(str(sender_object.email), transaction_intern_id, response_data["blockchain"], response_data["network"] ,amount, tx_currency, sender_address, creation_date)

            if response_data["blockchain"] != "ethereum" and response_data["blockchain"] != "xrp":
                sender_object.email = None
                sender_object.save()
        # print(response)
        # print(payload.decode("utf-8"))
        return HttpResponse("Webhook received!")

    return HttpResponse(status=200)

@csrf_exempt
def confirmed_token_transactions(request):
    if request.method == 'GET':
        return redirect('atm_functions:CheckBalance')
    elif request.method == 'POST':

        ETHEREUM_DEPOSIT_ADDRESS = "0x70568e1a620468a49136aee7febd357bb9469b2c"
        request_reader =request.META.get('wsgi.input')

        # print(request.headers)

        # bpayload = request_reader.stream.read1()  # UNCOMMENT FOR LOCAL TESTING ENVIRRONMENT
        bpayload = request_reader.read() #UNCOMMENT FOR PRODUCTION ENVIRONMENT

        payload = bpayload.decode("utf-8")

        start = payload.index("{")
        end = payload.rindex("}") + 1

        response = json.loads(payload[start:end])
        response_data = response["data"]["item"]

        transaction_id = response_data["transactionId"]
        amount = response_data["token"]["amount"]
        token_symbol = response_data["token"]["symbol"]

        cryptoapis_client = CryptoApis()
        transaction_details = cryptoapis_client.get_transaction_details_by_transactionid(response_data["blockchain"], response_data["network"], transaction_id)
        sender_address = transaction_details["senders"][0]["address"]

        sender_object = Address.objects.get(address=sender_address)
        currency_symbol_object = Cryptocurrency.objects.get(symbol=token_symbol)

        try:
            sender_currency_balance = Balance.objects.get(email=sender_object.email, currency_name=currency_symbol_object)
        except:
            sender_currency_balance = Balance(currency_name=currency_symbol_object, email=sender_object.email, amount=0)
        
        sender_currency_balance.amount += Decimal(amount)
        sender_currency_balance.save()
        try:
            transactionA = TransactionA(transaction_id=transaction_id, email=sender_object.email, address=sender_object, currency_name=currency_symbol_object, transaction_type="DEPOSIT", state="APPROVED",amount=amount)
            transactionA.save()
        except:
            sender_currency_balance.amount -= Decimal(amount)
            sender_currency_balance.save()
            return HttpResponse("Webhook received!")

        tx_currency = {
            "currency_name": currency_symbol_object.currency_name,
            "symbol": currency_symbol_object.symbol,
        }

        transaction_intern_id = str(transactionA.id_a) + "|" + transaction_id 
        creation_date = timezone.now()
        deposit_funds_email(str(sender_object.email), transaction_intern_id, response_data["blockchain"], response_data["network"] ,amount, tx_currency, ETHEREUM_DEPOSIT_ADDRESS, creation_date)

        # print(response)
        # print(payload.decode("utf-8"))
        return HttpResponse("Webhook received!")





    return HttpResponse(status=200)


# @csrf_exempt
# def test_receiver(request):
#     if request.method == 'GET':
#         return redirect('authentication:Home')


#     request_reader =request.META.get('wsgi.input')

#     # data = {
#     #     "request": str(dir(request_reader)),
#     #     "request_dict": str(request_reader.__dict__),
#     #     "buf_dir": str(dir(request_reader.buf)),
#     #     "buf_dict": str(request_reader.buf.__dict__),
#     #     "reader_dir": str(dir(request_reader.reader)),
#     #     "reader_dict": str(request_reader.reader.__dict__)
#     # }


#     # print(str(dir(request_reader)))
    
#     bpayload = request_reader.read()
#     payload = bpayload.decode("utf-8")

#     start = payload.index("{")
#     end = payload.rindex("}") + 1

#     response = json.loads(payload[start:end])

#     return HttpResponse(str(response))

#     # return HttpResponse(str(data))
#     # return HttpResponse(str(request_reader.buf.__dict__))