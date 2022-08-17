from django.urls import path
from . import views

app_name = "marketplace"

urlpatterns = [
    path("", views.test, name="Marketplace"),
]