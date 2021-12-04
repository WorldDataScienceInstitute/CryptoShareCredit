from django.urls import path
from . import views

app_name = 'authentication'
urlpatterns = [
    path('', views.home, name='Home'),
    path('Email/', views.email, name='Email'),
    path('Verify/', views.verify, name='Verify'),
    path('Signing/', views.signing, name='Signing'),
    path('Registration/', views.registration, name='Registration'),
    path('CardProducts/', views.card_products, name='CardProducts'),
    path('CardIssuance/', views.agreement_issuance, name="CardIssuance"),
    path('CardInfo', views.card_info, name='CardInfo'),
    path('Login/', views.views.login, name='Login'),
    path('Logout/', views.logout, name='Logout'),
]
