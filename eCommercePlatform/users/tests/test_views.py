from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from unittest.mock import patch
from django.utils import timezone
import stripe

from users.forms import UserRegisterForm, UserUpdateForm, OrderForm
from users.models import Cart, CartItem, Order, OrderItem, Payment
from products.models import Product, Category


class TestRegisterView(TestCase):

    def test_register_GET(self):
        response = self.client.get(reverse("users:register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/register.html")
        self.assertIsInstance(response.context["form"], UserRegisterForm)

    def test_register_POST_valid(self):
        form_data = {
            "username": "testuser",
            "email": "testuser@gmail.com",
            "password1": "testpassword123",
            "password2": "testpassword123",
        }
        response = self.client.post(reverse("users:register"), form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("products:products-listing"))
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_register_POST_invalid(self):
        form_data = {
            "username": "testuser",
            "email": "testuser@gmail.com",
            "password1": "testpassword123",
            "password2": "differentpassword",
        }
        response = self.client.post(reverse("users:register"), form_data)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/register.html")


class TestProfileView(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword123"
        )
        self.client.login(username="testuser", password="testpassword123")

    def test_profile_GET(self):
        response = self.client.get(reverse("users:profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/user_profile.html")
        self.assertIsInstance(response.context["user_form"], UserUpdateForm)

    def test_profile_POST_valid(self):
        form_data = {
            "username": "newusername",
            "email": "newemail@example.com",
            "old_password": "testpassword123",
            "new_password1": "newpassword123",
            "new_password2": "newpassword123",
        }
        response = self.client.post(reverse("users:profile"), form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("users:profile"))
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "newusername")
        self.assertTrue(
            self.client.login(username="newusername", password="newpassword123")
        )

    def test_profile_POST_invalid(self):
        form_data = {
            "username": "newusername",
            "email": "newemail@example.com",
            "old_password": "testpassword123",
            "new_password1": "newpassword123",
            "new_password2": "differentpassword",
        }
        response = self.client.post(reverse("users:profile"), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/user_profile.html")


class TestCartView(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword123"
        )
        self.client.login(username="testuser", password="testpassword123")
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Phone",
            description="A smartphone",
            category=self.category,
            price=10000,
            image_url="https://media.wisemarket.com.pk/variant/inventory_26455.webp",
        )
        self.cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)

    def test_cart_GET(self):
        response = self.client.get(reverse("users:cart"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/cart.html")
        self.assertContains(response, self.product)


class TestAddToCartView(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword123"
        )
        self.client.login(username="testuser", password="testpassword123")
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Phone",
            description="A smartphone",
            category=self.category,
            price=10000,
            image_url="https://media.wisemarket.com.pk/variant/inventory_26455.webp",
        )
        self.cart = Cart.objects.create(user=self.user)

    def test_add_to_cart_POST(self):
        response = self.client.post(
            reverse("users:add-to-cart", args=[self.product.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("products:products-listing"))
        cart = Cart.objects.get(user=self.user)
        self.assertTrue(
            CartItem.objects.filter(cart=cart, product=self.product).exists()
        )


class TestUpdateCartItemView(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword123"
        )
        self.client.login(username="testuser", password="testpassword123")
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Phone",
            description="A smartphone",
            category=self.category,
            price=10000,
            stock=5,
            image_url="https://media.wisemarket.com.pk/variant/inventory_26455.webp",
        )
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(
            cart=self.cart, product=self.product, quantity=2
        )

    def test_update_cart_item_POST_valid(self):
        response = self.client.post(
            reverse("users:update-cart-item", args=[self.product.id]), {"quantity": 3}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("users:cart"))
        self.cart_item.refresh_from_db()
        self.assertEqual(self.cart_item.quantity, 3)

    def test_update_cart_item_POST_invalid(self):
        response = self.client.post(
            reverse("users:update-cart-item", args=[self.product.id]), {"quantity": 10}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("users:cart"))
        self.cart_item.refresh_from_db()
        self.assertEqual(self.cart_item.quantity, 2)


class TestRemoveItemView(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword123"
        )
        self.client.login(username="testuser", password="testpassword123")
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Phone",
            description="A smartphone",
            category=self.category,
            price=10000,
            stock=5,
            image_url="https://media.wisemarket.com.pk/variant/inventory_26455.webp",
        )
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(
            cart=self.cart, product=self.product, quantity=2
        )

    def test_remove_item_POST(self):
        response = self.client.post(
            reverse("users:remove-item", args=[self.product.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("users:cart"))
        self.assertFalse(
            CartItem.objects.filter(cart=self.cart, product=self.product).exists()
        )


class TestCheckoutView(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword123"
        )
        self.client.login(username="testuser", password="testpassword123")
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Phone",
            description="A smartphone",
            category=self.category,
            price=10000,
            stock=5,
            image_url="https://media.wisemarket.com.pk/variant/inventory_26455.webp",
        )
        self.cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)

    def test_checkout_GET(self):
        response = self.client.get(reverse("users:checkout"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/checkout.html")
        self.assertIsInstance(response.context["form"], OrderForm)

    def test_checkout_POST(self):
        form_data = {
            "full_name": "Test User",
            "contact_no": "1234567890",
            "address": "123 Test Street",
            "city": "Test City",
            "state": "Test State",
            "zipcode": "12345",
            "country": "Test Country",
        }
        response = self.client.post(reverse("users:checkout"), form_data)
        self.assertEqual(response.status_code, 302)
        client_secret = response.url.split("/")[-2]
        self.assertRedirects(
            response, reverse("users:process-payment", args=[client_secret])
        )


class OrderViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword123"
        )
        self.client.login(username="testuser", password="testpassword123")
        self.other_user = User.objects.create_user(
            username="otheruser", password="password456"
        )
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Phone",
            description="A smartphone",
            category=self.category,
            price=10000,
            stock=50,
            image_url="https://media.wisemarket.com.pk/variant/inventory_26455.webp",
        )

        self.order1 = Order.objects.create(
            user=self.user,
            total_price=100.00,
            full_name="Test User",
            contact_no="123456789",
            address="123 Test Street",
            city="Test City",
            state="Test State",
            zipcode="12345",
            country="Test Country",
            order_date=timezone.now(),
        )
        self.orderitem1 = OrderItem.objects.create(
            order=self.order1, product=self.product, quantity=5
        )
        self.order2 = Order.objects.create(
            user=self.user,
            total_price=150.00,
            full_name="Test User",
            contact_no="123456789",
            address="123 Test Street",
            city="Test City",
            state="Test State",
            zipcode="12345",
            country="Test Country",
            order_date=timezone.now(),
        )
        self.orderitem2 = OrderItem.objects.create(
            order=self.order2, product=self.product, quantity=10
        )
        self.other_user_order = Order.objects.create(
            user=self.other_user,
            total_price=200.00,
            full_name="Other User",
            contact_no="987654321",
            address="456 Other Street",
            city="Other City",
            state="Other State",
            zipcode="54321",
            country="Other Country",
            status="P",
            order_date=timezone.now(),
        )
        self.orderitem3 = OrderItem.objects.create(
            order=self.other_user_order, product=self.product, quantity=2
        )

    def test_order_list_view(self):
        response = self.client.get(reverse("users:orders"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/order_history.html")
        orders = response.context["orders"]
        self.assertIn(self.order1, orders)
        self.assertIn(self.order2, orders)
        self.assertNotIn(self.other_user_order, orders)

    def test_order_list_view_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("users:orders"))
        self.assertEqual(response.status_code, 302)

    def test_order_detail_view(self):
        response = self.client.get(reverse("users:order-detail", args=[self.order1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/order_detail.html")
        order = response.context["order"]
        self.assertEqual(order, self.order1)

    def test_order_detail_view_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("users:order-detail", args=[self.order1.id]))
        self.assertEqual(response.status_code, 302)

    def test_order_detail_view_other_user(self):
        response = self.client.get(
            reverse("users:order-detail", args=[self.other_user_order.id])
        )
        self.assertEqual(response.status_code, 404)
