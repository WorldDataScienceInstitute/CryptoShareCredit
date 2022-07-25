import os
import smtplib,ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings
from .email_templates import send_funds_template


def Card_Creation_Email(to_addr):
    port = settings.EMAIL_PORT
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Crypto$hare Debit Card Created"

    #Code worked on stmp with gmail but not from domain.com
    #msg['From'] = msg['From'] = f"Crypto$hare <{settings.EMAIL_HOST_USER}>"

    msg['From'] = f"Crypto$hare <{settings.EMAIL_HOST_USER}>"
    msg['To'] = to_addr
    html = """
    <html>
    <head></head>
    <body>
        <p>Hi there!</p>

        <p>This email has been used to create a debit card at <a href="http://www.cryptoshareapp.com/">Crypto$hare</a> - The First Peer to Peer Lending Platform that allows CryptoCurrency & Physical assets to be used as Collateral! </p>

        <p>If this was not you, please secure your account at <a href="http://www.cryptoshareapp.com/">Crypto$hare</a></p>
    </body>
    </html>
    """

    part1 = MIMEText(html, 'html')
    part2 = MIMEText("This email has been used to create a debit card at  http://www.cryptoshareapp.com/", 'Crypto$share')

    msg.attach(part1)
    msg.attach(part2)

    context = ssl.create_default_context()
    s = smtplib.SMTP(settings.EMAIL_HOST,port)
    s.starttls(context=context)
    s.ehlo()
    s.login(settings.EMAIL_HOST_USER, settings.NO_REPLY_PASSWORD)
    s.sendmail(settings.EMAIL_HOST_USER, to_addr, msg.as_string())
    s.quit()
    return


def Account_Creation_Email(to_addr):
    port = settings.EMAIL_PORT
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Crypto$hare Account Created"
    #Code worked on stmp with gmail but not from domain.com
    #msg['From'] = msg['From'] = f"Crypto$hare <{settings.EMAIL_HOST_USER}>"

    msg['From'] = f"Crypto$hare <{settings.EMAIL_HOST_USER}>"
    msg['To'] = to_addr
    html = """
    <html>
    <head></head>
        <body>
        
        <p>Hi there!</p>

        <p>This email has been used to create an account at <a href="http://www.cryptoshareapp.com/">Crypto$hare</a> - The First Peer to Peer Lending Platform that allows CryptoCurrency & Physical assets to be used as Collateral! </p>

        <p>Currently, you may preview Crypto$hare's features, but you'll need to create a digital debit card to access all of the services.</p>
        </body>
    </html>
    """

    part1 = MIMEText(html, 'html')
    part2 = MIMEText("This email has been used to create an account at  http://www.cryptoshareapp.com/", 'Crypto$share')

    msg.attach(part1)
    msg.attach(part2)

    context = ssl.create_default_context()
    s = smtplib.SMTP(settings.EMAIL_HOST,port)
    s.starttls(context=context)
    s.ehlo()
    s.login(settings.EMAIL_HOST_USER, settings.NO_REPLY_PASSWORD)
    s.sendmail(settings.EMAIL_HOST_USER, to_addr, msg.as_string())
    s.quit()
    return


def code_creation_email(to_addr, pin):
    port = settings.EMAIL_PORT
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Crypto$hare PIN Confirmation"

    msg['From'] = f"Crypto$hare <{settings.EMAIL_HOST_USER}>"
    msg['To'] = to_addr
    
    html = f"""
    <html>
    <head></head>
        <body>
        
        <p>Hi there!</p>

        <p>This email has been registered for <a href="http://www.cryptoshareapp.com/">Crypto$hare</a> - The First Peer to Peer Lending Platform that allows CryptoCurrency & Physical assets to be used as Collateral!  </p>

        <p>Your registered 6 digit pin for Crypto$hare is the following:</p>

        <big><big><big><big><b>{pin}</b></big></big></big></big>

        <p>If this was not you, please secure your account at <a href="http://www.cryptoshareapp.com/">Crypto$hare</a></p>
        </body>
    </html>
    """

    part1 = MIMEText(html, 'html')
    part2 = MIMEText("This email has been used to create an account at  http://www.cryptoshareapp.com/", 'Crypto$share')

    msg.attach(part1)
    msg.attach(part2)

    context = ssl.create_default_context()
    s = smtplib.SMTP(settings.EMAIL_HOST,port)
    s.starttls(context=context)
    s.ehlo()
    s.login(settings.EMAIL_HOST_USER, settings.NO_REPLY_PASSWORD)
    s.sendmail(settings.EMAIL_HOST_USER, to_addr, msg.as_string())
    s.quit()
    return


