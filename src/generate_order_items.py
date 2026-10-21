import csv
import random
from pathlib import Path

# Locate the project and data folders
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# Configuration
NUMBER_OF_ORDER_ITEMS = 2500

PRODUCTS_FILE = DATA_DIR / "products.csv"
ORDERS_FILE = DATA_DIR / "orders.csv"
OUTPUT_FILE = DATA_DIR / "order_items.csv"

def load_product_ids():
    with open(PRODUCTS_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        product_ids = [
            int(row["product_id"])
            for row in reader
        ]
        
        return product_ids

def load_order_ids():
    with open(ORDERS_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        order_ids = [
            int(row["order_id"])
            for row in reader
        ]
        
        return order_ids

def load_product_prices():
    with open(PRODUCTS_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        product_prices = [
            (int(row["product_id"]), float(row["price"]))
            for row in reader
        ]

    return dict(product_prices)

def generate_order_item(order_item_id, order_ids, product_ids, product_prices):
    order_id = random.choice(order_ids)
    product_id = random.choice(product_ids)
    quantity = random.randint(1, 5)
    unit_price = product_prices[product_id]
    line_total = round(unit_price * quantity, 2)

    return {
        "order_item_id": order_item_id,
        "order_id": order_id,
        "product_id": product_id,
        "quantity": quantity,
        "unit_price": unit_price,
        "line_total": line_total
    }

def main():
    product_ids = load_product_ids()
    order_ids = load_order_ids()
    product_prices = load_product_prices()
    
    order_items = []

    for order_item_id in range(1, NUMBER_OF_ORDER_ITEMS + 1):
            order_item = generate_order_item(
                order_item_id, 
                order_ids, 
                product_ids, 
                product_prices
            )
            order_items.append(order_item)

            with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
                fieldnames = [
                    "order_item_id",
                    "order_id",
                    "product_id",
                    "quantity",
                    "unit_price",
                    "line_total"
                ]

                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(order_items)

            print(f"Successfully generated {len(order_items)} order items!")
            print(f"File saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()