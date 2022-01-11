from django.urls import path
from django.views.generic.base import TemplateView
from . import views

app_name = 'authentication'
urlpatterns = [
    path('', views.home, name='Home'),
    path('Email/', views.email, name='Email'),
    path('GiveBack/', views.give_back, name="GiveBack"),
    path('Verify/', views.verify, name='Verify'),
    path('Signing/', views.signing, name='Signing'),
    path('Registration/', views.registration, name='Registration'),
    path('PasswordReset', views.reset_password, name="PasswordReset"),
    path('Login/', views.views.login, name='Login'),
    path('Logout/', views.logout, name='Logout'),
    path('cryptoapis-cb-6f598fa9ec82e7005f74c3f0db0e67b925580b89f479833b30df93286147020a.txt/',TemplateView.as_view(template_name="cryptoapis-cb-6f598fa9ec82e7005f74c3f0db0e67b925580b89f479833b30df93286147020a.txt", content_type="text/plain"), name="CryptoApis")

]
