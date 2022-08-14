from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Business(models.Model):
    id_business = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_owner')
    official_name = models.CharField(max_length=57)
    system_name = models.CharField(max_length=57)
    logo_url = models.CharField(max_length=255, null=True)
    category = models.CharField(max_length=30)
    creation_datetime = models.DateTimeField(auto_now_add=True)