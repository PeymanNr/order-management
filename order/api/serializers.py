from rest_framework import serializers
from order.models import Order


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.id")

    class Meta:
        model = Order
        fields = [
            "id",
            "product_name",
            "quantity",
            "price",
            "created_at",
            "updated_at",
            "user",
        ]
