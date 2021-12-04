from django.db import models
from django.utils import timezone
# from django.contrib.auth.models import AbstractUser

# class MyUser(AbstractUser):
#     USERNAME_FIELD = 'email'
#     email = models.EmailField(_('email address'), unique=True) # changes email to unique and blank to false
#     REQUIRED_FIELDS = []
# removes email from REQUIRED_FIELDS


class Status(models.Model):
    # id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    ver_id = models.CharField(primary_key=True, verbose_name="AptoID", max_length=40)
    EmailId = models.CharField(max_length=50)
    verify = models.BooleanField(default=False)
    regtime = models.DateTimeField(default=timezone.now)
