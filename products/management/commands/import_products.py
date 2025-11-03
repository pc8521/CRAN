from django.core.management.base import BaseCommand
import json
import os
from products.models import Product, Category  # Adjust if Category is in another app

class Command(BaseCommand):
    help = "Clear existing products and import filtered products from JSON"

    def handle(self, *args, **kwargs):
        # Locate the JSON file relative to this script
        base_dir = os.path.dirname(__file__)
        file_path = os.path.join(base_dir, "data.json")

        # Load the filtered product data
        try:
            with open(file_path, "r") as f:
                products = json.load(f)
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"❌ File not found: {file_path}"))
            return
        except json.JSONDecodeError:
            self.stderr.write(self.style.ERROR("❌ Failed to parse JSON file."))
            return

        # Clear existing products
        Product.objects.all().delete()
        self.stdout.write(self.style.WARNING("⚠️ All existing products have been deleted."))

        # Import each product
        created_count = 0
        for item in products:
            try:
                # Handle category (ForeignKey)
                category_name = item.get("category")
                category_obj, _ = Category.objects.get_or_create(name=category_name)

                # Handle brand (default to empty string if null)
                brand_value = item.get("brand") or ""

                Product.objects.create(
                    sku=item.get("sku"),
                    name=item.get("name"),
                    description=item.get("description"),
                    price=item.get("price"),
                    stock=item.get("stock"),
                    category=category_obj,
                    brand=brand_value
                )
                created_count += 1
            except Exception as e:
                self.stderr.write(self.style.WARNING(f"⚠️ Skipped product due to error: {e}"))

        self.stdout.write(self.style.SUCCESS(f"✅ Imported {created_count} products successfully."))
