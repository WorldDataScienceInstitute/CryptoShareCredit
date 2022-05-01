import requests
import json
import os
# from fake_useragent import UserAgent

class SimpleSwap:
    def __init__(self):
        self.BASE = "https://api.simpleswap.io/v1"
        self.QUERYPARAMS = {
                            # "api_key": os.environ.get("SIMPLESWAP_API_KEY")
                            "api_key": "d7202cef-1406-4810-8735-749255cd8ae1"
        }
        self.USER_AGENT = "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1467.0 Safari/537.36"
        self.HEADERS = {
                        "Content-Type": "application/json",
        }
        
    def get_exchange_pairs_for_currency(self, symbol):
        url = self.BASE + f"/get_pairs"
        endpoint_params = {
                            "fixed": False,
                            "symbol": symbol
        }
        response = requests.get(url, headers=self.HEADERS, params=(dict(self.QUERYPARAMS,**endpoint_params))).json()
        return response

    def get_estimated_exchange_amount(self, currency_from, currency_to, amount):
        url = self.BASE + f"/get_estimated"
        endpoint_params = {
                            "fixed": False,
                            "currency_from": currency_from,
                            "currency_to": currency_to,
                            "amount": amount
        }

        response = requests.get(url, headers=self.HEADERS, params=(dict(self.QUERYPARAMS,**endpoint_params))).json()
        return response
    
    def get_minimal_exchange_amount(self, currency_from, currency_to):
        url = self.BASE + f"/get_ranges"
        endpoint_params = {
                            "fixed": False,
                            "currency_from": currency_from,
                            "currency_to": currency_to
        }

        response = requests.get(url, headers=self.HEADERS, params=(dict(self.QUERYPARAMS,**endpoint_params))).json()
        return response
    


if __name__ == "__main__":

    simpleswap_client = SimpleSwap()

    r = simpleswap_client.get_exchange_pairs_for_currency("BTC")

    # r = simpleswap_client.get_estimated_exchange_amount("BTC", "USDC", 1)

    # r = simpleswap_client.get_minimal_exchange_amount("BTC", "USDC")

    print(r, type(r))
    # print(type(r))

    # def get_confirmed_transactions(self, blockchain, network):

    #     if blockchain == "ethereum":
    #         if network == "mainnet":
    #             pass
    #         elif network == "ropsten":
    #             address = "0xc6981d668ca9e04735efba2cf93110fee883191a"

    #     url = self.BASE +  f"/blockchain-data/{blockchain}/{network}/addresses/{address}/transactions"
    #     request = requests.get(url, headers=self.HEADERS, params=self.querystring).json()

    #     return request["data"]["items"]

    # def is_valid_address(self, blockchain, network, address):
    #     url = self.BASE +  f"/blockchain-tools/{blockchain}/{network}/addresses/validate"
    #     data ={
    #             "context": "",
    #             "data": {
    #                 "item": {
    #                     "address": f"{address}"
    #                 }
    #             }
    #         }

    #     request = requests.post(url, headers=self.HEADERS, json=data).json()
        
    #     return request["data"]["item"]["isValid"]