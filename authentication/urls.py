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
    path('cryptoapis-cb-882177858d66ecf6407ea92945b8a9dfebb576cbb27bc3b8b0fc9541e5e0a2cc.txt/',TemplateView.as_view(template_name="cryptoapis-cb-882177858d66ecf6407ea92945b8a9dfebb576cbb27bc3b8b0fc9541e5e0a2cc.txt", content_type="text/plain"), name="CryptoApis")

]
