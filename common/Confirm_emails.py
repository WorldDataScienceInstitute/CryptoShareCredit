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

# Card_Creation_Email("noreply.Cryptoshare@gmail.com")

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

def Code_Creation_Email(to_addr,pin):
    port = settings.EMAIL_PORT
    htmlpin=pin
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Crypto$hare Confirmation Pin"
    #Code worked on stmp with gmail but not from domain.com
    #msg['From'] = msg['From'] = f"Crypto$hare <{settings.EMAIL_HOST_USER}>"

    msg['From'] = f"Crypto$hare <{settings.EMAIL_HOST_USER}>"
    msg['To'] = to_addr
    
    html = """
    <html>
    <head></head>
        <body>
        
        <p>Hi there!</p>

        <p>This email has been registered for <a href="http://www.cryptoshareapp.com/">Crypto$hare</a> - The First Peer to Peer Lending Platform that allows CryptoCurrency & Physical assets to be used as Collateral!  </p>

        <p>Your registered 6 digit pin for Crypto$hare is the following:</p>

        <big><big><big><big><b>%s</b></big></big></big></big>

        <p>If this was not you, please secure your account at <a href="http://www.cryptoshareapp.com/">Crypto$hare</a></p>
        </body>
    </html>
    """%(pin)

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

 