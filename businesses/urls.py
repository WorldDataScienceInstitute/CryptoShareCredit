from django.urls import path
from . import views

app_name = "businesses"

urlpatterns = [
    path("", views.test, name="Businesses"),
]