from django.urls import path
from . import views

app_name = "cryptosharepay"

urlpatterns = [
    path("pay-with-crypto/<str:transaction_id>/", views.pay_with_cryptoshare, name="PayWithCryptoshare"),
    # path("", views.marketplace, name="CryptosharePay"),
]