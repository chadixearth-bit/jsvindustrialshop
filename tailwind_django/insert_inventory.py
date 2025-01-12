import os
import django
import random
from decimal import Decimal
from django.core.files import File
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tailwind_django.settings')
django.setup()

from inventory.models import Brand, Category, Warehouse, InventoryItem

# Create sample brands
brands = [
    "Samsung", "Apple", "Sony", "LG", "Dell", "HP", "Lenovo", "Asus",
    "Acer", "Microsoft"
]

# Create sample categories
categories = [
    "Laptops", "Smartphones", "Tablets", "TVs", "Monitors",
    "Accessories", "Audio", "Gaming", "Networking", "Storage"
]

# Create or get warehouses
attendant_warehouse, _ = Warehouse.objects.get_or_create(name="Attendant Warehouse")
manager_warehouse, _ = Warehouse.objects.get_or_create(name="Manager Warehouse", is_main=True)

# Create brands if they don't exist
brand_objects = []
for brand_name in brands:
    brand, _ = Brand.objects.get_or_create(name=brand_name)
    brand_objects.append(brand)

# Create categories if they don't exist
category_objects = []
for category_name in categories:
    category, _ = Category.objects.get_or_create(name=category_name)
    category_objects.append(category)

# Sample product names and models
product_adjectives = ["Pro", "Elite", "Ultra", "Max", "Plus", "Premium", "Standard", "Basic"]
product_types = ["Book", "Pad", "Station", "Device", "Machine", "Hub", "Box", "Unit"]

def generate_item_data():
    brand = random.choice(brand_objects)
    category = random.choice(category_objects)
    model = f"{random.choice(['A', 'B', 'C', 'D', 'X', 'Y', 'Z'])}{random.randint(1000, 9999)}"
    adjective = random.choice(product_adjectives)
    type_name = random.choice(product_types)
    item_name = f"{brand.name} {adjective} {type_name}"
    price = Decimal(random.uniform(100, 2000)).quantize(Decimal('0.01'))
    stock = random.randint(5, 50)
    
    return {
        'brand': brand,
        'category': category,
        'model': model,
        'item_name': item_name,
        'price': price,
        'stock': stock,
        'description': f"High-quality {category.name.lower()} from {brand.name}. Model: {model}",
    }

# Insert items into attendant warehouse
print("Creating items for Attendant Warehouse...")
for _ in range(50):
    item_data = generate_item_data()
    item = InventoryItem.objects.create(
        warehouse=attendant_warehouse,
        **item_data
    )
    print(f"Created: {item.item_name}")

# Insert items into manager warehouse
print("\nCreating items for Manager Warehouse...")
for _ in range(25):
    item_data = generate_item_data()
    item = InventoryItem.objects.create(
        warehouse=manager_warehouse,
        **item_data
    )
    print(f"Created: {item.item_name}")

print("\nInventory items created successfully!")
print(f"Total items in Attendant Warehouse: {InventoryItem.objects.filter(warehouse=attendant_warehouse).count()}")
print(f"Total items in Manager Warehouse: {InventoryItem.objects.filter(warehouse=manager_warehouse).count()}")
