from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from .tasks import generate_address_task
from .models import Address
import coinaddrvalidator
    
# Define a test class for the celery task
class GenerateAdressTaskTest(TestCase):
    # Define a test method that checks if the task is correctly creating the data in the database
    def test_generate_address(self):
        # Call the generate_address_task function with BTC
        id = generate_address_task('BTC')
        address_obj = Address.objects.get(id=id)
        self.assertEqual(address_obj.id, 1)
        validation_result = coinaddrvalidator.validate('btc', address_obj.address)
        self.assertTrue(validation_result.valid)

        # Call the generate_address_task function with BNB (unsupported)
        self.assertRaises(ValueError, generate_address_task, coin='BNB')

# Define a test class for the Address model
class AddressModelTest(TestCase):
    # Define a setup method that runs before each test method
    def setUp(self):
        # Create some sample addresses for testing
        Address.objects.create(coin='BTC', address='2N3kfQkYDH48Z4ZR88uaytLHNVbNJowjTym', private_key='0x123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef')
        Address.objects.create(coin='ETH', address='0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B', private_key='0xabcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789')
    
    # Define a test method that checks the string representation of the Address model
    def test_str(self):
        # Get the first address from the database
        btc_address = Address.objects.get(id=1)
        
        # Check that its string representation is equal to its address field
        self.assertEqual(str(btc_address), btc_address.address)
        
        # Get the second address from the database
        eth_address = Address.objects.get(id=2)
        
        # Check that its string representation is equal to its address field
        self.assertEqual(str(eth_address), eth_address.address)

# Define a test class for the API views
class APIViewsTest(APITestCase):
    # Define a setup method that runs before each test method
    def setUp(self):
        # Create an API client object for sending requests
        self.client = APIClient()
        # Create some sample addresses for testing
        Address.objects.create(coin='BTC', address='2N3kfQkYDH48Z4ZR88uaytLHNVbNJowjTym', private_key='0x123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef')
        Address.objects.create(coin='ETH', address='0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B', private_key='0xabcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789')
    
    # Define a test method that checks the generate view
    def test_generate(self):
        # Send a POST request to the generate endpoint with an invalid coin as data
        response = self.client.post(reverse('generate'), {'coin': 'BNB'})

        # Check that the response status code is 400 (bad request)
        self.assertEqual(response.status_code, 400)
        
        # Check that the response data contains an error message
        self.assertIn('error', response.data)

    # Define a test method that checks the list view
    def test_list(self):
        # Send a GET request to the list endpoint
        response = self.client.get(reverse('list'))
        
        # Check that the response status code is 200 (ok)
        self.assertEqual(response.status_code, 200)
        
        # Check that the response data is a list of two addresses
        self.assertEqual(len(response.data), 2)
        
        # Check that the first address in the list has the correct fields and values
        self.assertEqual(response.data[0]['id'], 1)
        self.assertEqual(response.data[0]['coin'], 'BTC')
        self.assertEqual(response.data[0]['address'], '2N3kfQkYDH48Z4ZR88uaytLHNVbNJowjTym')
        
        # Check that the second address in the list has the correct fields and values
        self.assertEqual(response.data[1]['id'], 2)
        self.assertEqual(response.data[1]['coin'], 'ETH')
        self.assertEqual(response.data[1]['address'], '0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B')
    
    # Define a test method that checks the retrieve view
    def test_retrieve(self):
        # Send a GET request to the retrieve endpoint with a valid ID as parameter
        response = self.client.get(reverse('retrieve', kwargs={'pk': 1}))
        
        # Check that the response status code is 200 (ok)
        self.assertEqual(response.status_code, 200)
        
        # Check that the response data is an address with the correct fields and values
        self.assertEqual(response.data['id'], 1)
        self.assertEqual(response.data['coin'], 'BTC')
        self.assertEqual(response.data['address'], '2N3kfQkYDH48Z4ZR88uaytLHNVbNJowjTym')
        
        # Send a GET request to the retrieve endpoint with an invalid ID as parameter
        response = self.client.get(reverse('retrieve', kwargs={'pk': 3}))
        
        # Check that the response status code is 404 (not found)
        self.assertEqual(response.status_code, 404)
