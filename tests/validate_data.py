import csv
from pathlib import Path 

# Locate the project and data folders
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"

# Configuration
CUSTOMERS_FILE = DATA_DIR / "customers.csv"
PRODUCTS_FILE = DATA_DIR / "products.csv"
ORDERS_FILE = DATA_DIR / "orders.csv"
ORDER_ITEMS_FILE = DATA_DIR / "order_items.csv"


def load_csv(file_path):
    with open(file_path, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)


def check_unique_ids(records, id_column, dataset_name):
    ids = [row[id_column] for row in records]

    if len(ids) == len(set(ids)):
        print(f"PASS: {dataset_name} has unique {id_column} values.")
    else:
        print(f"FAIL: {dataset_name} contains duplicate {id_column} values.")


def check_foreign_keys(child_records, child_column, parent_records, parent_column, relationship_name):
    valid_parent_ids = {
        row[parent_column]
        for row in parent_records
    }

    invalid_records = [
        row[child_column]
        for row in child_records
        if row[child_column] not in valid_parent_ids
    ]

    if not invalid_records:
        print(f"PASS: {relationship_name} - all references are valid.")
    else:
        print(
            f"FAIL: {relationship_name} - "
            f"{len(invalid_records)} invalid reference(s) found."
        )
        print(f"Invalid IDs: {invalid_records[:10]}")


def check_line_totals(order_items):
    invalid_items = []

    for item in order_items:
        unit_price = float(item["unit_price"])
        quantity = int(item["quantity"])
        recorded_total = round(float(item["line_total"]), 2)
        expected_total = round(unit_price * quantity, 2)

        if recorded_total != expected_total:
            invalid_items.append(item["order_item_id"])

    if not invalid_items:
        print("PASS: All order-item line totals are correct.")
        return True
    else:
        print(
            f"FAIL: {len(invalid_items)} order-item(s) have incorrect line totals."
        )
        print(f"Invalid order_item_ids: {invalid_items[:10]}")
        return False


def test_invalid_line_total():
    test_items = [
        {
            "order_item_id": "9999",
            "unit_price": "10.00",
            "quantity": "2",
            "line_total": "25.00"
        }
    ]

    result = check_line_totals(test_items)

    assert result is False, "Validator failed to catch an invalid total."

    print("TEST PASSED: Invalid line total was detected.")


def check_business_rules(products, orders, order_items):
    errors = []

    # Check product prices
    for product in products:
        if float(product["price"]) < 0:
            errors.append(
                f"Product {product['product_id']} has a negative price."
            )

    # Check order statuses
    valid_statuses = {
        "Delivered",
        "Shipped",
        "Processing",
        "Cancelled"
    }

    for order in orders:
        if order["order_status"] not in valid_statuses:
            errors.append(
                f"Order {order['order_id']} has an invalid status."
            )

    # Check order-item quantities and prices
    for item in order_items:
        if int(item["quantity"]) <= 0:
            errors.append(
                f"Order item {item['order_item_id']} has an invalid quantity."
            )

        if float(item["unit_price"]) < 0:
            errors.append(
                f"Order item {item['order_item_id']} has a negative unit price."
            )

    if not errors:
        print("PASS: All business rules are satisfied.")
    else:
        print(f"FAIL: Found {len(errors)} business rule violation(s).")
        for error in errors[:10]:
            print(f" - {error}")


def check_missing_values(datasets):
    required_fields = {
        "Customers": (datasets["Customers"], [
            "customer_id", "first_name", "last_name",
            "email", "country", "signup_date"
        ]),
        "Products": (datasets["Products"], [
            "product_id", "product_name", "category",
            "price", "stock_quantity", "launch_date"
        ]),
        "Orders": (datasets["Orders"], [
            "order_id", "customer_id", "order_date", "order_status"
        ]),
        "Order items": (datasets["Order items"], [
            "order_item_id", "order_id", "product_id",
            "quantity", "unit_price", "line_total"
        ])
    }

    missing = []

    for dataset_name, (records, fields) in required_fields.items():
        for row_number, record in enumerate(records, start=2):
            for field in fields:
                if not record.get(field, "").strip():
                    missing.append(
                        f"{dataset_name}, row {row_number}: {field} is missing."
                    )

    if not missing:
        print("PASS: No required values are missing.")
    else:
        print(f"FAIL: Found {len(missing)} missing value(s).")
        for error in missing[:10]:
            print(f" - {error}")


def main():
    customers = load_csv(CUSTOMERS_FILE)
    products = load_csv(PRODUCTS_FILE)
    orders = load_csv(ORDERS_FILE)
    order_items = load_csv(ORDER_ITEMS_FILE)

    print(f"Loaded {len(customers)} customers.")
    print(f"Loaded {len(products)} products.")
    print(f"Loaded {len(orders)} orders.")
    print(f"Loaded {len(order_items)} order items.")

    check_unique_ids(customers, "customer_id", "Customers")
    check_unique_ids(products, "product_id", "Products")
    check_unique_ids(orders, "order_id", "Orders")
    check_unique_ids(order_items, "order_item_id", "Order Items")

    check_foreign_keys(orders, "customer_id", customers, "customer_id", "Orders -> Customers")
    check_foreign_keys(order_items, "order_id", orders, "order_id", "Order Items -> Orders")
    check_foreign_keys(order_items, "product_id", products, "product_id", "Order Items -> Products")
    
    check_line_totals(order_items)

    check_business_rules(products, orders, order_items)

    check_missing_values({
        "Customers": customers,
        "Products": products,
        "Orders": orders,
        "Order items": order_items
    })

if __name__ == "__main__":
    main()
    test_invalid_line_total()