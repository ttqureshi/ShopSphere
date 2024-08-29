from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Product, Category, ReviewRating


class TestProductsListingView(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.product1 = Product.objects.create(
            name="Phone",
            description="A smartphone",
            category=self.category,
            price=10000,
            image_url="https://media.wisemarket.com.pk/variant/inventory_26455.webp",
        )
        self.product2 = Product.objects.create(
            name="Laptop",
            description="A laptop",
            category=self.category,
            price=100000,
            image_url="https://cdn.ttgtmedia.com/rms/onlineimages/hp_elitebook_mobile.jpg",
        )

    def test_products_listing_view(self):
        response = self.client.get(reverse("products:products-listing"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/products_listing.html")
        self.assertContains(response, self.product1)
        self.assertContains(response, self.product2)

    def test_products_listing_view_with_category_filter(self):
        response = self.client.get(
            reverse("products:products-listing"), {"category": "Electronics"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product1)
        self.assertContains(response, self.product2)


class TestProductDetailView(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Phone",
            description="A smartphone",
            category=self.category,
            price=10000,
            image_url="https://media.wisemarket.com.pk/variant/inventory_26455.webp",
        )
        self.user = User.objects.create_user(username="testuser", password="password")
        self.review = ReviewRating.objects.create(
            product=self.product, user=self.user, review="Great product!", rating=5
        )

    def test_product_detail_view(self):
        response = self.client.get(reverse("products:detail", args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/product_detail.html")
        self.assertContains(response, self.product)
        self.assertContains(response, self.review.review)


class TestProductSearchView(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Phone",
            description="A smartphone",
            category=self.category,
            price=10000,
            image_url="https://media.wisemarket.com.pk/variant/inventory_26455.webp",
        )

    def test_product_search_view(self):
        response = self.client.get(reverse("products:search"), {"search": "smartphone"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/search.html")
        self.assertIn(self.product, response.context["search_results"])
        self.assertEqual(response.context["search_query"], "smartphone")


class TestSubmitReviewView(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Phone",
            description="A smartphone",
            category=self.category,
            price=10000,
            image_url="https://media.wisemarket.com.pk/variant/inventory_26455.webp",
        )
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")

    def test_submit_review_view_new_review(self):
        form_data = {
            "review": "Great product!",
            "rating": 5,
        }
        response = self.client.post(
            reverse("products:submit-review", args=[self.product.id]), form_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            ReviewRating.objects.filter(product=self.product, user=self.user).exists()
        )

    def test_submit_review_view_update_review(self):
        ReviewRating.objects.create(
            product=self.product,
            user=self.user,
            review="Good product.",
            rating=4,
        )
        form_data = {
            "review": "Updated review: Excellent product!",
            "rating": 5,
        }
        response = self.client.post(
            reverse("products:submit-review", args=[self.product.id]), form_data
        )
        self.assertEqual(response.status_code, 302)
        updated_review = ReviewRating.objects.get(product=self.product, user=self.user)
        self.assertEqual(updated_review.review, "Updated review: Excellent product!")
