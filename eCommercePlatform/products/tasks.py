from celery import shared_task
from django.conf import settings
from django.core.files.storage import default_storage
import csv


@shared_task
def update_add_products_from_csv(file_path):
    from .models import Category, Product

    with default_storage.open(file_path, "r") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            if row:
                category = Category.objects.get(id=row["category_id"])
                product, _ = Product.objects.update_or_create(
                    name=row["name"],
                    category=category,
                    defaults={
                        "name": row["name"],
                        "description": row["description"],
                        "price": row["price"],
                        "image_url": row["image_url"],
                        "stock": row["stock"],
                        "category": category,
                    },
                )
    default_storage.delete(file_path)
