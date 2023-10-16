from celery import shared_task
from .models import Address
from .utils import get_address_generator

@shared_task
def generate_address_task(coin):
    generator = get_address_generator(coin)
    address, private_key = generator.generate_address()
    address_obj = Address.objects.create(coin=coin, address=address, private_key=private_key)
    return address_obj.id
