from rest_framework import generics, status, serializers
from rest_framework.response import Response
from .models import Address
from .serializers import AddressSerializer, GenerateAddressRequestSerializer
from .tasks import generate_address_task
from django.conf import settings
from drf_spectacular.utils import extend_schema, inline_serializer


class GenerateAddressView(generics.CreateAPIView):
    serializer_class = GenerateAddressRequestSerializer

    # DRF_spectacular schema
    @extend_schema(
        request=GenerateAddressRequestSerializer,
        responses={
            202: inline_serializer(
                "GenerateAddressResponseSuccessSerializer",
                {
                    "task_id": serializers.CharField(max_length=100),
                    "message": serializers.CharField(max_length=100),
                },
            ),
            400: inline_serializer(
                "GenerateAddressResponseErrorSerializer",
                {"error": serializers.CharField(max_length=100)},
            ),
        },
    )
    def post(self, request):
        # Get the coin from the request data
        coin = request.data.get("coin")

        # Check if the coin is supported
        if coin not in settings.CRYPTO_APP_COINS:
            return Response(
                {"error": f"Unsupported coin: {coin}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Call the Celery task to generate an address asynchronously
        task = generate_address_task.delay(coin)

        # Return a response with the task ID and a message
        return Response(
            {"task_id": task.id, "message": f"Generating an address for {coin}"},
            status=status.HTTP_202_ACCEPTED,
        )


class ListAddressView(generics.ListAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class RetrieveAddressView(generics.RetrieveAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
