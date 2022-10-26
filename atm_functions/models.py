from calendar import month
from django.db import models
from django.contrib.auth.models import User
from businesses.models import Business
from django.utils import timezone
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# Create your models here.


# <--------------- ACCOUNT OBJECTS ----------------->
# <--------------- ACCOUNT OBJECTS ----------------->
# <--------------- ACCOUNT OBJECTS ----------------->

class Account(models.Model):
    # extension of default user table
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # phone number used for verification
    email = models.CharField(max_length=40, null=True)
    credit_grade = models.CharField(max_length=4, default="FFF")
    country = models.CharField(max_length=57, null=True)
    state = models.CharField(max_length=57, null=True)
    birthdate = models.DateField(null=True)
    system_username = models.CharField(max_length=30, unique=True, null=True)
    net_worth = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    card_pin = models.CharField(max_length=12, null=True)

class StripeAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    stripe_customer_id = models.CharField(max_length=20, null=False)
    description = models.CharField(max_length=100, null=True)

class UserAssets(models.Model):
    id_asset = models.AutoField(primary_key=True)
    email = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    type = models.CharField(max_length=20, null=True)
    name = models.CharField(max_length=255, null=True)
    worth = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    extra_field = models.CharField(max_length=57, null=True)

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    username = models.CharField(max_length=30, null=True)
    user_reference = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contact_user', null=True)

class Notification(models.Model):
    id_notification = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_lob = models.CharField(max_length=20, null=True)
    notification_type = models.CharField(max_length=20, null=True)
    notification_state = models.CharField(max_length=15)
    description = models.CharField(max_length=255, null=True)
    creation_datetime = models.DateTimeField(auto_now_add=True)

# <--------------- ACCOUNT OBJECTS ----------------->
# <--------------- ACCOUNT OBJECTS ----------------->
# <--------------- ACCOUNT OBJECTS ----------------->



class DynamicUsername(models.Model):
    id_username = models.CharField(max_length=30, primary_key=True)
    username_type = models.CharField(max_length=10, null=True) # USER or BUSINESS
    user_reference = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    business_reference = models.ForeignKey(Business, on_delete=models.CASCADE, null=True, related_name='user_owner_business')
    referral_credits = models.DecimalField(max_digits=15, decimal_places=6, default=10)

class WaitingList(models.Model):
    id_wl = models.AutoField(primary_key=True)
    email = models.CharField(max_length=40)

class History(models.Model):
    EmailId = models.OneToOneField(to=User, on_delete=models.CASCADE, primary_key=True)
    Amount = models.BigIntegerField()
    Date = models.DateTimeField()


# <--------------- CURRENCIES ----------------->
# <--------------- CURRENCIES ----------------->
# <--------------- CURRENCIES ----------------->


# <--------------- DIGITAL CURRENCIES ----------------->
class DigitalCurrency(models.Model):
    id_currency = models.AutoField(primary_key=True)
    currency_name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=10)
    currency_type = models.CharField(max_length=10)
    exchange_rate = models.DecimalField(max_digits=15, decimal_places=6)

class Cryptocurrency(models.Model):
    currency_name = models.CharField(max_length=50, primary_key=True)
    contract = models.CharField(max_length=255, unique=True)
    wallet_address = models.CharField(max_length=255)
    blockchain = models.CharField(max_length=21)
    network = models.CharField(max_length=10)
    symbol = models.CharField(max_length=10)
    currency_type = models.CharField(max_length=10)
    exchange_rate = models.DecimalField(max_digits=15, decimal_places=6)

class Currency(models.Model):
    id_currency = models.AutoField(primary_key=True)
    currency_type = models.CharField(max_length=10)
    currency_name = models.CharField(max_length=50)
    crypto_currency =  models.ForeignKey(Cryptocurrency, on_delete=models.SET_NULL, null=True)
    digital_currency =  models.ForeignKey(DigitalCurrency, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)


# <--------------- CURRENCIES ----------------->
# <--------------- CURRENCIES ----------------->
# <--------------- CURRENCIES ----------------->




# <--------------- FINANCE ----------------->
# <--------------- FINANCE ----------------->
# <--------------- FINANCE ----------------->

class Address(models.Model):
    address = models.CharField(max_length=100, primary_key=True)
    email = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    currency_name = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE)
    expiration_datetime = models.DateTimeField(default=timezone.now()+timedelta(days=6), null= True)

class Balance(models.Model):
    currency_type = models.CharField(max_length=10)
    currency_name = models.ForeignKey(Cryptocurrency, on_delete=models.SET_NULL, null=True)
    digital_currency_name = models.ForeignKey(DigitalCurrency, on_delete=models.SET_NULL, null=True)
    email = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=18, decimal_places=8)

# <--------------- FINANCE ----------------->
# <--------------- FINANCE ----------------->
# <--------------- FINANCE ----------------->


# <--------------- WILLS ----------------->
# <--------------- WILLS ----------------->
# <--------------- WILLS ----------------->

class BlockchainWill(models.Model):
    id_w = models.AutoField(primary_key=True)
    transaction_id = models.CharField(max_length=255, unique=True, null=True)
    email = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=15)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    full_legal_name = models.CharField(max_length=255, null=True)
    birthdate = models.DateField(null=True)
    birth_country = models.CharField(max_length=57, null=True)
    associated_email1 = models.CharField(max_length=40, null=True)
    associated_email2 = models.CharField(max_length=40, null=True)
    associated_email3 = models.CharField(max_length=40, null=True)
    selfie_photo_url = models.CharField(max_length=255, null=True)      
    document_id_url = models.CharField(max_length=255, null=True)      
    video_url = models.CharField(max_length=255, null=True)      

