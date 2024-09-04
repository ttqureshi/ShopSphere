from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView

from . import views

app_name = "users"  # designates that these urls are inside the users app

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path(
        "login/", 
        LoginView.as_view(
            template_name='users/login.html', 
            redirect_authenticated_user=True, 
            next_page='products:products-listing'
        ), 
        name="login"
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="products:products-listing"),
        name="logout",
    ),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("cart/", views.CartView.as_view(), name="cart"),
    path("add-to-cart/<int:product_id>", views.AddToCartView.as_view(), name="add-to-cart"),
    path(
        "update-cart-item/<int:product_id>",
        views.UpdateCartItemView.as_view(),
        name="update-cart-item",
    ),
    path("remove-item/<int:product_id>", views.RemoveItemView.as_view(), name="remove-item"),
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("orders/", views.OrderListView.as_view(), name="orders"),
    path("order-detail/<int:order_id>", views.OrderDetailView.as_view(), name="order-detail"),
]
