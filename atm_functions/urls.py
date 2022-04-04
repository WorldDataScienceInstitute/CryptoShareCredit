from django.urls import path
from . import views

app_name = 'atm_functions'
urlpatterns = [
     path('CheckBalance/', views.check_balance, name='CheckBalance'),
     path('WithdrawMoney/', views.withdraw_money, name='WithdrawMoney'),
     path('DepositMoney/', views.deposit_money, name='DepositMoney'),
     path('DepositSelection/', views.deposit_selection, name='DepositSelection'),
     path('CryptoShareWallet/', views.cryptoshare_wallet, name='CryptoShareWallet'),
     path('SelectBank/', views.bank, name='SelectBank'),
     path('TyWithdraw/', views.ty_withdraw, name='TyWithdraw'),
     path('TyDeposit/', views.ty_deposit, name='TyDeposit'),
     path('BuyCrypto/', views.buy_crypto, name='BuyCrypto'),
     path('BorrowMoney/', views.borrow_money, name='BorrowMoney'),
     path('BorrowCrypto/', views.borrow_crypto, name='BorrowCrypto'),
     path('BorrowCryptoDashboard/', views.borrow_crypto_dashboard, name='BorrowCryptoDashboard'),
     path('CreateBorrowingOffer/', views.create_borrowing_offer, name='CreateBorrowingOffer'),
     path('CreateLendingOffer/', views.create_lending_offer, name='CreateLendingOffer'),
     path('RemoveOffer/', views.remove_offer, name='RemoveOffer'),
     path('PayOffer/', views.pay_offer, name='PayOffer'),
     path('LendMoney/', views.lend_money, name='LendMoney'),
     path('LendCrypto/', views.lend_crypto, name='LendCrypto'),
     path('BorrowOffer/', views.borrow_offer, name='BorrowOffer'),
     path('LendOffer/', views.lend_offer, name='LendOffer'),
     path('Shop/', views.shop, name="Shop"),
     path('Settings/', views.atm_settings, name="Settings"),
     path('EarnMoney/', views.earn_money, name="EarnMoney"),
     path('ConnectWallet/', views.connect_wallet, name="ConnectWallet"),
     path('ApproveWallet/', views.approve_wallet, name="ApproveWallet"),
     path('DisconnectWallet/', views.disconnect_wallet, name="DisconnectWallet"),
     path('SendMoney/', views.send_money, name="SendMoney"),
     path('SendCoinbaseWallet/', views.send_coinbase_wallet, name="SendCoinbaseWallet"),
     path('SendCryptoShareWallet/', views.send_cryptoshare_wallet, name="SendCryptoShareWallet"),
     path('SendMoneyConfirmation/', views.send_money_confirmation, name="SendMoneyConfirmation"),
     path('MyAddresses/', views.my_addresses, name="MyAddresses"),
     path('MyTransactions/', views.my_transactions, name="MyTransactions"),
     path('RegisterAddress/', views.register_address, name="RegisterAddress"),
     path('GenerateAddress/', views.generate_address, name="GenerateAddress"),
     path('CardDashboard/', views.card_dashboard, name="CardDashboard"),
     path('CardCreateUser/', views.aptopayments_create_user, name="CardCreateUser"),
     #WEBHOOKS
     path('ConfirmationsCoinTransactions/', views.confirmations_coin_transactions, name="ConfirmationsCryptoTransactions"),
     path('ConfirmedCoinTransactions/', views.confirmed_coin_transactions, name="ConfirmedCoinTransactions"),
     path('ConfirmedTokenTransactions/', views.confirmed_token_transactions, name="ConfirmedTokenTransactions"),
     path('DailyRoutine/', views.daily_routine, name="DailyRoutine"),
     path('TestReceiver/', views.test_receiver, name="TestReceiver")
     # path('NotificationService/', views.notification_service, name="NotificationService")
]
