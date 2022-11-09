from multiprocessing import context
from django.conf import settings as django_settings
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect, FileResponse, Http404

from decimal import Decimal

from common.cryptosharepay import CryptoSharePay
from common.cryptoapis import CryptoApis
from common.emails import sent_funds_cryptoshare_wallet_email
from common.utils import calculate_credit_grade


from atm_functions.models import User
from atm_functions.models import Account, Address, Balance, Cryptocurrency, DigitalCurrency, BlockchainWill, Beneficiary, TransactionA, TransactionB, WaitingList, UserAssets, StripeAccount, TransactionStripe, DynamicUsername, TransactionCredits, Contact, Notification, Insurance, Referral

@login_required()
def pay_with_cryptoshare(request, transaction_id = None):
    if request.session['country_code'] == "US":
        messages.error(request, "US customers can't use this functionality.", extra_tags='danger')
        return redirect("atm_functions:Home")

    wallet_currencies = {
        "Litecoin": True,
        "Dash": True,
        "Zcash": True,
        "Bitcoin Cash": True,
        "Bitcoin": True,
        "Dogecoin": True
    }


    context = {
        "transaction_exists": False,
        "transaction_id": transaction_id,
    }

    if not transaction_id:
        return render(request, "cryptosharepay/pay_with_crypto.html", context)


    cryptosharepay_client = CryptoSharePay()

    try:
        transaction = cryptosharepay_client.get_transaction(transaction_id)

        if transaction["data"]["transaction"]["status"] != "PENDING":
            # return render(request, "cryptosharepay/pay_with_crypto.html", context)
            context["transaction_exists"] = True
        else:
            context["transaction_exists"] = True
    except:
        return render(request, "cryptosharepay/pay_with_crypto.html", context)

    transaction_data = transaction["data"]["transaction"]
    cryptocurrency_symbol = transaction_data["cryptocurrency_code"]

    try:
        cryptocurrency_object = Cryptocurrency.objects.get(symbol=cryptocurrency_symbol)
    except:
        messages.info(request, "Cryptocurrency not supported.")
        context["transaction_exists"] = False

    if request.method == "POST":
        total_amount = transaction_data["cryptocurrency_amount"]
        amount_received = transaction_data["cryptocurrency_amount_received"]

        if amount_received:
            amount_to_pay = total_amount - amount_received
        else:
            amount_to_pay = total_amount
        
        user_object = request.user

        try:
            balance_object = Balance.objects.get(
                email = user_object,
                currency_name = cryptocurrency_object
            )
            if balance_object.amount < amount_to_pay:
                messages.error(request, "You don't have enough funds to pay for this transaction, please deposit more funds.")
                return redirect('atm_functions:CryptoShareWallet')
        except:
            messages.error(request, "You don't have enough funds to pay for this transaction, please deposit more funds.")
            return redirect('atm_functions:CryptoShareWallet')


        # TRANSFER FUNDS CODECHUNK

        amount = str(float(amount_to_pay) * 0.97)
        recipient_address = transaction_data["address"]

        sending_address_object = Address.objects.get(currency_name=cryptocurrency_object, email=request.user)

        if float(balance_object.amount) < float(amount):
            messages.info(request, "Insufficient funds.")
            return redirect('atm_functions:SendCryptoShareWallet')

        cryptoapis_client = CryptoApis()

        is_valid_address = cryptoapis_client.is_valid_address(cryptocurrency_object.blockchain, "mainnet", recipient_address)
        if not is_valid_address:
            messages.info(request, "Invalid address. Please try again.")
            return redirect('atm_functions:SendCryptoShareWallet')

        if cryptocurrency_object.currency_name in wallet_currencies:
            #MISSING ENDPOINT
            transaction_response = cryptoapis_client.generate_coins_transaction_from_wallet(cryptocurrency_object.blockchain, "mainnet", recipient_address, amount)
            # print(request)
        else:
        # elif sending_currency in address_currencies:
            transaction_response = cryptoapis_client.generate_coins_transaction_from_address(cryptocurrency_object.blockchain, "mainnet",sending_address_object.address, recipient_address, amount)
        # print(request)
        if cryptocurrency_object.currency_name in wallet_currencies:
            total_transaction_amount = transaction_response["totalTransactionAmount"]
        else:
            total_transaction_amount = transaction_response["recipients"][0]["amount"]
            
        transaction_id = transaction_response["transactionRequestId"]

        balance_object.amount -= Decimal(amount_to_pay)
        balance_object.save()

        transaction_a = TransactionA(transaction_id=transaction_id, email=request.user, address=sending_address_object, currency_name=cryptocurrency_object, transaction_type="WITHDRAWAL", state="PENDING", amount=amount, internal_state="WAITING_FOR_APPROVAL")
        transaction_a.save()
        # print(sending_blockchain, sending_currency, amount, recipient_address)

        sent_funds_cryptoshare_wallet_email(str(transaction_a.email), "CrytosharePay Transaction Payment", transaction_a.currency_name.currency_name ,transaction_a.amount, "PENDING", transaction_a.creation_datetime, receiver=recipient_address)
        calculate_credit_grade(request.user)
                




        print(transaction)


    return render(request, "cryptosharepay/pay_with_crypto.html", context)
