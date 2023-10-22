from rest_framework import serializers
from .models import *


class DeliveryAddressAPIView(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAddress
        fields = '__all__'
