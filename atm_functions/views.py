# from time import timezone
from email import message
from multiprocessing import context
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Q
from .models import User
from decimal import Decimal
from atm_functions.models import Account, Address, Balance, Cryptocurrency, TransactionA, TransactionB, TransactionC
# from common.utils import currency_list
from common.utils import get_currencies_exchange_rate, calculate_credit_grade
from common.emails import sent_funds_email, sent_funds_cryptoshare_wallet_email, deposit_funds_email, revoked_address_email, expired_transactionb_email, inprogress_transactionb_email, test_email
from common.cryptoapis import CryptoApis
from common.cryptoapis_utils import CryptoApisUtils
from common.aptopayments import AptoPayments
from google_currency import convert
from coinbase.wallet.client import OAuthClient
from coinbase.wallet.error import TwoFactorRequiredError
from datetime import timedelta

import hmac
import hashlib

import os
import requests
import json

def home(request):
    if not request.user.is_authenticated:
        return render(request, 'atm_login.html')
        # return render(request, "buy_blockchain_credit_lines.html")

    context = {}
    return redirect('atm_functions:CheckCredit')


# @login_required(login_url='authentication:Login')
@login_required()
def credit_grades(request):
    context = {}

    return render(request, 'credit_grades.html', context)

@login_required()
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

    if request.user.is_authenticated:
        # get account details for user
        u = User.objects.get(pk=request.user.pk)

        # get first name
        name = u.first_name

        #---------------------- CRYPTOAPIS ----------------------#
        cryptoapis_balances = Balance.objects.filter(email=request.user)

        context = {
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
                                },
                                {
                                    "currency_name": "Bitcoin",
                                    "blockchain": "bitcoin",
                                    "symbol": "BTC",
                                    "has_address": False
                                },
                                {
                                    "currency_name": "Dogecoin",
                                    "blockchain": "dogecoin",
                                    "symbol": "DOGE",
                                    "has_address": False
                                },
                                {
                                    "currency_name": "Ethereum",
                                    "blockchain": "ethereum",
                                    "symbol": "ETH",
                                    "has_address": False
                                }
                                ]
    }

    currencies = Address.objects.filter(email=request.user).values("currency_name")
    currencies_addresses = Address.objects.filter(email=request.user)

    currencies_dict = {}
    for currency in currencies_addresses:
        currencies_dict[currency.currency_name.currency_name] = currency.address
        
    #Get all wallet addresses from Cryptocurrency table that match currency_name field in currencies variable
    addresses = Cryptocurrency.objects.filter(currency_name__in=currencies)
    context["addresses"] = addresses

    for address in addresses:
        #Changing address blockchain for displaying in frontend
        if address.blockchain == "xrp":
            address.blockchain = "ripple"

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

        elif address.currency_name == "Bitcoin":
            address.wallet_address = currencies_dict["Bitcoin"]
            context["address_confirmations"][5]["has_address"] = True

        elif address.currency_name == "Dogecoin":
            address.wallet_address = currencies_dict["Dogecoin"]
            context["address_confirmations"][6]["has_address"] = True

        elif address.currency_name == "Ethereum":
            address.wallet_address = currencies_dict["Ethereum"]
            context["address_confirmations"][7]["has_address"] = True

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

    return render(request, 'swap_crypto.html')

    # process_step = request.GET.get('step','1')
    # # print(process_step)

    # if process_step == '1':
    #     url = "https://www.coinzark.com/api/v2/swap/currencies"
    #     response = requests.get(url).json()

    #     if response["success"] == "false":
    #         messages.info(request, "Something went wrong, please try again later.")
    #         return redirect('atm_functions:Home')

    #     context = {
    #             "step": 1,
    #             }
        
    #     result = response["result"]

    #     receivable_cryptos = []
    #     depositable_cryptos = []

    #     for crypto in result:
    #         # print(crypto["id"], crypto["canDeposit"], crypto["canReceive"])
    #         if crypto["canDeposit"]:
    #             depositable_cryptos.append(crypto)
    #         if crypto["canReceive"]:
    #             receivable_cryptos.append(crypto)
        
    #     context["receivable_cryptos"] = receivable_cryptos
    #     context["depositable_cryptos"] = depositable_cryptos

    #     return render(request, 'swap_crypto.html', context)

    # if process_step == "2" or process_step == "3":
    #     receive_crypto = request.POST.get('receiveCrypto','').split("|")
    #     deposit_crypto = request.POST.get('depositCrypto','').split("|")
    #     exchangingAmount = request.POST.get('exchangingAmount','')

    #     if not receive_crypto or not deposit_crypto or not exchangingAmount:
    #         messages.info(request, "Please fill all fields before proceeding.")
    #         return redirect('atm_functions:Home')

    # if process_step == "2":
    #     context = {
    #             "step": 2,
    #             }

    #     url = f"https://www.coinzark.com/api/v2/swap/rate?from={receive_crypto[0]}&to={deposit_crypto[0]}&amount={exchangingAmount}"
    #     response = requests.get(url).json()

    #     if response["success"] == "false":
    #         messages.info(request, "Something went wrong, please try again later.")
    #         return redirect('atm_functions:Home')
    #     result = response["result"]

    #     context["receiveCrypto"] = {
    #                                 "id": receive_crypto[0],
    #                                 "name": receive_crypto[1]
    #                                 }

    #     context["depositCrypto"] = {
    #                                 "id": deposit_crypto[0],
    #                                 "name": deposit_crypto[1]
    #                                 }

    #     context["exchangingAmount"] = exchangingAmount
    #     context["rate_result"] = result

    #     return render(request, 'swap_crypto.html', context)
    
    # elif process_step == "3":
    #     context = {
    #             "step": 3,
    #             }

    #     address_destination = request.POST.get('destinationAddress','')
    #     address_refund = request.POST.get('refundAddress','')

    #     url = f"https://www.coinzark.com/api/v2/swap/rate?from={receive_crypto[0]}&to={deposit_crypto[0]}&amount={exchangingAmount}"
    #     response = requests.get(url).json()

    #     if response["success"] == "false":
    #         messages.info(request, "Something went wrong, please try again later.")
    #         return redirect('atm_functions:Home')

    #     url = f"https://www.coinzark.com/api/v2/swap/create"

    #     data = {
    #             "from": receive_crypto[0],
    #             "to": deposit_crypto[0],
    #             "amount": exchangingAmount,
    #             "destination": address_destination,
    #             "refund": address_refund
    #         }

    #         # data = {
    #         #     "from": "BTC",
    #         #     "to": "LTC",
    #         #     "amount": 0.0001,
    #         #     "destination": "Ldg8nAfsUR7DTJ4DHXVhEviwrsDf3H8Viu",
    #         #     "refund": "bc1qmsqmdcslcfvhs7j4ftkxpyng25umfuwmyyy2u6"
    #         # }
    #     print(data)

    #     response2 = requests.post(url, json=data).json()
    #     if response2["success"] == "false":
    #         messages.info(request, "Something went wrong, please try again later.")
    #         return redirect('atm_functions:Home')

    #     transaction_id = response2["result"]["uuid"]

    #     transaction_swap = TransactionC(
    #                                     transaction_id = transaction_id, 
    #                                     email = request.user, 
    #                                     crypto_id_from = receive_crypto[0], 
    #                                     crypto_id_to = deposit_crypto[0], 
    #                                     address_destination = address_destination, 
    #                                     address_refund = address_refund, 
    #                                     amount = exchangingAmount,
    #                                     network_fee = response["result"]["receive_network_fee"],
    #                                     amount_estimated_return = response["result"]["receive_network_fee_included"]
    #                                     )
    #     transaction_swap.save()

    #     print(receive_crypto[0], deposit_crypto[0], exchangingAmount)

    #     return redirect('atm_functions:MyTransactions')

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

    balances = Balance.objects.filter(email=request.user)
    context['balances'] = balances
    
    return render(request,'send_cryptoshare_wallet.html', context)

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


        amount = form_response["sendingAmount"]
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
        total_transaction_amount = transaction_response["totalTransactionAmount"]
        # total_transaction_amount = transaction_response["recipients"][0]["amount"]
        transaction_id = transaction_response["transactionRequestId"]

        balance_object.amount -= Decimal(total_transaction_amount)
        balance_object.save()

        transaction_a = TransactionA(transaction_id=transaction_id, email=request.user, address=sending_address_object, currency_name=currency_object, transaction_type="WITHDRAWAL", state="PENDING", amount=amount, internal_state="WAITING_FOR_APPROVAL")
        transaction_a.save()
        # print(sending_blockchain, sending_currency, amount, recipient_address)

        sent_funds_cryptoshare_wallet_email(str(transaction_a.email), "SENT FUNDS REQUEST", transaction_a.currency_name.currency_name ,transaction_a.amount, "PENDING", transaction_a.creation_datetime, receiver=recipient_address)

        messages.success(request, "Your withdrawal request has been created")

        return redirect('atm_functions:CheckCredit')
    else:
        return redirect('atm_functions:TransferMoney')

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
        return redirect('atm_functions:CryptoShareWallet')
    
    #Check if there is already a balance with that currency name for that email
    balance_exists = Balance.objects.filter(email=email_object, currency_name=currency_object)
    if not balance_exists:
        new_balance = Balance(email=email_object, currency_name=currency_object, amount = 0)
        new_balance.save()

    cryptoapis_utils = CryptoApisUtils()

    address, error = cryptoapis_utils.generate_address(request.user, currency_object, register_function = True)
    if error is not None:
        messages.info(request, error)
        return redirect('atm_functions:CryptoShareWallet')
    
    messages.info(request, "Address generated successfully.")

    return redirect('atm_functions:CryptoShareWallet')

