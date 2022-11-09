import requests
import json
import time
import os

class CryptoSharePay:
    def __init__(self):
        self.BASE = "https://api.cryptosharepay.com/v1"
        self.HEADERS = {
        "Content-Type": "application/json"
        }

    def get_transaction(self, transaction_id):
        url = self.BASE +  f"/protected/transactions/payments/{transaction_id}/"
        print(url)
        response = requests.get(url, headers=self.HEADERS).json()

        return response

    
    # def generate_coins_transaction_from_wallet(self, blockchain, network, address, amount, data = ""):
    #     url = self.BASE + f"/wallet-as-a-service/wallets/{self.WALLET_ID}/{blockchain}/{network}/transaction-requests"
    #     data = {
    #             "context": "",
    #             "data": {
    #                 "item": {
    #                     "callbackSecretKey": self.CALLBACK_SECRET_KEY,
    #                     "callbackUrl": "https://www.cryptoshareapp.com/atm/ConfirmationsCoinTransactions/",
    #                     "feePriority": "standard",
    #                     "note": data,
    #                     "prepareStrategy": "optimize-size",
    #                     "recipients": [
    #                         {
    #                             "address": address,
    #                             "amount": amount
    #                         }
    #                     ]
    #                 }
    #             }
    #         }

    #     request = requests.post(url, headers=self.HEADERS, json=data).json()

    #     return request["data"]["item"]

