from django.shortcuts import render, redirect
from . import views
from django.db.models import Q
from django.contrib import auth
from django.contrib.auth.models import User
from atm_functions.models import Account
from django.contrib import messages
from django.conf import settings
from django.utils.safestring import mark_safe
from common.utils import  state_dict, country_codes
from common.Confirm_emails import Account_Creation_Email, Code_Creation_Email
from traceback import print_exc
from coinbase.wallet.client import OAuthClient


def home(request):
    if request.user.is_authenticated:
        u = User.objects.get(pk=request.user.pk)
        name = u.first_name
    else:
        name = None
    context = {
        'name': name
        }
    if request.method == "POST":
        return render(request, 'signin-up.html', context)
    else:
        return render(request, 'language.html', context)


def signing(request):
    if request.method == "POST":
        context = {'country_codes': country_codes}
        return render(request, 'email.html', context)
    else:
        if request.user.is_authenticated:
            u = User.objects.get(pk=request.user.pk)
            name = u.first_name
        else:
            name = None
        context = {
        'name': name
        }
        return render(request, 'signin-up.html', context)


def email(request):
    """Page for the user to enter their email and phone number to begin registration"""
    context = {'country_codes': country_codes}
    if request.method == 'POST':
        if User.objects.filter(email=request.POST.get('email')).exists():
            messages.info(request, "An account with this email already exists.")
            return render(request, 'email.html', context)
        else:
            pin = request.POST.get('pin')
            email = request.POST.get('email').lower()
            first_name = request.POST.get('fname')
            last_name = request.POST.get('lname')
            user = User.objects.create_user(
                email=email, username=email, password=pin,
                first_name=first_name, last_name=last_name
                )
            Account.objects.create(user=user, Email=email)
            Code_Creation_Email(to_addr=email, pin=pin)
            messages.success(request, mark_safe(
                f"""A confirmation email has been sent to you from {settings.DEFAULT_FROM_EMAIL}.<br>
                If you do not receive it within a few minutes, check your spam/junk folder.""")
                )
            return redirect('authentication:Signing')
    else:
        return render(request, 'email.html', context)


def verify(request):
    """Page for the user to submit their verification code"""
    if 'email' not in request.session:
        messages.info(request, "Please enter your email first.")
        return redirect('authentication:Email')
    if request.method == 'POST':
        ver_code = request.POST.get('ver_code')
        ver_code = ver_code.replace(' ', '')
        ver_code = ver_code.replace('-', '')
        pin = request.POST.get('pin')
        email = request.session['email']
        messages.success(request, mark_safe(
                    """Your email has been verified.<br>
                    You can preview Crypto$hare's features,
                    but you'll need to create a digital debit card wallet to access all of the services."""
                    ))
        return redirect('authentication:Signing')
    else:
        messages.warning(request, mark_safe("""An error occurred. Please try again.<br>
            If this error persists,
            return to the <a href="{% url 'authentication:Email' %}">setup page</a>
            and re-submit your information."""))
        return render(request, 'verify.html')


def registration(request):
    """Page for the user to fully authenticate their account with personal info"""
    context = {
        'states': state_dict,
        'country_codes': country_codes
        }
    if request.user.is_authenticated:
        u = User.objects.get(pk=request.user.pk)
        if u.account.Auth_Level == 1:
            messages.info(request, f"You are currently signed in as {u.email}.")
        if u.account.Auth_Level == 2:
            messages.info(request, f"Your personal information has already been verified.")
            return redirect('authentication:Signing')
        if u.account.Auth_Level == 3:
            messages.info(request, f"Your Crypto$hare account already has full access.")
            return redirect('authentication:Signing')
        if request.method == 'POST':
            messages.success(
                    request, "Your personal information has successfully been verified!"
                    )
            return redirect('authentication:Signing')
        else:
            return render(request, 'reg.html', context)
    else:
        messages.info(request, mark_safe("""Please <a href="/Email/">authenticate your email</a> first before creating
        a digital debit card wallet."""))
        # return redirect('authentication:Signing')
        return render(request, 'reg.html', context)


def login(request):
    """Page for the user to log in"""
    if request.user.is_authenticated:
        messages.info(request, "You are already signed in.")
        return redirect('authentication:Signing')
    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('pin')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "You have been signed in.")

            request.session['wallet_conn'] = False
            request.session['access_token'] = None
            request.session['refresh_token'] = None

            return redirect('atm_functions:CheckBalance')
        else:
            messages.info(request, "Incorrect login information. Please try again.")
            return render(request, 'login.html')
    return render(request, 'login.html')


def logout(request):
    """Logs the user out. No specific page is rendered. Redirects
    user back to the homepage"""

    # ---------- ¡We need to optimize this! ----------
    try:
        coinbase_client = OAuthClient(request.session['access_token'], request.session['refresh_token'])
        coinbase_client.revoke()
    except:
        pass

    auth.logout(request)
    if request.method == 'POST':
        messages.success(request, 'You have been logged out!')
    elif request.method == 'GET':
        messages.info(request, 'You have been automatically logged out due to inactivity.')
    return redirect('authentication:Home')
