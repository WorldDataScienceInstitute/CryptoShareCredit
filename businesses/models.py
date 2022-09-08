from django.db import models
from django.contrib.auth.models import User
# from marketplace.models import PurchaseHistory

# Create your models here.


class Business(models.Model):
    id_business = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_owner')
    official_name = models.CharField(max_length=57)
    system_name = models.CharField(max_length=57)
    logo_url = models.CharField(max_length=255, null=True)
    category = models.CharField(max_length=30)
    system_category = models.CharField(max_length=30, null=True)
    creation_datetime = models.DateTimeField(auto_now_add=True)


class BusinessMessages(models.Model):
    id_message = models.AutoField(primary_key=True)
    id_purchase = models.ForeignKey("marketplace.PurchaseHistory", on_delete=models.CASCADE)
    message_sender = models.CharField(max_length=20, null=True)
    message = models.TextField(null=True, blank=True)
    creation_datetime = models.DateTimeField(auto_now_add=True)