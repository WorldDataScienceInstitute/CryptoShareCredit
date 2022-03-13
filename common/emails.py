import smtplib,ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings


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
    s = smtplib.SMTP('smtp.domain.com',port)
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
    s = smtplib.SMTP('smtp.domain.com',port)
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
    s = smtplib.SMTP('smtp.domain.com',port)
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
    s = smtplib.SMTP('smtp.domain.com',port)
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
    s = smtplib.SMTP('smtp.domain.com',port)
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
    s = smtplib.SMTP('smtp.domain.com',port)
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

        <p>Please have in mind that for security reasons the assigned deposit address is changed when a deposit is made or every 6 days, whichever ocurrs first.</p>

        <p>For making a new Crypto Deposit, please go to <a href="https://www.cryptoshareapp.com/atm/DepositCrypto/">Crypto$hare Deposit Crypto</a> and generate a new deposit address</p>

        <p>Customer Support Transaction ID:  <b style="color: red">{transaction_id}</b> </p>

        <p>If this was not you, please secure your account at <a href="http://www.cryptoshareapp.com/">Crypto$hare</a>.</p>
        </body>
    </html>
    """

    part1 = MIMEText(html, 'html')

    msg.attach(part1)

    context = ssl.create_default_context()
    s = smtplib.SMTP('smtp.domain.com',port)
    s.starttls(context=context)
    s.ehlo()
    s.login(settings.EMAIL_HOST_USER, settings.NO_REPLY_PASSWORD)
    s.sendmail(settings.EMAIL_HOST_USER, sender_email, msg.as_string())
    s.quit()
    return