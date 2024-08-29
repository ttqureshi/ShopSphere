from django.test import TestCase
from django.contrib.auth.models import User
from products.models import Category, Product, ReviewRating


class CategoryModelTest(TestCase):
    def test_category_creation(self):
        category = Category.objects.create(name="Electronics")
        self.assertEqual(category.name, "Electronics")
        self.assertEqual(str(category), "Electronics")


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Books")

    def test_product_creation(self):
        product = Product.objects.create(
            name="The Great Gatsby",
            description="A classic novel by F. Scott Fitzgerald",
            price=9.99,
            stock=5,
            category=self.category,
        )
        self.assertEqual(product.name, "The Great Gatsby")
        self.assertEqual(product.price, 9.99)
        self.assertEqual(product.stock, 5)
        self.assertEqual(str(product), "The Great Gatsby")
        self.assertEqual(product.category, self.category)

    def test_product_avg_ratings_no_reviews(self):
        product = Product.objects.create(
            name="The Great Gatsby",
            description="A classic novel by F. Scott Fitzgerald",
            price=9.99,
            stock=5,
            category=self.category,
        )
        self.assertEqual(product.avg_ratings, 0)

    def test_product_avg_ratings_with_reviews(self):
        product = Product.objects.create(
            name="The Great Gatsby",
            description="A classic novel by F. Scott Fitzgerald",
            price=9.99,
            stock=5,
            category=self.category,
        )
        user = User.objects.create_user(username="testuser", password="password")
        ReviewRating.objects.create(product=product, user=user, rating=4.0)
        ReviewRating.objects.create(product=product, user=user, rating=5.0)

        self.assertEqual(product.avg_ratings, 4.5)


class ReviewRatingModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Smartphone",
            description="Latest model with cutting-edge features",
            price=699.99,
            stock=10,
            category=self.category,
        )
        self.user = User.objects.create_user(username="reviewer", password="password")

    def test_review_rating_creation(self):
        review = ReviewRating.objects.create(
            product=self.product,
            user=self.user,
            review="Great phone with excellent battery life.",
            rating=4.5,
        )
        self.assertEqual(str(review), "Great phone with excellent battery life.")
        self.assertEqual(review.rating, 4.5)
        self.assertEqual(review.product, self.product)
        self.assertEqual(review.user, self.user)
