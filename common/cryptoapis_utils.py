from atm_functions.models import Cryptocurrency, Address
from .cryptoapis import CryptoApis

class CryptoApisUtils:
    def generate_address(self, user, currency_object, register_function = False):
        currency_addresses = Address.objects.filter(email=user, currency_name=currency_object).count()
        error = None

        if currency_addresses == 0:
            available_addresses = Address.objects.filter(
                                                        currency_name = currency_object, 
                                                        email = None
                                                        )
            if available_addresses.count() == 0:
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
                
                if currency_object.blockchain == "xrp":
                    newAddress = Address(
                                        address=deposit_address, 
                                        email=user, 
                                        currency_name=currency_object, 
                                        expiration_datetime = None)
                else:
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

            else:
                newAddress = available_addresses.first()
                newAddress.email = user
                newAddress.save()

            return newAddress, error
        else:
            currency_addresses = Address.objects.get(email=user, currency_name=currency_object)
            
        if register_function:
            error = "You already have an address for this currency."
        return currency_addresses, error


