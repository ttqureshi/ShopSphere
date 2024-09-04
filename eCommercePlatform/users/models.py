from django.db import models
from django.contrib.auth.models import User
from djstripe.models import StripeModel
from django.core.exceptions import ValidationError
import uuid

from products.models import Product


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Product, through="CartItem")


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.quantity * self.product.price


class Order(models.Model):
    DELIVERY_STATUS_CHOICES = {
        ("P", "Pending"),
        ("D", "Delivered"),
    }
    user = models.ForeignKey(User, related_name="orders", on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    full_name = models.CharField(max_length=70)
    contact_no = models.CharField(max_length=13, null=True)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=15)
    state = models.CharField(max_length=15)
    zipcode = models.CharField(max_length=10)
    country = models.CharField(max_length=20)
    status = models.CharField(max_length=1, choices=DELIVERY_STATUS_CHOICES, default="P")

    def save(self, *args, **kwargs):
        if self.status != "P" and not self.orderitem_set.exists():
            raise ValidationError("An order must have at least one order item.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.id} by {self.user.username} placed on {self.order_date}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    @property
    def total_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.quantity} x {self.product} (Order: {self.order.id})"


class Payment(StripeModel):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.order.id}"
