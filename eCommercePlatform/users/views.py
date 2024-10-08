from django.db.models.base import Model as Model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.db import transaction
from django.http import Http404
from django.conf import settings
import stripe
import time

from .forms import UserRegisterForm, OrderForm, UserUpdateForm
from products.models import Product
from .models import Cart, CartItem, Order, OrderItem, Payment
from .tasks import send_sms


class RegisterView(View):
    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            cart = Cart(user=request.user)
            cart.save()
            return redirect("products:products-listing")
        return render(request, "users/register.html", {"form": form})

    def get(self, request):
        form = UserRegisterForm()
        context = {"form": form}
        return render(request, "users/register.html", context)


class ProfileView(LoginRequiredMixin, View):
    login_url = "/users/login"

    def post(self, request):
        user_form = UserUpdateForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(user=request.user, data=request.POST)

        if user_form.is_valid() and password_form.is_valid():
            user_form.save()
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your profile has been updated successfully.")
            return redirect("users:profile")
        else:
            error_message = (
                "Password change unsuccessful. Please correct the errors below."
            )
            if "password_form" in locals() and password_form.errors:
                error_message += f' Reason: {", ".join([", ".join(errors) for errors in password_form.errors.values()])}'
            messages.error(request, error_message)

            context = {"user_form": user_form, "password_form": password_form}
            return render(request, "users/user_profile.html", context)

    def get(self, request):
        user_form = UserUpdateForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)

        context = {"user_form": user_form, "password_form": password_form}
        return render(request, "users/user_profile.html", context)


class CartView(LoginRequiredMixin, DetailView):
    login_url = "/users/login"

    model = Cart
    template_name = "users/cart.html"
    context_object_name = "cart"

    def get_object(self, queryset=None):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = self.object.cartitem_set.select_related("product").all()
        context["total_price"] = sum(
            item.quantity * item.product.price for item in items
        )
        return context


class AddToCartView(LoginRequiredMixin, View):
    login_url = "/users/login"

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        in_stock = product.stock > 0

        if in_stock:
            cart = Cart.objects.get(user=request.user)
            cart_item, is_created = CartItem.objects.get_or_create(
                cart=cart, product=product
            )

            if not is_created:
                cart_item.quantity += 1
                cart_item.save()
            else:
                cart_item.quantity = 1

        return redirect("products:products-listing")


class UpdateCartItemView(LoginRequiredMixin, View):
    login_url = "/users/login"

    def post(self, request, product_id):
        cart = Cart.objects.get(user=request.user)
        cart_item = cart.cartitem_set.get(product_id=product_id)
        product = Product.objects.get(id=product_id)
        stock_left = product.stock
        quantity = int(request.POST.get("quantity"))
        if quantity <= stock_left:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            messages.warning(
                request, f"Only {stock_left} {product.name} left in stock."
            )
        return redirect("users:cart")

    def get(self, request):
        return redirect("users:cart")


class RemoveItemView(LoginRequiredMixin, View):
    login_url = "/users/login"

    def post(self, request, product_id):
        cart = Cart.objects.get(user=request.user)
        cart_item = cart.cartitem_set.get(product_id=product_id)
        cart_item.delete()
        return redirect("users:cart")


class CheckoutView(LoginRequiredMixin, FormView):
    login_url = "/users/login"

    template_name = "users/checkout.html"
    form_class = OrderForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = get_object_or_404(Cart, user=self.request.user)
        items = cart.cartitem_set.select_related("product").all()
        total_price = sum(item.quantity * item.product.price for item in items)
        context.update(
            {
                "cart": cart,
                "total_price": total_price,
            }
        )
        return context

    def form_valid(self, form):
        cart = get_object_or_404(Cart, user=self.request.user)
        items = cart.cartitem_set.select_related("product").all()
        total_price = sum(item.quantity * item.product.price for item in items)

        with transaction.atomic():
            order = form.save(commit=False)
            order.user = self.request.user
            order.total_price = total_price
            order.save()

            payment = Payment(order=order, amount=total_price, user=self.request.user)
            payment.save()

            stripe.api_key = settings.STRIPE_PRIVATE_KEY
            intent = stripe.PaymentIntent.create(
                amount=int(payment.amount * 100),
                currency="usd",
                automatic_payment_methods={"enabled": True},
                metadata={"payment_id": payment.id},
            )

        return redirect("users:process-payment", client_secret=intent.client_secret)


def process_payment(request, client_secret):
    if request.method == "POST":
        stripe.api_key = settings.STRIPE_PRIVATE_KEY
        try:
            payment_intent_id = (
                client_secret.split("_")[0] + "_" + client_secret.split("_")[1]
            )
            time.sleep(1)
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)

            if intent.status == "succeeded":
                payment_id = intent.metadata["payment_id"]
                payment = Payment.objects.get(id=payment_id)
                payment.paid = True
                payment.save()

                cart = get_object_or_404(Cart, user=payment.user)
                items = cart.cartitem_set.select_related("product").all()
                order = payment.order

                for cart_item in items:
                    OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        quantity=cart_item.quantity,
                    )
                    product = Product.objects.get(id=cart_item.product.id)
                    product.stock -= cart_item.quantity
                    product.save()
                cart.cartitem_set.all().delete()
                order.status = "D"
                order.save()
                messages.success(request, "Payment successful!")
                send_sms.delay(order.id)
                return render(
                    request, "users/order_confirmation.html", {"order": order}
                )
            else:
                messages.error(
                    request,
                    f"Couldn't process payment. Please check your credentials and try again",
                )

        except stripe.error.StripeError as e:
            messages.error(request, f"Payment failed: {e.user_message}")

    context = {"client_secret": client_secret}
    return render(request, "users/process_payment.html", context)


class OrderListView(LoginRequiredMixin, ListView):
    login_url = "/users/login"

    model = Order
    template_name = "users/order_history.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderDetailView(LoginRequiredMixin, DetailView):
    login_url = "/users/login"

    model = Order
    template_name = "users/order_detail.html"
    context_object_name = "order"

    def get_object(self):
        order_id = self.kwargs.get("order_id")
        order = get_object_or_404(Order, id=order_id)
        if order and order.user == self.request.user:
            return order
        else:
            raise Http404

