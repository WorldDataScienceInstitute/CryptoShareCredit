from django.urls import path
from . import views

app_name = "businesses"

urlpatterns = [
    path("", views.businesses, name="Businesses"),
    path("create/", views.create_business, name="Create"),
    path("manage/", views.manage_businesses, name="Manage"),
    path("manage/<int:id_business>/", views.manage_business, name="ManageBusiness"),
    path("edit/", views.edit_business, name="Edit"),
    path("search/", views.search_business, name="Search"),

    path("manage/<int:id_business>/sales/", views.manage_sales, name="ManageSales"),
    path("manage/<int:id_business>/sales/messages/<int:id_purchase>", views.sale_messages, name="SaleMessages"),
    path("manage/<int:id_business>/sales/messages/<int:id_purchase>/send", views.sale_send_message, name="SaleSendMessage"),

    path("create/product/<int:id_business>/", views.create_product, name="CreateProduct"),
    path("delete/product/<int:id_business>/<int:id_product>/", views.delete_product, name="DeleteProduct"),
    path("manage/product/<int:id_business>/", views.manage_products, name="ManageProduct"),

]
