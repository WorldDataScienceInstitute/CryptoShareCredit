from django.urls import path
from . import views

app_name = "atm_functions"
urlpatterns = [
     path("", views.home, name="Home"),
     path("ApproveWallet/", views.approve_wallet, name="ApproveWallet"),
     path("Businesses/", views.businesses, name="Businesses"),
     path("CreateBusiness/", views.create_business, name="CreateBusiness"),
     path("ManageBusinesses/", views.manage_businesses, name="ManageBusinesses"),
     path("EditBusiness/", views.edit_business, name="EditBusiness"),
     path("EstateNetWorth/", views.estate_net_worth, name="EstateNetWorth"),
     path("EditEstateNetWorth/", views.edit_estate_net_worth, name="EditEstateNetWorth"),
     path("SearchBusiness/", views.search_business, name="SearchBusiness"),
     path("BlockchainWills/", views.blockchain_wills, name="BlockchainWills"),
     path("RegisterBlockchainWill/", views.register_blockchain_will, name="RegisterBlockchainWill"),
     path("CertificateBlockchainWill/", views.certificate_blockchain_will, name="CertificateBlockchainWill"),     
     path("CertificateBlockchainWill/<int:id>/", views.certificate_blockchain_will, name="CertificateBlockchainWill"),     
     path("BuyCrypto/", views.buy_crypto, name="BuyCrypto"),
     path("BuyCredit/", views.buy_credit, name="BuyCredit"),
     path("BuyCryptoWidget/", views.buy_crypto_widget, name="BuyCryptoWidget"),
     path("CheckCredit/", views.check_balance, name="CheckCredit"),
     path("CreditGrades/", views.credit_grades, name="CreditGrades"),
     path("CryptoShareWallet/", views.cryptoshare_wallet, name="CryptoShareWallet"),
     path("CryptoNews/", views.crypto_news, name="CryptoNews"),
     path("ConnectWallet/", views.connect_wallet, name="ConnectWallet"),
     path("DisconnectWallet/", views.disconnect_wallet, name="DisconnectWallet"),
     path("GenerateAddress/", views.generate_address, name="GenerateAddress"),
     path("MyAddresses/", views.my_addresses, name="MyAddresses"),
     path("MyTransactions/", views.my_transactions, name="MyTransactions"),
     path("Profile/", views.profile, name="Profile"),
     path("SwapCrypto/", views.swap_crypto, name="SwapCrypto"),
     path("Settings/", views.atm_settings, name="Settings"),
     path("SendCoinbaseWallet/", views.send_coinbase_wallet, name="SendCoinbaseWallet"),
     path("SendCryptoShareWallet/", views.send_cryptoshare_wallet, name="SendCryptoShareWallet"),
     path("SendMoneyConfirmation/", views.send_money_confirmation, name="SendMoneyConfirmation"),
     path("TransferMoney/", views.transfer_money, name="TransferMoney"),

     #API ENDPOINTS
     path("SimpleSwapAPI/", views.simpleswap_api, name="SimpleSwapAPI"),
     path("GetCreditGrade/", views.get_credit_grade, name="GetCreditGrade"),
     path("CurrenciesWidget/", views.get_currencies_balance_widget, name="CurrenciesWidget"),


     #WEBHOOKS
     path("ConfirmationsCoinTransactions/", views.confirmations_coin_transactions, name="ConfirmationsCryptoTransactions"),
     path("ConfirmedCoinTransactions/", views.confirmed_coin_transactions, name="ConfirmedCoinTransactions"),
     path("ConfirmedTokenTransactions/", views.confirmed_token_transactions, name="ConfirmedTokenTransactions"),
     path("DailyRoutine/", views.daily_routine, name="DailyRoutine"),
     path("UpdateExchangeRates/", views.update_exchange_rates, name="UpdateExchangeRates"),
     path("RegisterWaitlistEmail/", views.register_waitlist_email, name="RegisterWaitlistEmail"),
     path("TestReceiver/", views.test_receiver, name="TestReceiver")
     # path("NotificationService/", views.notification_service, name="NotificationService")
]
