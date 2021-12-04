import json
from django.shortcuts import render, redirect
import requests
from . import views
from django.db.models import Q
from django.contrib import auth
from django.contrib.auth.models import User
from atm_functions.models import Account
from django.contrib import messages
from django.conf import settings
from django.utils.safestring import mark_safe
from common.utils import  state_dict, country_codes
from common.utils import get_card_products, apply_for_card, accept_disclaimer, confirm_approval, issue_card, conf_cards_issued, get_transactions
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
            email = request.POST.get('email')
            first_name = request.POST.get('fname')
            last_name = request.POST.get('lname')
            user = User.objects.create_user(
                email=email, username=email, password=pin,
                first_name=first_name, last_name=last_name
                )
            Account.objects.create(user=user)
            #Account_Creation_Email(to_addr=email)
            Code_Creation_Email(to_addr=email,pin=pin)
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
        # u_phone = u.account.Phone
        # context['user_phone'] = u_phone
        if request.method == 'POST':
            fname = request.POST.get('ind_fname')
            lname = request.POST.get('ind_lname')
            # address = request.POST.get('ind_address')
            # city = request.POST.get('ind_city')
            # state = request.POST.get('ind_state')
            # zip_code = request.POST.get('ind_zip')
            # country_code = request.POST.get('ind_country_code', '1')
            # country_code = country_code.replace("+", '')
            # phone = request.POST.get('ind_phone')
            # ssn = request.POST.get('ind_ssn')
            # dob = request.POST.get('ind_dob')
            # pin = request.POST.get('password')

            # verify_dob(u.account.BirthdayVerificationId, dob)
            # create_card_user_response = create_card_user(
            #         u.account.VerificationId, country_code, phone, ssn, u.email,
            #         dob, fname, lname, address, city, state, zip_code)
            # try:
            #     create_card_user_response['user_token']
            # except Exception:
            #     print_exc()
            #     messages.info(request,
            #     mark_safe(f"""Your account could not be created. Please try again. <br>
            #     Error: {create_card_user_response['message']}"""))
            #     return render(request, 'reg.html', context=context)
            # u.set_password(pin)
            u.first_name = fname
            u.last_name = lname
            u.save()
            u.account.Auth_Level = 2
            # u.account.UserToken = create_card_user_response['user_token']
            u.account.save()
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

### Card Issuance
# Steps 1-2
def card_products(request):
    """Retrieves all the available card programs for the user applying for a card.
    Also displays the card agreement to the user"""
    if request.user.is_authenticated:
        u = User.objects.get(pk=request.user.pk)
        if u.account.Auth_Level < 2:
            messages.info(request,
                "You need to create a full account before applying for a digital debit card.")
            return redirect('authentication:Signing')
        session_token = u.account.UserToken
        if request.method == 'POST':
            card_program_id = request.session['card_program_id']
            card_application = apply_for_card(
                session_token=session_token, card_program_id=card_program_id)
            agreement_url = card_application['next_action']['configuration']['disclaimer']['value']
            print(card_application)
            request.session['application_id'] = card_application['id']
            request.session['workflow_id'] = card_application['workflow_object_id']
            request.session['action_id'] = card_application['next_action']['action_id']
            context = {'agreement_url': agreement_url}
            print(request.session['workflow_id'])
            return render(request, 'agreement.html', context)
        if request.method == 'GET':
            get_card_response = get_card_products(session_token=session_token)
            try:
                get_card_response['data']
            except Exception as e:
                messages.warning(request, f"An error occurred: {get_card_response['message']}")
                return redirect('authentication:Signing')
            card_program = get_card_response['data'][0]['name']
            request.session['card_program_id'] = get_card_response['data'][0]['id']
            context = {
                'card_name': card_program
            }
            return render(request, 'cardproducts.html', context)
    else:
        messages.info(request, "Please sign in or register before applying for a digital debit card.")
        return redirect('authentication:Signing')


# Step 3-5
def agreement_issuance(request):
    """Sends acceptance of cardholder agreements to Apto endpoint"""
    if request.user.is_authenticated:
        workflow_id = request.session['workflow_id']
        # print(workflow_id)
        # print(request.session['application_id'])
        u = User.objects.get(pk=request.user.pk)
        accept_result = accept_disclaimer(
            session_token=u.account.UserToken,
            workflow_id=workflow_id,
            action_id=request.session['action_id']
        )
        if accept_result == 200:
            response = confirm_approval(
                session_token=u.account.UserToken,
                application_id=request.session['application_id']
            )
            if response.status_code == 200:
                issue_card(
                    session_token=u.account.UserToken,
                    card_application_id=request.session['application_id']
                )
                Account.objects.filter(user=request.user).update(Auth_Level=3)
                messages.info(request, "Your card has been approved and issued!")
                return redirect('authentication:CardInfo')
            else:
                messages.warning(request, f"An error occurred: {response.json()}")
                return render('authentication:Signing')
        else:
            messages.warning(request, f"An error occurred: {accept_result}")
            return render('authentication:Signing')
    else:
        messages.info(request, "You need to be signed in to access this page.")
        return redirect('authentication:Signing')


# Step 6
def card_info(request):
    if request.user.is_authenticated:
        u = User.objects.get(pk=request.user.pk)
        response = conf_cards_issued(session_token=u.account.UserToken)
        card = response['data'][0]
        card_id = card['account_id']
        transactions = get_transactions(
            session_token=u.account.UserToken, card_id=card_id
        )
        tx_list = [tx for tx in transactions['data']]
        # print(tx_list)
        # card_info = get_balance(card_id)
        status = card['state'].capitalize()
        card_name = card['features']['add_funds']['soft_descriptor']
        balance = card['spendable_today']['amount']
        spend_limit = card['features']['add_funds']['limits']['daily']['max']['amount']
        last_four = card['last_four']
        context = {
            "status": status,
            "spend_limit": spend_limit,
            "balance": balance,
            "card_name": card_name,
            "last_four": last_four,
        }
        return render(request, 'card_info.html', context)
    else:
        messages.info(request, "You need to be signed in to access this page.")
        return redirect('authentication:Signing')


def login(request):
    """Page for the user to log in"""
    if request.user.is_authenticated:
        messages.info(request, "You are already signed in.")
        return redirect('authentication:Signing')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('pin')
        # remove space/dash in case code was copied and pasted
        password = password.replace(' ', '')
        password = password.replace('-', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            # log the user in
            auth.login(request, user)
            messages.success(request, "You have been signed in.")

            request.session['wallet_conn'] = False
            request.session['access_token'] = None
            request.session['refresh_token'] = None

            return redirect('atm_functions:CheckBalance')
        else: # authentication failed
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
    # ---------- ¡We need to optimize this! ----------
    request.session['wallet_conn'] = False
    request.session['access_token'] = None
    request.session['refresh_token'] = None

    auth.logout(request)
    if request.method == 'POST':
        messages.success(request, 'You have been logged out!')
    elif request.method == 'GET':
        messages.info(request, 'You have been automatically logged out due to inactivity.')
    return redirect('authentication:Home')
