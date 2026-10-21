
import csv
import random
from datetime import date, timedelta
from pathlib import Path

# Locate the project and data folders
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# Configuration
NUMBER_OF_CUSTOMERS = 500
OUTPUT_FILE = DATA_DIR / "customers.csv"

first_names = ["John", "Sarah", "Mohammed", "Emily", "David",
    "Aisha", "Daniel", "Fatima", "James", "Olivia",
    "Noah", "Zara", "Liam", "Amara", "Ethan",
    "Layla", "Adam", "Sophia", "Yusuf", "Mia",
    "Alexander", "Hannah", "Omar", "Isabella", "Ryan",
    "Nadia", "Benjamin", "Leila", "Samuel", "Chloe",
    "Ibrahim", "Grace", "Michael", "Amina", "Jacob",
    "Mariam", "Lucas", "Priya", "Gabriel", "Zainab"]
last_names = ["Smith", "Khan", "Patel", "Johnson", "Williams",
    "Brown", "Davis", "Wilson", "Anderson", "Taylor",
    "Miller", "Singh", "Naidoo", "Suleman", "Botha",
    "Mokoena", "Gani", "Mthembu", "Pillay", "Jacobs",
    "Ahmed", "Hassan", "Ali", "Clarke", "Martin",
    "Thompson", "White", "Harris", "Lewis", "Walker",
    "Roberts", "Young", "King", "Scott", "Green",
    "Adams", "Nelson", "Mitchell", "Campbell", "Robinson"]
countries = ["USA", "South Africa", "UK", "Canada", "Australia"]

def generate_customer(customer_id):
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    country = random.choice(countries)

    signup_date = date.today() - timedelta(
        days=random.randint(1, 730)
    )

    return {
        "customer_id": customer_id,
        "first_name": first_name,
        "last_name": last_name,
        "email": f"{first_name.lower()}.{last_name.lower()}{customer_id}@example.com",
        "country": country,
        "signup_date": signup_date.isoformat()
    }

def main():
    customers = []

    for customer_id in range(1001, 1001 + NUMBER_OF_CUSTOMERS):
        customer = generate_customer(customer_id)
        customers.append(customer)

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "customer_id",
                "first_name",
                "last_name",
                "email",
                "country",
                "signup_date"
            ]
        )

        writer.writeheader()
        writer.writerows(customers)

    print(f"Successfully generated {len(customers)} customers!")
    print(f"File saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()

