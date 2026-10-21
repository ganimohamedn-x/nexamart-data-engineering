
import csv
import random
from datetime import date, timedelta
from pathlib import Path
from tempfile import template

# Locate the project and data folders
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# Configuration
NUMBER_OF_PRODUCTS = 30
OUTPUT_FILE = DATA_DIR / "products.csv"

product_catalog = [
    {"name": "Wireless Headphones", "category": "Electronics", "min_price": 30, "max_price": 180},
    {"name": "Bluetooth Speaker", "category": "Electronics", "min_price": 20, "max_price": 120},
    {"name": "USB-C Charger", "category": "Electronics", "min_price": 10, "max_price": 50},
    {"name": "Laptop Stand", "category": "Electronics", "min_price": 15, "max_price": 80},
    {"name": "Smart Watch", "category": "Electronics", "min_price": 40, "max_price": 300},
    {"name": "Cotton T-Shirt", "category": "Clothing", "min_price": 8, "max_price": 35},
    {"name": "Denim Jeans", "category": "Clothing", "min_price": 25, "max_price": 90},
    {"name": "Running Shoes", "category": "Clothing", "min_price": 35, "max_price": 150},
    {"name": "Winter Jacket", "category": "Clothing", "min_price": 40, "max_price": 200},
    {"name": "Backpack", "category": "Accessories", "min_price": 15, "max_price": 100},
    {"name": "Leather Wallet", "category": "Accessories", "min_price": 10, "max_price": 75},
    {"name": "Sunglasses", "category": "Accessories", "min_price": 10, "max_price": 120},
    {"name": "Coffee Maker", "category": "Home", "min_price": 25, "max_price": 160},
    {"name": "Desk Lamp", "category": "Home", "min_price": 12, "max_price": 90},
    {"name": "Water Bottle", "category": "Home", "min_price": 8, "max_price": 40},
    {"name": "Yoga Mat", "category": "Fitness", "min_price": 15, "max_price": 70},
    {"name": "Dumbbell Set", "category": "Fitness", "min_price": 30, "max_price": 180},
    {"name": "Football", "category": "Sports", "min_price": 12, "max_price": 60},
    {"name": "Cookbook", "category": "Books", "min_price": 10, "max_price": 45},
    {"name": "Notebook Set", "category": "Stationery", "min_price": 5, "max_price": 25},
    {"name": "Mechanical Keyboard", "category": "Electronics", "min_price": 35, "max_price": 200},
    {"name": "Travel Mug", "category": "Home", "min_price": 8, "max_price": 45},
    {"name": "Baseball Cap", "category": "Accessories", "min_price": 8, "max_price": 35},
    {"name": "Resistance Bands", "category": "Fitness", "min_price": 8, "max_price": 40},
    {"name": "Graphic Novel", "category": "Books", "min_price": 12, "max_price": 50},
    {"name": "Hoodie", "category": "Clothing", "min_price": 20, "max_price": 85},
    {"name": "Phone Case", "category": "Electronics", "min_price": 5, "max_price": 40},
    {"name": "Throw Blanket", "category": "Home", "min_price": 15, "max_price": 100},
    {"name": "Tennis Racket", "category": "Sports", "min_price": 25, "max_price": 160},
    {"name": "Ballpoint Pen Set", "category": "Stationery", "min_price": 3, "max_price": 20},
]

def generate_product(product_id):
    template = product_catalog[product_id - 2001]

    minimum_cents = template["min_price"] * 100
    maximum_cents = template["max_price"] * 100

    valid_prices = []

    for cents in range(minimum_cents, maximum_cents + 1):
        if cents % 100 in (49, 99):
            valid_prices.append(cents)

    price = random.choice(valid_prices) / 100

    stock_quantity = random.randint(0, 500)

    launch_date = date.today() - timedelta(
        days=random.randint(1, 730)
    )

    return {
        "product_id": product_id,
        "product_name": template["name"],
        "category": template["category"],
        "price": price,
        "stock_quantity": stock_quantity,
        "launch_date": launch_date.isoformat()
    }

def main():
    products = []

    for product_id in range(2001, 2001 + NUMBER_OF_PRODUCTS):
        product = generate_product(product_id)
        products.append(product)

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
        fieldnames = [
            "product_id",
            "product_name",
            "category",
            "price",
            "stock_quantity",
            "launch_date"
        ]

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(products)

    print(f"Successfully generated {len(products)} products!")
    print(f"File saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()