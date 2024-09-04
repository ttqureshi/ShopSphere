from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg


class Category(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField()
    stock = models.IntegerField(default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name
    
    @property
    def avg_ratings(self):
        average_rating = ReviewRating.objects.filter(product=self).aggregate(Avg('rating'))['rating__avg']
        return average_rating if average_rating is not None else 0

class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.review
    