def pin_reset_email(to_addr, pin):
    port = settings.EMAIL_PORT
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Crypto$hare PIN Reset"

    msg['From'] = f"Crypto$hare <{settings.EMAIL_HOST_USER}>"
    msg['To'] = to_addr
    
    html = f"""
    <html>
    <head></head>
        <body>
        
        <p>Hi there!</p>

        <p>You are receiving this email because a PIN reset was requested at <a href="http://www.cryptoshareapp.com/">Crypto$hare</a>.</p>

        <p>Your new PIN for Crypto$hare is the following:</p>

        <big><big><big><big><b>{pin}</b></big></big></big></big>

        <p>If this was not you, please secure your account at <a href="http://www.cryptoshareapp.com/">Crypto$hare</a>.</p>
        </body>
    </html>
    """

    part1 = MIMEText(html, 'html')

    msg.attach(part1)

    context = ssl.create_default_context()
    s = smtplib.SMTP(settings.EMAIL_HOST,port)
    s.starttls(context=context)
    s.ehlo()
    s.login(settings.EMAIL_HOST_USER, settings.NO_REPLY_PASSWORD)
    s.sendmail(settings.EMAIL_HOST_USER, to_addr, msg.as_string())
    s.quit()
    return

def sent_funds_email(sender_email, concept, tx_amount, tx_native_amount, tx_state, creation_date, receiver):
    port = settings.EMAIL_PORT
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Crypto$hare transaction"

    msg['From'] = f"Crypto$hare <{settings.EMAIL_HOST_USER}>"
    msg['To'] = sender_email
    
    html = f"""
    <html>
    <head></head>
        <body>
        
        <p>¡Hi there!</p>

        <p>You are receiving this email because a transaction was made in <a href="http://www.cryptoshareapp.com/">Crypto$hare</a>.</p>

        <p>The transaction details are as follows:</p>

        <p>Transaction concept: {concept}</p>

        <p>Sent to: {receiver}</p>

        <p>Transaction amount {tx_amount['currency']} : {tx_amount['amount']} </p>

        <p>Transaction native amount {tx_native_amount['currency']} : {tx_native_amount['amount']}</p>

        <p>Transaction state: {tx_state}</p>

        <p>Transaction creation date: {creation_date}</p>


        <p>If this was not you, please secure your account at <a href="http://www.cryptoshareapp.com/">Crypto$hare</a>.</p>
        </body>
    </html>
    """

    part1 = MIMEText(html, 'html')

    msg.attach(part1)

    context = ssl.create_default_context()
    s = smtplib.SMTP(settings.EMAIL_HOST,port)
    s.starttls(context=context)
    s.ehlo()
    s.login(settings.EMAIL_HOST_USER, settings.NO_REPLY_PASSWORD)
    s.sendmail(settings.EMAIL_HOST_USER, sender_email, msg.as_string())
    s.quit()
    return

def sent_funds_cryptoshare_wallet_email(sender_email, concept, currency, amount, tx_state, creation_date, receiver = None):
    port = settings.EMAIL_PORT
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Crypto$hare transaction"

    msg['From'] = f"Crypto$hare <{settings.EMAIL_HOST_USER}>"
    msg['To'] = sender_email
    
    html = f"""
    <html>
    <head></head>
        <body>
        
        <p>¡Hi there!</p>

        <p>You are receiving this email because a transaction was made in <a href="http://www.cryptoshareapp.com/">Crypto$hare</a>.</p>

        <p>The transaction details are as follows:</p>

        <p>Transaction concept: {concept}</p>
        """
    if receiver is not None:
        html += f"""
        <p>Sent to: {receiver}</p>
        """
    html += f"""

        <p>Transaction amount {currency} : {amount} </p>

        <p>Transaction state: {tx_state}</p>

        <p>Transaction creation date: {creation_date}</p>


        <p>If this was not you, please secure your account at <a href="http://www.cryptoshareapp.com/">Crypto$hare</a>.</p>
        </body>
    </html>
    """

    part1 = MIMEText(html, 'html')

    msg.attach(part1)

    context = ssl.create_default_context()
    s = smtplib.SMTP(settings.EMAIL_HOST,port)
    s.starttls(context=context)
    s.ehlo()
    s.login(settings.EMAIL_HOST_USER, settings.NO_REPLY_PASSWORD)
    s.sendmail(settings.EMAIL_HOST_USER, sender_email, msg.as_string())
    s.quit()
    return

