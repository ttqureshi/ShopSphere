from django.urls import path, include
from rest_framework.routers import DefaultRouter

from products.api import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'reviews', views.ReviewRatingViewSet, basename='reviewrating')

urlpatterns = [
    path('', include(router.urls)),
]
