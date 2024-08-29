from django.test import SimpleTestCase
from django.urls import reverse, resolve

from users.views import (
    RegisterView,
    ProfileView,
    CartView,
    AddToCartView,
    UpdateCartItemView,
    RemoveItemView,
    CheckoutView,
    process_payment,
    OrderListView,
    OrderDetailView,
)


class TestURLs(SimpleTestCase):
    def test_register_url_resolves(self):
        url = reverse("users:register")
        self.assertEquals(resolve(url).func.view_class, RegisterView)

    def test_profile_url_resolves(self):
        url = reverse("users:profile")
        self.assertEquals(resolve(url).func.view_class, ProfileView)

    def test_cart_url_resolves(self):
        url = reverse("users:cart")
        self.assertEquals(resolve(url).func.view_class, CartView)

    def test_add_to_cart_url_resolves(self):
        url = reverse("users:add-to-cart", args=[1])
        self.assertEquals(resolve(url).func.view_class, AddToCartView)

    def test_update_cart_item_url_resolves(self):
        url = reverse("users:update-cart-item", args=[1])
        self.assertEquals(resolve(url).func.view_class, UpdateCartItemView)

    def test_remove_item_url_resolves(self):
        url = reverse("users:remove-item", args=[1])
        self.assertEquals(resolve(url).func.view_class, RemoveItemView)

    def test_checkout_url_resolves(self):
        url = reverse("users:checkout")
        self.assertEquals(resolve(url).func.view_class, CheckoutView)

    def test_process_payment_url_resolves(self):
        url = reverse("users:process-payment", args=[1])
        self.assertEquals(resolve(url).func, process_payment)

    def test_orders_url_resolves(self):
        url = reverse("users:orders")
        self.assertEquals(resolve(url).func.view_class, OrderListView)

    def test_order_detail_url_resolves(self):
        url = reverse("users:order-detail", args=[1])
        self.assertEquals(resolve(url).func.view_class, OrderDetailView)

