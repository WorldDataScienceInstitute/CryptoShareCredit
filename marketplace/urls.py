from django.urls import path
from . import views

app_name = "marketplace"

urlpatterns = [
    path("", views.marketplace, name="Marketplace"),
    path("product/<int:id_product>/", views.product_info, name="Product"),  
]