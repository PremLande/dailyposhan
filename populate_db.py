#!/usr/bin/env python3
"""
Populate SQLite database with sample products for testing
"""

import os
import sys
import django

# Add the backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend-django'))

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dailyposhan_backend.settings')
django.setup()

from apps.products.models import Product

def populate_products():
    """Add sample products to the database"""

    products_data = [
        {
            'id': 1,
            'name': 'Muscle Fuel Jar',
            'price': 249,
            'calories': 420,
            'protein': '34g',
            'description': 'Grilled chicken, boiled eggs, quinoa, kidney beans, broccoli, cherry tomatoes with herb vinaigrette',
            'stock': 50,
            'is_active': True,
        },
        {
            'id': 2,
            'name': 'Glow & Flow Jar',
            'price': 229,
            'calories': 310,
            'protein': '14g',
            'description': 'Pomegranate seeds, avocado, beetroot, walnuts, spinach, feta, cucumber with lemon-turmeric dressing',
            'stock': 45,
            'is_active': True,
        },
        {
            'id': 3,
            'name': 'Chatori Jar',
            'price': 199,
            'calories': 260,
            'protein': '12g',
            'description': 'Sprouts, corn, raw mango, onion, green chutney, sev, chaat masala � the ultimate desi jar salad',
            'stock': 40,
            'is_active': True,
        },
    ]

    for product_data in products_data:
        product, created = Product.objects.get_or_create(
            id=product_data['id'],
            defaults=product_data
        )
        if created:
            print(f"✓ Created product: {product.name}")
        else:
            # Update existing product
            for key, value in product_data.items():
                setattr(product, key, value)
            product.save()
            print(f"✓ Updated product: {product.name}")

    print(f"\n✅ Database populated with {len(products_data)} products")

if __name__ == '__main__':
    populate_products()