def deposit_funds_email(sender_email, transaction_id, blockchain, network ,tx_amount, tx_currency, tx_address, creation_date):
    port = settings.EMAIL_PORT
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Crypto$hare transaction"

    msg['From'] = f"Crypto$hare <{settings.EMAIL_HOST_USER}>"
    msg['To'] = sender_email

    html = f"""
    <html>
    <head></head>
        <body>
        
        <p>¡Hi there!</p>

        <p>You are receiving this email because a transaction was made in <a href="http://www.cryptoshareapp.com/">Crypto$hare</a>.</p>

        <p>You have received a deposit into your Crypto$hare account!</p>

        <p>Transaction creation date: {creation_date.strftime('%Y-%m-%d')} UTC</p>

        <p>Transaction hour: {creation_date.strftime('%H:%M:%S')} UTC </p>

        <p>Symbol: {tx_currency["symbol"]}</p>

        <p>Currency: {tx_currency["currency_name"]}</p>

        <p>Amount: {tx_amount}</p>

        <p>Blockchain: {blockchain}</p>

        <p>Network: {network}</p>

        <p>Deposit made to <b>{tx_address}</b> address  </p>

        <p>Please have in mind that for security reasons the assigned deposit address is changed if a deposit is not made within 6 days after the creation date.</p>

        <p>For making a new Crypto Deposit, please go to <a href="https://www.cryptoshareapp.com/atm/DepositCrypto/">Crypto$hare Deposit Crypto</a> and generate a new deposit address</p>

        <p>Customer Support Transaction ID:  <b style="color: red">{transaction_id}</b> </p>

        <p>If this was not you, please secure your account at <a href="http://www.cryptoshareapp.com/">Crypto$hare</a>.</p>
        </body>
    </html>
    """

    part1 = MIMEText(html, 'html')

    msg.attach(part1)

    context = ssl.create_default_context()
    s = smtplib.SMTP(settings.EMAIL_HOST,port)
    s.starttls(context=context)
    s.ehlo()
    s.login(settings.EMAIL_HOST_USER, settings.NO_REPLY_PASSWORD)
    s.sendmail(settings.EMAIL_HOST_USER, sender_email, msg.as_string())
    s.quit()
    return

def revoked_address_email(sender_email, address, currency, blockchain):
    port = settings.EMAIL_PORT
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Crypto$hare revoked address"

    msg['From'] = f"Crypto$hare <{settings.EMAIL_HOST_USER}>"
    msg['To'] = sender_email
    
    html = f"""
    <html>
    <head></head>
        <body>
        
        <p>¡Hi there!</p>

        <p>You are receiving this email because your crypto address was revoked in <a href="http://www.cryptoshareapp.com/">Crypto$hare</a>.</p>

        <p>The address details are as follows:</p>

        <p>Address : {address} </p>

        <p>Currency : {currency}</p>

        <p>Blockchain : {blockchain.capitalize()}</p>



        <b><p>Remember that every generated address that haven't received funds passing the next 6 days from its generation in <a href="http://www.cryptoshareapp.com/">Crypto$hare</a>
        is revoked for security reasons.</p></b>

        <p>For generating another address, please visit <a href="https://www.cryptoshareapp.com/atm/CryptoShareWallet/">Crypto$hare Wallet</a>.</p>

        <p>If you think this is an error, please contact support</p>
        </body>
    </html>
    """

    part1 = MIMEText(html, 'html')

    msg.attach(part1)

    context = ssl.create_default_context()
    s = smtplib.SMTP(settings.EMAIL_HOST,port)
    s.starttls(context=context)
    s.ehlo()
    s.login(settings.EMAIL_HOST_USER, settings.NO_REPLY_PASSWORD)
    s.sendmail(settings.EMAIL_HOST_USER, sender_email, msg.as_string())
    s.quit()
    return

