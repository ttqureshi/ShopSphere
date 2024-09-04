from rest_framework import serializers
from django.contrib.auth.models import User

from products.models import Category, Product, ReviewRating


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["url", "id", "name"]


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )
    category_name = serializers.SerializerMethodField(read_only=True)
    reviews = serializers.HyperlinkedRelatedField(
        many=True, view_name="reviewrating-detail", read_only=True
    )

    class Meta:
        model = Product
        fields = [
            "url",
            "id",
            "name",
            "description",
            "price",
            "image",
            "stock",
            "category_id",
            "category_name",
            "reviews",
        ]

    def get_category_name(self, obj):
        return obj.category.name


class ReviewRatingSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    product = serializers.HyperlinkedRelatedField(
        view_name="product-detail", read_only=True
    )

    class Meta:
        model = ReviewRating
        fields = ["url", "id", "product", "user", "review", "rating", "created_at"]
