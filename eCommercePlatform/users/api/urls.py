from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.api import views

router = DefaultRouter()

router.register(r"carts", views.CartViewSet)
router.register(r"cartitems", views.CartItemViewSet)
router.register(r"orders", views.OrderViewSet)
router.register(r"orderitems", views.OrderItemViewSet)
router.register(r"users", views.UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
