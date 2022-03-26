from itertools import count
from celery import Celery
from atm_functions.models import Cryptocurrency

app = Celery('ATM')

@app.task
def test():
    counter = Cryptocurrency.objects.all().count()
    c = Cryptocurrency(currency__name=f"Test{counter}", contract=f"0x0_{counter}", wallet_address="0x0", blockchain="0x0", network="0x0", symbol="0x0")
    c.save()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))