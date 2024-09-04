from rest_framework import serializers
from django.contrib.auth.models import User
from django.urls import reverse

from users.models import Cart, CartItem, Order, OrderItem


class UserSerializer(serializers.HyperlinkedModelSerializer):
    orders = serializers.HyperlinkedRelatedField(
        many=True, view_name="order-detail", read_only=True
    )

    class Meta:
        model = User
        fields = ["url", "id", "username", "orders"]


class CartItemSerializer(serializers.HyperlinkedModelSerializer):
    product_name = serializers.ReadOnlyField(source="product.name")

    class Meta:
        model = CartItem
        fields = ["url", "product_name", "quantity", "total_price"]


class CartSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    items = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["url", "user", "items"]

    def get_items(self, obj):
        cart_items = CartItem.objects.filter(cart=obj)
        return [
            {
                "product_name": item.product.name,
                "quantity": item.quantity,
                "total_price": item.total_price,
            }
            for item in cart_items
        ]


class OrderItemSerializer(serializers.HyperlinkedModelSerializer):
    product_name = serializers.ReadOnlyField(source="product.name")

    class Meta:
        model = OrderItem
        fields = ["url", "product_name", "quantity", "total_price"]


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    ordered_items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "url",
            "user",
            "order_date",
            "total_price",
            "full_name",
            "address",
            "city",
            "state",
            "zipcode",
            "country",
            "ordered_items",
        ]

    def get_ordered_items(self, obj):
        items = OrderItem.objects.filter(order=obj)
        return [
            {
                "product_name": item.product.name,
                "unit_price": item.product.price,
                "quantity": item.quantity,
            }
            for item in items
        ]
