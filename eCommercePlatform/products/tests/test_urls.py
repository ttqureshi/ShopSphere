from django.test import SimpleTestCase
from django.urls import reverse, resolve

from products.views import (
    ProductsListingView,
    ProductDetailView,
    ProductSearchView,
    SubmitReviewView,
)


class TestURLs(SimpleTestCase):

    def test_product_listing_url_resolves(self):
        url = reverse("products:products-listing")
        self.assertEquals(resolve(url).func.view_class, ProductsListingView)

    def test_detail_url_resolves(self):
        url = reverse("products:detail", args=[1])
        self.assertEquals(resolve(url).func.view_class, ProductDetailView)

    def test_search_url_resolves(self):
        url = reverse("products:search")
        self.assertEquals(resolve(url).func.view_class, ProductSearchView)

    def test_submit_review_url_resolves(self):
        url = reverse("products:submit-review", args=[1])
        self.assertEquals(resolve(url).func.view_class, SubmitReviewView)
