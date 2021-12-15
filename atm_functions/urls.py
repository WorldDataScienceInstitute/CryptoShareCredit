from django.urls import path
from . import views

app_name = 'atm_functions'
urlpatterns = [
     path('CheckBalance/', views.check_balance, name='CheckBalance'),
     path('WithdrawMoney/', views.withdraw_money, name='WithdrawMoney'),
     path('DepositMoney/', views.deposit_money, name='DepositMoney'),
     path('DepositSelection/', views.deposit_selection, name='DepositSelection'),
     path('SelectBank/', views.bank, name='SelectBank'),
     path('TyWithdraw/', views.ty_withdraw, name='TyWithdraw'),
     path('TyDeposit/', views.ty_deposit, name='TyDeposit'),
     path('BorrowMoney/', views.borrow_money, name='BorrowMoney'),
     path('LendMoney/', views.lend_money, name='LendMoney'),
     path('Shop/', views.shop, name="Shop"),
     path('Settings/', views.atm_settings, name="Settings"),
     path('EarnMoney/', views.earn_money, name="EarnMoney"),
     path('ConnectWallet/', views.connect_wallet, name="ConnectWallet"),
     path('ApproveWallet/', views.approve_wallet, name="ApproveWallet"),
     path('DisconnectWallet/', views.disconnect_wallet, name="DisconnectWallet"),
     path('SendMoney/', views.send_money, name="SendMoney")
     # path('VerfyWallet/', views.verify_wallet, name="VerfyWallet"),
]
