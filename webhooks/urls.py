from django.urls import path
from . import views

app_name = "webhooks"

urlpatterns = [
    path("", views.test, name="Webhooks"),
    path("GetNotifications/", views.get_notifications, name="GetNotifications"),
]
