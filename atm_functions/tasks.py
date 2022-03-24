from celery import Celery
from atm_functions.models import Cryptocurrency

app = Celery('ATM')

@app.task(bind=True)
def debug_task(self):

    print('Request: {0!r}'.format(self.request))
    c_test = Cryptocurrency(currency_name="C_Test", contract="0x0", wallet_address="0x0", blockchain="0x0", network="0x0", symbol="0x0")
    c_test.save() 