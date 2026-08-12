from rest_framework import serializers

from orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'customer',
            'barber',
            'status',
            'description',
            'endpoint_time',
            'image',
            'created_at',
        )
        read_only_fields = ('customer',)