class Beneficiary(models.Model):
    blockchain_wills = models.ManyToManyField(BlockchainWill)
    full_legal_name = models.CharField(max_length=255, null=True)
    birthdate = models.DateField(null=True)
    birth_country = models.CharField(max_length=57, null=True)
    relationship = models.CharField(max_length=50, null=True)
    associated_email1 = models.CharField(max_length=40, null=True)
    associated_email2 = models.CharField(max_length=40, null=True)
    will_percentage = models.IntegerField(null=True)
    selfie_photo_url = models.CharField(max_length=255, null=True)

# <--------------- WILLS ----------------->
# <--------------- WILLS ----------------->
# <--------------- WILLS -----------------> 

# <--------------- INSURANCE ----------------->
# <--------------- INSURANCE ----------------->
# <--------------- INSURANCE ----------------->

class Insurance(models.Model):
    id_insurance = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=18, decimal_places=8)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    expiration_datetime = models.DateTimeField(default=timezone.now() + relativedelta(months=6), null= True)


# <--------------- INSURANCE ----------------->
# <--------------- INSURANCE ----------------->
# <--------------- INSURANCE ----------------->


    
class TransactionStripe(models.Model):
    id_transaction = models.AutoField(primary_key=True)
    stripe_account = models.ForeignKey(StripeAccount, on_delete=models.CASCADE)
    payment_intent = models.CharField(max_length=30, unique=True, null=False)
    amount = models.DecimalField(max_digits=18, decimal_places=8)
    transaction_type = models.CharField(max_length=15)
    transaction_type_internal = models.CharField(max_length=30)
    transaction_state = models.CharField(max_length=15)
    creation_datetime = models.DateTimeField(auto_now_add=True)

class TransactionCredits(models.Model):
    id_transaction = models.AutoField(primary_key=True)
    sender_user = models.ForeignKey(User, related_name = "new_sender_user", on_delete=models.CASCADE)
    sender_username = models.CharField(max_length=30, null=True)
    receiver_user = models.ForeignKey(User, related_name = "new_receiver_user", on_delete=models.CASCADE)
    receiver_username = models.CharField(max_length=30, null=True)
    digital_currency_name = models.ForeignKey(DigitalCurrency, on_delete=models.DO_NOTHING)
    transaction_type = models.CharField(max_length=15)
    transaction_state = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=18, decimal_places=8)
    note = models.CharField(max_length=100, null=True)
    creation_datetime = models.DateTimeField(auto_now_add=True)

class Referral(models.Model):
    id_referal = models.AutoField(primary_key=True)
    referral_code = models.CharField(max_length=30, null=False)
    credits = models.DecimalField(max_digits=18, decimal_places=8, default = 10)
    user_referring = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_referring')
    user_referred = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_referred')
    creation_datetime = models.DateTimeField(auto_now_add=True)

#Transaction for Deposits and Withdrawals CRYPTO
class TransactionA(models.Model):
    id_a = models.AutoField(primary_key=True)
    transaction_id = models.CharField(max_length=255, unique=True)
    email = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING, null=True)
    currency_name = models.ForeignKey(Cryptocurrency, on_delete=models.DO_NOTHING)
    transaction_type = models.CharField(max_length=15)
    state = models.CharField(max_length=15)
    internal_state = models.CharField(max_length=35, null=True)
    amount = models.DecimalField(max_digits=15, decimal_places=8)
    creation_datetime = models.DateTimeField(auto_now_add=True)

#Transaction for lending and borrowing
class TransactionB(models.Model):
    id_b = models.AutoField(primary_key=True)
    transaction_id = models.CharField(max_length=255, unique=True)
    emitter = models.ForeignKey(User, related_name = "emmiter_email", on_delete=models.CASCADE)
    # address_emitter = models.ForeignKey(Address, related_name = "emmiter_addresss", on_delete=models.DO_NOTHING)
    receptor = models.ForeignKey(User, related_name = "receptor_email", on_delete=models.DO_NOTHING, null=True)
    # address_receptor = models.ForeignKey(Address, related_name = "receptor_addresss", on_delete=models.DO_NOTHING, null=True)
    currency_name = models.ForeignKey(Cryptocurrency, on_delete=models.DO_NOTHING)
    currency_name_collateral = models.ForeignKey(Cryptocurrency, related_name = "currency_name_collateral", on_delete=models.DO_NOTHING)
    transaction_type = models.CharField(max_length=15)
    state = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=15, decimal_places=8)
    amount_collateral = models.DecimalField(max_digits=15, decimal_places=8, null=True)
    interest_rate = models.IntegerField(null=True)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    start_datetime = models.DateTimeField(null=True)
    end_datetime = models.DateTimeField(null=True)

# #Transaction for swapping CRYPTO
# class TransactionC(models.Model):
#     id_c = models.AutoField(primary_key=True)
#     transaction_id = models.CharField(max_length=38, unique=True)
#     creation_datetime = models.DateTimeField(auto_now_add=True)
#     email = models.ForeignKey(User, on_delete=models.CASCADE)
#     crypto_id_from = models.CharField(max_length=10)
#     crypto_id_to = models.CharField(max_length=10)
#     address_destination = models.CharField(max_length=100)
#     address_destination_ed = models.CharField(max_length=30, null=True)
#     address_refund = models.CharField(max_length=100)
#     address_refund_ed = models.CharField(max_length=30, null=True)
#     amount = models.DecimalField(max_digits=15, decimal_places=8)
#     amount_estimated = models.DecimalField(max_digits=15, decimal_places=8)
