from django.test import TestCase
from django.contrib.auth.models import User

from products.models import Product, Category
from users.models import Cart, CartItem, Order, OrderItem, Payment

class CartModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Phone",
            description="A smartphone",
            stock=10,
            category=self.category,
            price=100,
            image_url="https://media.wisemarket.com.pk/variant/inventory_26455.webp",
        )

    def test_cart_creation(self):
        cart = Cart.objects.create(user=self.user)
        self.assertEqual(cart.user, self.user)

    def test_cart_items(self):
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)
        self.assertEqual(cart.items.count(), 1)

    def test_cart_item_total_price(self):
        cart = Cart.objects.create(user=self.user)
        cart_item = CartItem.objects.create(cart=cart, product=self.product, quantity=3)
        self.assertEqual(cart_item.total_price, 300.00)


class OrderModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Phone",
            description="A smartphone",
            stock=10,
            category=self.category,
            price=100,
            image_url="https://media.wisemarket.com.pk/variant/inventory_26455.webp",
        )

    def test_order_creation(self):
        order = Order.objects.create(
            user=self.user,
            total_price=200.00,
            full_name="John Doe",
            contact_no="1234567890",
            address="123 Main St",
            city="Test City",
            state="Test State",
            zipcode="12345",
            country="Test Country",
        )
        self.assertEqual(order.user, self.user)

    def test_order_item_creation(self):
        order = Order.objects.create(
            user=self.user,
            total_price=200.00,
            full_name="John Doe",
            contact_no="1234567890",
            address="123 Main St",
            city="Test City",
            state="Test State",
            zipcode="12345",
            country="Test Country",
        )
        order_item = OrderItem.objects.create(order=order, product=self.product, quantity=2)
        self.assertEqual(order.orderitem_set.count(), 1)
        self.assertEqual(order_item.total_price, 200.00)


class PaymentModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.order = Order.objects.create(
            user=self.user,
            total_price=200.00,
            full_name="John Doe",
            contact_no="1234567890",
            address="123 Main St",
            city="Test City",
            state="Test State",
            zipcode="12345",
            country="Test Country",
        )

    def test_payment_creation(self):
        payment = Payment.objects.create(user=self.user, order=self.order, amount=200.00, paid=True)
        self.assertEqual(payment.user, self.user)
        self.assertTrue(payment.paid)

    def test_payment_string_representation(self):
        payment = Payment.objects.create(user=self.user, order=self.order, amount=200.00)
        self.assertEqual(str(payment), f"{self.user.username} - {self.order.id}")
