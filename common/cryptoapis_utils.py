from atm_functions.models import Cryptocurrency, Address
from django.utils import timezone
from datetime import timedelta
from .cryptoapis import CryptoApis

class CryptoApisUtils:
    def generate_address(self, user, currency_object, register_function = False):
        currency_addresses = Address.objects.filter(email=user, currency_name=currency_object).count()
        error = None

        if currency_addresses != 0:
            currency_addresses = Address.objects.get(email=user, currency_name=currency_object)
            if register_function:
                error = "You already have an address for this currency."
            return currency_addresses, error
        else:
            available_addresses = Address.objects.filter(
                                                        currency_name = currency_object, 
                                                        email = None
                                                        )
            if available_addresses.count() != 0:
                newAddress = available_addresses.first()
                newAddress.email = user
                newAddress.expiration_datetime = timezone.now()+timedelta(days=6)
                newAddress.save()
                
            elif available_addresses.count() == 0:
                cryptoapis_client = CryptoApis()

                number_of_addresses = Address.objects.filter(currency_name = currency_object).count()

                try:
                    deposit_address = cryptoapis_client.generate_deposit_address(
                                                                                currency_object.blockchain, 
                                                                                currency_object.network, 
                                                                                number_of_addresses)
                except:
                    error = "Error generating address. Please try again later."
                    return None, error
                
                # if currency_object.blockchain == "xrp":
                #     newAddress = Address(
                #                         address=deposit_address, 
                #                         email=user, 
                #                         currency_name=currency_object, 
                #                         expiration_datetime = None)
                # else:
                #     newAddress = Address(
                #                         address=deposit_address, 
                #                         email=user, 
                #                         currency_name=currency_object)

                newAddress = Address(
                                    address=deposit_address, 
                                    email=user, 
                                    currency_name=currency_object)

                newAddress.save()

                try:
                    cryptoapis_client.generate_coin_subscription(currency_object.blockchain, currency_object.network, deposit_address)
                except:
                    newAddress.email = None
                    newAddress.save()
                    error = "Error generating address, please contact support"
                    return None, error
                
                #GENERATE TOKEN SUBSCRIPTION
                if currency_object.blockchain == "ethereum" and currency_object.network == "mainnet":
                    try:
                        cryptoapis_client.generate_token_subscription(currency_object.blockchain, currency_object.network, deposit_address)
                    except:
                            newAddress.email = None
                            newAddress.save()
                            error = "Error generating address for ERC-20 Tokens, please contact support"
                            return None, error

            return newAddress, error
        


def get_currencies_exchange_rate():
    cryptoapis_client = CryptoApis()

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

    exchange_rates = []
    exchange_rates.append(rate_ltc)
    exchange_rates.append(rate_bch)
    exchange_rates.append(rate_dash)
    exchange_rates.append(rate_zec)
    exchange_rates.append(rate_xrp)

    return exchange_rates
