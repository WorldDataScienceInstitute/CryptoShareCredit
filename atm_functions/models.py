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
    currencyName = models.CharField(max_length=50, primary_key=True)
    contract = models.CharField(max_length=255, unique=True)
    blockchain = models.CharField(max_length=21)
    network = models.CharField(max_length=10)

class Address(models.Model):
    address = models.CharField(max_length=100, primary_key=True)
    email = models.OneToOneField(User)
    currencyName = models.OneToOneField(Cryptocurrency)

class Balance(models.Model):
    currencyName = models.OneToOneField(Cryptocurrency)
    email = models.OneToOneField(User)
    amount = models.DecimalField(max_digits=15, decimal_places=8)

# type is one of 'deposit' or 'withdrawal'
# state is one of 'approved', 'in progress', or 'canceled'
class TransactionA(models.Model):
    transactionId = models.AutoField(primary_key=True)
    email = models.OneToOneField(User)
    address = models.OneToOneField(Address)
    currencyName = models.OneToOneField(Cryptocurrency)
    transactionType = models.CharField(max_length=15)
    state = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=15, decimal_places=8)

class TransactionB(models.Model):
    transactionId = models.AutoField(primary_key=True)
    emitter = models.ForeignKey(User)
    addressEmitter = models.OneToOneField(Address)
    receptor = models.ForeignKey(User)
    addressReceptor = models.OneToOneField(Address)
    currencyName = models.OneToOneField(Cryptocurrency)
    transactionType = models.CharField(max_length=15)
    state = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=15, decimal_places=8)