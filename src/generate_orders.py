import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

# Locate the project and data folders
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# Configuration
NUMBER_OF_ORDERS = 1000

CUSTOMERS_FILE = DATA_DIR / "customers.csv"
OUTPUT_FILE = DATA_DIR / "orders.csv"

def load_customer_ids():
    with open(CUSTOMERS_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        customer_ids = [
            int(row["customer_id"])
            for row in reader
        ]

    return customer_ids

def generate_order(order_id, customer_ids):
    customer_id = random.choice(customer_ids)

    order_date = datetime.now() - timedelta(
        days=random.randint(1, 365)
    )

    order_status = random.choice([
        "Delivered",
        "Delivered",
        "Delivered",
        "Shipped",
        "Processing",
        "Cancelled"
    ])

    return {
        "order_id": order_id,
        "customer_id": customer_id,
        "order_date": order_date.strftime("%Y-%m-%d %H:%M:%S"),
        "order_status": order_status
    }

def main():
    customer_ids = load_customer_ids()
    orders = []

    for order_id in range(5001, 5001 + NUMBER_OF_ORDERS):
        order = generate_order(order_id, customer_ids)
        orders.append(order)

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
        fieldnames = [
            "order_id",
            "customer_id",
            "order_date",
            "order_status"
        ]

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(orders)

    print(f"Successfully generated {len(orders)} orders!")
    print(f"File saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()