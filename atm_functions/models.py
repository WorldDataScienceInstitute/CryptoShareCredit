from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
from datetime import datetime as dt

# Create your models here.


class Account(models.Model):
    # extension of default user table
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # phone number used for verification
    Email = models.CharField(max_length=40, null=True)

class History(models.Model):
    EmailId = models.OneToOneField(to=User, on_delete=models.CASCADE, primary_key=True)
    Amount = models.BigIntegerField()
    Date = models.DateTimeField()

class Cryptocurrency(models.Model):
    currency_name = models.CharField(max_length=50, primary_key=True)
    contract = models.CharField(max_length=255, unique=True)
    wallet_address = models.CharField(max_length=255)
    blockchain = models.CharField(max_length=21)
    network = models.CharField(max_length=10)
    symbol = models.CharField(max_length=10)

class Address(models.Model):
    address = models.CharField(max_length=100, primary_key=True)
    email = models.ForeignKey(User, on_delete=models.CASCADE)
    currency_name = models.ForeignKey(Cryptocurrency, on_delete=models.DO_NOTHING)

class Balance(models.Model):
    currency_name = models.ForeignKey(Cryptocurrency, on_delete=models.DO_NOTHING)
    email = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=8)

# type is one of 'deposit' or 'withdrawal'
# state is one of 'approved', 'in progress', or 'canceled'
class TransactionA(models.Model):
    id_a = models.AutoField(primary_key=True)
    transaction_id = models.CharField(max_length=255, unique=True)
    email = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING)
    currency_name = models.ForeignKey(Cryptocurrency, on_delete=models.DO_NOTHING)
    transactionType = models.CharField(max_length=15)
    state = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=15, decimal_places=8)

class TransactionB(models.Model):
    id_b = models.AutoField(primary_key=True)
    transaction_id = models.CharField(max_length=255, unique=True)
    emitter = models.ForeignKey(User, related_name = "emmiter_email", on_delete=models.CASCADE)
    address_emitter = models.ForeignKey(Address, related_name = "emmiter_addresss", on_delete=models.DO_NOTHING)
    receptor = models.ForeignKey(User, related_name = "receptor_email", on_delete=models.DO_NOTHING)
    address_receptor = models.ForeignKey(Address, related_name = "receptor_addresss", on_delete=models.DO_NOTHING)
    currency_name = models.ForeignKey(Cryptocurrency, on_delete=models.DO_NOTHING)
    transaction_type = models.CharField(max_length=15)
    state = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=15, decimal_places=8)