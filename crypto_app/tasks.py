from celery import shared_task
from .models import Address
from .utils import AddressGenerator

@shared_task
def generate_address_task(coin):
    generator = AddressGenerator()
    address, private_key = generator.generate_address(coin)
    address_obj = Address.objects.create(coin=coin, address=address, private_key=private_key)
    return address_obj.id