def expired_transactionb_email(sender_email, email_type, id_b, payment_currency, collateral_currency, payment_amount, collateral_amount, interest_rate, days_to_pay, start_datetime, end_datetime):
    port = settings.EMAIL_PORT
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Crypto$hare expired loan"

    msg['From'] = f"Crypto$hare <{settings.EMAIL_HOST_USER}>"
    msg['To'] = sender_email
    
    html = f"""
    <html>
    <head></head>
        <body>
        
        <p>¡Hi there!</p>

        <p>You are receiving this email because your issued loan has expired in <a href="http://www.cryptoshareapp.com/">Crypto$hare</a>.</p>

        <p>The address details are as follows:</p>

        <p>LoanID : {id_b} </p>

        <p> ----------------------------------------- </p>

        <p>Payment Currency : {payment_currency}</p>

        <p>Payment Amount : {payment_amount}</p>

        <p> ----------------------------------------- </p>

        <p>Collateral Currency : {collateral_currency}</p>

        <p>Collateral Amount : {collateral_amount}</p>

        <p> ----------------------------------------- </p>

        <p>Interest Rate : {interest_rate}</p>

        <p>Days To Pay : {days_to_pay}</p>

        <p>Start Date : {start_datetime}</p>

        <p>End Date : {end_datetime}</p>
        """

    if email_type == "BORROWER":
        html += f"""
        <p> The collateral amount has been substracted permanently from your account. </p>
        """
    elif email_type == "LENDER":
        html += f"""
        <p> The collateral amount has been deposited into your account. </p>
        """

    html += """    
        <p>If you think this is an error, please contact support</p>
        </body>
    </html>
    """

    part1 = MIMEText(html, 'html')

    msg.attach(part1)

    context = ssl.create_default_context()
    s = smtplib.SMTP(settings.EMAIL_HOST,port)
    s.starttls(context=context)
    s.ehlo()
    s.login(settings.EMAIL_HOST_USER, settings.NO_REPLY_PASSWORD)
    s.sendmail(settings.EMAIL_HOST_USER, sender_email, msg.as_string())
    s.quit()
    return

def inprogress_transactionb_email(user_email, id_b, transaction_id, currency_name, currency_name_collateral, transaction_type, amount, amount_collateral, interest_rate, days_to_pay, start_datetime, end_datetime):
    port = settings.EMAIL_PORT
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Crypto$hare in progress loan"

    msg['From'] = f"Crypto$hare <{settings.EMAIL_HOST_USER}>"
    msg['To'] = user_email
    
    html = f"""
    <html>
    <head></head>
        <body>
        
        <p>¡Hi there!</p>

        <p>You are receiving this email because a loan has started in <a href="http://www.cryptoshareapp.com/">Crypto$hare</a>.</p>

        <p>The loan details are as follows:</p>

        <p>LoanID : {id_b} </p>

        <p>LoanID : {transaction_id} </p>

        <p> ----------------------------------------- </p>

        <p>Loan Type : {transaction_type}</p>

        <p>Interest Rate : {interest_rate}</p>

        <p>Days To Pay : {days_to_pay}</p>

        <p>Start Date : {start_datetime}</p>

        <p>End Date : {end_datetime}</p>
        
        <p> ----------------------------------------- </p>

        <p>Payment Currency : {currency_name}</p>

        <p>Payment Amount : {amount}</p>

        <p>Collateral Currency : {currency_name_collateral}</p>

        <p>Collateral Amount : {amount_collateral}</p>

        """

    html += """    
        <p>If you think this is an error, please contact support</p>
        </body>
    </html>
    """

    part1 = MIMEText(html, 'html')

    msg.attach(part1)

    context = ssl.create_default_context()
    s = smtplib.SMTP(settings.EMAIL_HOST,port)
    s.starttls(context=context)
    s.ehlo()
    s.login(settings.EMAIL_HOST_USER, settings.NO_REPLY_PASSWORD)
    s.sendmail(settings.EMAIL_HOST_USER, user_email, msg.as_string())
    s.quit()
    return

def test_email(user_email,transaction_id, blockchain, network ,tx_amount, tx_currency, tx_address, creation_date):
    port = settings.EMAIL_PORT
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Crypto$hare in progress loan"

    msg['From'] = f"Crypto$hare <{settings.EMAIL_HOST_USER}>"
    msg['To'] = user_email



    html = send_funds_template(transaction_id, blockchain, network ,tx_amount, tx_currency, tx_address, creation_date)

    part1 = MIMEText(html, 'html')

    msg.attach(part1)

    context = ssl.create_default_context()
    s = smtplib.SMTP(settings.EMAIL_HOST,port)
    s.starttls(context=context)
    s.ehlo()
    s.login(settings.EMAIL_HOST_USER, settings.NO_REPLY_PASSWORD)
    s.sendmail(settings.EMAIL_HOST_USER, user_email, msg.as_string())
    s.quit()
    return
    