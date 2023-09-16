from django.db import models

class Address(models.Model):
    coin = models.CharField(max_length=3) # The coin acronym, such as BTC or ETH
    address = models.CharField(max_length=50) # The generated address
    private_key = models.CharField(max_length=64) # The private key in hex format
    
    def __str__(self):
        return self.address