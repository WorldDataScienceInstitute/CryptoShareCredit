import requests
import json
import uuid


class AptoPayments:
    def __init__(self):
        self.VERSION = "v1"
        self.BASE = f"https://api.sbx.aptopayments.com/{self.VERSION}"
        self.HEADERS = {
            "Content-Type": "application/json",
            "Api-Key": "Bearer wSKKWswLXqotj6JuL/Qn+73nyaysW8gPACScKhHjyscaWPwMLhFXHy6FD/OyCDi4"
        }
        self.endpoint = ""
        self.endpoint_options = {
            "verifications": "/verifications",
            "user": "/user",
            "config": "/config"
        }
        
    
    def start_phone_verification_process(self, country_code, phone_number):
        self.endpoint = self.endpoint_options["verifications"]
        url = self.BASE + self.endpoint + "/start"
        payload = {
            "datapoint_type": "phone",
            "datapoint": {
                "data_type": "phone",
                "country_code": country_code,
                "phone_number": phone_number
            }
        }

        request = requests.post(url, headers=self.HEADERS, json=payload).json()

        return request

    def start_email_verification_process(self, email, country_code, phone_number):
        self.endpoint = self.endpoint_options["verifications"]
        url = self.BASE + self.endpoint + "/start"
        payload = {
            "datapoint_type": "phone",
            "datapoint": {
                "data_type": "phone",
                "verified": False,
                "not_specified": True,
                "email": email,
                "country_code": country_code,
                "phone_number": phone_number
            }
        }

        request = requests.post(url, headers=self.HEADERS, json=payload).json()

        return request

    def complete_verification_process(self, verification_code, verification_id):
        self.endpoint = self.endpoint_options["verifications"]
        url = self.BASE + self.endpoint + f"/{verification_id}/finish"

        payload = {
            "secret": verification_code
        }

        request = requests.post(url, headers=self.HEADERS, json=payload).json()

        return request

    def create_user(self, email, verification_id, country_code, phone_number, birthdate, first_name, last_name, street_address, street_address_2, city, state, postal_code, country):
        self.endpoint = self.endpoint_options["user"]
        url = self.BASE + self.endpoint

        payload = {
            "metadata": {},
            "custodian_uid": email,
            "data_points": {
                "type": "list",
                "data": [
                    {
                        "data_type": "phone",
                        "verified": True,
                        "verification": {
                            "type": "verification",
                            "verification_type": "phone",
                            "verification_id": verification_id,
                            "status": "passed"
                        },
                        "not_specified": False,
                        "country_code": country_code,
                        "phone_number": phone_number
                    },
                    {
                        "type": "email",
                        "email": email
                    },
                    {
                        "type": "birthdate",
                        "data": birthdate
                    },
                    {
                        "type": "name",
                        "first_name": first_name,
                        "last_name": last_name
                    },
                    {
                        "type": "address",
                        "street_one": street_address,
                        "street_two": street_address_2,
                        "locality": city,
                        "region": state,
                        "postal_code": postal_code,
                        "country": country
                    }
                ]
            }
        }

        request = requests.post(url, headers=self.HEADERS, json=payload).json()

        return request

    def login_user(self, verification_id):
        self.endpoint = self.endpoint_options["user"]
        url = self.BASE + self.endpoint + "/login"
        payload = {
            "verifications":{
                "type": "list",
                "data": [
                    {
                        "verification_id": verification_id
                    },
                    {
                        "verification_id": verification_id
                    }
                ]
            }
        }

        request = requests.post(url, headers=self.HEADERS, json=payload).json()

        return request

    def list_all_card_programs(self):
        self.endpoint = self.endpoint_options["config"]
        url = self.BASE + self.endpoint + "/cardproducts"

        request = requests.get(url, headers=self.HEADERS).json()

        return request

    def retreive_configuration(self):
        self.endpoint = self.endpoint_options["config"]
        url = self.BASE + self.endpoint

        request = requests.get(url, headers=self.HEADERS).json()

        return request


                            
        

if __name__ == "__main__":
    apto_payments = AptoPayments()

    # config = apto_payments.retreive_configuration()
    # print(config)

    # verification = apto_payments.start_email_verification_process("albertonavarreteramirez@gmail.com", "1", "5014767432")
    # print(verification)

    # verification = apto_payments.start_phone_verification_process("1", "5014767432")
    # print(verification)
    # test = apto_payments.list_all_card_programs()

    complete_verification = apto_payments.complete_verification_process("000000", "entity_e5f62636e0bbe5ae")
    print(complete_verification)

    # print(test)
    pass
    # print("This is a module")
    # crypto = CryptoApis()
    # content = crypto.confirmed_transactions("ethereum", "ropsten")
    # print(content["data"]["items"])
    # # print(content["data"]["items"])
    # print(len(content["data"]["items"]))