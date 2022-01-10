import requests
import json
import time
import os

class CryptoApis:
    def __init__(self):
        self.BASE = "https://rest.cryptoapis.io/v2"
        self.querystring = {"limit":20,"offset":0}
        self.HEADERS = {
        'Content-Type': "application/json",
        'X-API-Key': os.environ['CRYPTOAPIS_API_KEY']
        }
        # len(content["data"]["items"]
    def get_confirmed_transactions(self, blockchain, network):

        if blockchain == "ethereum":
            if network == "mainnet":
                pass
            elif network == "ropsten":
                address = "0xc6981d668ca9e04735efba2cf93110fee883191a"

        url = self.BASE +  f"/blockchain-data/{blockchain}/{network}/addresses/{address}/transactions"
        request = requests.get(url, headers=self.HEADERS, params=self.querystring).json()

        return request["data"]["items"]

    def get_transaction_details_by_transactionid(self, blockchain, network, transactionid):
        url = self.BASE +  f"/blockchain-data/{blockchain}/{network}/transactions/{transactionid}"
        request = requests.get(url, headers=self.HEADERS).json()

        return request["data"]["item"]

    def get_exchange_rate_by_symbols(self,fromSymbol, toSymbol):
        url = self.BASE +  f"/market-data/exchange-rates/by-symbols/{fromSymbol}/{toSymbol}?context=&calculationTimestamp={int(time.time())}"
        request = requests.get(url, headers=self.HEADERS).json()
        
        return request['data']["item"]
        

if __name__ == "__main__":
    # cryptoapis_client = CryptoApis()
    # exchange_rate = cryptoapis_client.get_exchange_rate_by_symbols("ETH", "USD")["rate"]
    # print(exchange_rate)
    # crypto = CryptoApis()
    # data = crypto.get_transaction_details_by_transactionid("ethereum", "ropsten", "0x312af4de375e8851bb40e7cd3358286663e7809f279c3e2c2fb55d506cf41e95")

    # print(data)

    pass
    # print("This is a module")
    # crypto = CryptoApis()
    # content = crypto.confirmed_transactions("ethereum", "ropsten")
    # print(content["data"]["items"])
    # # print(content["data"]["items"])
    # print(len(content["data"]["items"]))