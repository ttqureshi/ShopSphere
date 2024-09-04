from django.urls import path, include

from . import views

app_name = "products"

urlpatterns = [
    path("", views.ProductsListingView.as_view(), name="products-listing"),
    path("<int:pk>/", views.ProductDetailView.as_view(), name="detail"),
    path("search/", views.ProductSearchView.as_view(), name="search"),
    path("submit-review/<int:product_id>/", views.SubmitReviewView.as_view(), name="submit-review"),
]
