from django.urls import path
from . import views

app_name = "atm_functions"
urlpatterns = [
     path("", views.home, name="Home"),
     path("CheckCredit/", views.check_balance, name="CheckCredit"),
     path("CreditGrades/", views.credit_grades, name="CreditGrades"),
     path("CryptoShareWallet/", views.cryptoshare_wallet, name="CryptoShareWallet"),
     path("BuyCrypto/", views.buy_crypto, name="BuyCrypto"),
     path("BuyCryptoWidget/", views.buy_crypto_widget, name="BuyCryptoWidget"),
     path("BuyCredit/", views.buy_credit, name="BuyCredit"),
     path("Settings/", views.atm_settings, name="Settings"),
     path("ConnectWallet/", views.connect_wallet, name="ConnectWallet"),
     path("ApproveWallet/", views.approve_wallet, name="ApproveWallet"),
     path("DisconnectWallet/", views.disconnect_wallet, name="DisconnectWallet"),
     path("TransferMoney/", views.transfer_money, name="TransferMoney"),
     path("SendCoinbaseWallet/", views.send_coinbase_wallet, name="SendCoinbaseWallet"),
     path("SendCryptoShareWallet/", views.send_cryptoshare_wallet, name="SendCryptoShareWallet"),
     path("SendMoneyConfirmation/", views.send_money_confirmation, name="SendMoneyConfirmation"),
     path("MyAddresses/", views.my_addresses, name="MyAddresses"),
     path("MyTransactions/", views.my_transactions, name="MyTransactions"),
     path("GenerateAddress/", views.generate_address, name="GenerateAddress"),
     path("GetCreditGrade/", views.get_credit_grade, name="GetCreditGrade"),
     #WEBHOOKS
     path("ConfirmationsCoinTransactions/", views.confirmations_coin_transactions, name="ConfirmationsCryptoTransactions"),
     path("ConfirmedCoinTransactions/", views.confirmed_coin_transactions, name="ConfirmedCoinTransactions"),
     path("ConfirmedTokenTransactions/", views.confirmed_token_transactions, name="ConfirmedTokenTransactions"),
     path("DailyRoutine/", views.daily_routine, name="DailyRoutine"),
     path("UpdateExchangeRates/", views.update_exchange_rates, name="UpdateExchangeRates"),
     path("TestReceiver/", views.test_receiver, name="TestReceiver")
     # path("NotificationService/", views.notification_service, name="NotificationService")
]
