from django.db import models
from django.contrib.auth.models import User
from businesses.models import Business
from django.utils import timezone
from datetime import datetime, timedelta


class DigitalService(models.Model):
    id_product = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, null=True)
    price = models.DecimalField(max_digits=18, decimal_places=8)
    photo_url = models.CharField(max_length=255, null=True)      
    description = models.CharField(max_length=250, null=True)


class Product(models.Model):
    id_product = models.AutoField(primary_key=True)
    business = models.ForeignKey(Business, on_delete = models.CASCADE)
    category = models.CharField(max_length=30)
    
    digital_service_reference = models.ForeignKey(DigitalService, on_delete = models.CASCADE, null = True)
