from rest_framework import serializers
from .models import Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'coin', 'address']

class GenerateAddressRequestSerializer(serializers.Serializer):
    coin = serializers.CharField(max_length=3)
