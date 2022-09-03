from django.urls import path
from . import views

app_name = "marketplace"

urlpatterns = [
    path("", views.marketplace, name="Marketplace"),
    path("purchase-history/", views.purchases_history, name="PurchaseHistory"),
    path("product/info/<int:id_product>/", views.product_info, name="ProductInfo"),  
    path("product/buy/<int:id_product>/", views.buy_product, name="ProductBuy"),  
]