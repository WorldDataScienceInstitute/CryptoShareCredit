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
]
