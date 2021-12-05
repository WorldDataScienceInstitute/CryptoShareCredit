from django.urls import path
from . import views

app_name = 'authentication'
urlpatterns = [
    path('', views.home, name='Home'),
    path('Email/', views.email, name='Email'),
    path('GiveBack/', views.give_back, name="GiveBack"),
    path('Verify/', views.verify, name='Verify'),
    path('Signing/', views.signing, name='Signing'),
    path('Registration/', views.registration, name='Registration'),
    path('Login/', views.views.login, name='Login'),
    path('Logout/', views.logout, name='Logout'),
]