def get_credit_grade(request):
    user = Account.objects.get(user = request.user)

    test = {
        "credit_grade": user.credit_grade
    }
    return HttpResponse(json.dumps(test), content_type="application/json")

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

        coingecko_id = querystring_options[currency.symbol]

        exchange_rate = response[coingecko_id]["usd"]
        currency.exchange_rate = exchange_rate
        currency.save()
    
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
        request_reader = request.META.get('wsgi.input')
        # print(request.headers)

        # bpayload = request_reader.stream.read1()  # UNCOMMENT FOR LOCAL TESTING ENVIRRONMENT
        bpayload = request_reader.read() #UNCOMMENT FOR PRODUCTION ENVIRONMENT

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
        request_reader = request.META.get('wsgi.input')

        # bpayload = request_reader.stream.read1()  # UNCOMMENT FOR LOCAL TESTING ENVIRRONMENT
        bpayload = request_reader.read() #UNCOMMENT FOR PRODUCTION ENVIRONMENT

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

            # sender_object.expiration_datetime = None
            # sender_object.save()

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

        ETHEREUM_DEPOSIT_ADDRESS = "0x70568e1a620468a49136aee7febd357bb9469b2c"
        commission = 1 - 0.01
        request_reader =request.META.get('wsgi.input')

        # print(request.headers)

        # bpayload = request_reader.stream.read1()  # UNCOMMENT FOR LOCAL TESTING ENVIRRONMENT
        bpayload = request_reader.read() #UNCOMMENT FOR PRODUCTION ENVIRONMENT

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
        deposit_funds_email(str(sender_object.email), transaction_intern_id, response_data["blockchain"], response_data["network"] ,amount, tx_currency, ETHEREUM_DEPOSIT_ADDRESS, creation_date)

        # print(response)
        # print(payload.decode("utf-8"))
        return HttpResponse("Webhook received!")





    return HttpResponse(status=200)


@csrf_exempt
def test_receiver(request):

    t = TransactionA.objects.get(id_a=6)
    test_email("albertonavarreteramirez@gmail.com",t.transaction_id, t.currency_name.blockchain, t.currency_name.network ,t.amount, {"symbol":"TST","currency_name":"TEST"}, t.address.address, t.creation_datetime)
    print("OK")
    return HttpResponse(status=200)