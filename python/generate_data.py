import os
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from faker import Faker


# ============================================================
# CONFIGURATION
# ============================================================

SEED = 42

random.seed(SEED)
np.random.seed(SEED)
Faker.seed(SEED)

fake = Faker("en_IN")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")

os.makedirs(RAW_DIR, exist_ok=True)

# Test dataset size
# We will increase NUM_TRANSACTIONS to 100,000
# after validating the generator.
NUM_CUSTOMERS = 8000
NUM_PRODUCTS = 150
NUM_STORES = 25
NUM_TRANSACTIONS = 1000

START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2025, 12, 31)


# ============================================================
# BUSINESS MASTER DATA
# ============================================================

REGIONS = {
    "South": [
        ("Chennai", "Tamil Nadu"),
        ("Coimbatore", "Tamil Nadu"),
        ("Kochi", "Kerala"),
        ("Bengaluru", "Karnataka"),
        ("Hyderabad", "Telangana"),
    ],
    "West": [
        ("Mumbai", "Maharashtra"),
        ("Pune", "Maharashtra"),
        ("Ahmedabad", "Gujarat"),
        ("Surat", "Gujarat"),
        ("Nagpur", "Maharashtra"),
    ],
    "North": [
        ("Delhi", "Delhi"),
        ("Jaipur", "Rajasthan"),
        ("Lucknow", "Uttar Pradesh"),
        ("Chandigarh", "Chandigarh"),
        ("Noida", "Uttar Pradesh"),
    ],
    "East": [
        ("Kolkata", "West Bengal"),
        ("Bhubaneswar", "Odisha"),
        ("Patna", "Bihar"),
        ("Guwahati", "Assam"),
        ("Ranchi", "Jharkhand"),
    ],
}


CATEGORIES = {
    "Electronics": [
        "Televisions",
        "Mobile Phones",
        "Laptops",
        "Audio",
        "Accessories",
    ],
    "Home & Kitchen": [
        "Kitchen Appliances",
        "Furniture",
        "Cookware",
        "Home Decor",
    ],
    "Clothing": [
        "Men's Clothing",
        "Women's Clothing",
        "Kids' Clothing",
        "Footwear",
    ],
    "Grocery": [
        "Staples",
        "Snacks",
        "Beverages",
        "Packaged Food",
    ],
    "Personal Care": [
        "Skincare",
        "Haircare",
        "Bath & Body",
        "Grooming",
    ],
}


PRODUCT_NAMES = {
    "Televisions": [
        "Smart LED TV",
        "4K UHD TV",
        "QLED Smart TV",
        "Full HD TV",
    ],
    "Mobile Phones": [
        "Android Smartphone",
        "5G Smartphone",
        "Budget Smartphone",
        "Premium Smartphone",
    ],
    "Laptops": [
        "Business Laptop",
        "Gaming Laptop",
        "Ultrabook",
        "Student Laptop",
    ],
    "Audio": [
        "Bluetooth Speaker",
        "Wireless Headphones",
        "Earbuds",
        "Soundbar",
    ],
    "Accessories": [
        "USB-C Cable",
        "Wireless Charger",
        "Power Bank",
        "Phone Case",
    ],
    "Kitchen Appliances": [
        "Mixer Grinder",
        "Microwave Oven",
        "Air Fryer",
        "Electric Kettle",
    ],
    "Furniture": [
        "Office Chair",
        "Study Table",
        "Bookshelf",
        "Coffee Table",
    ],
    "Cookware": [
        "Non-stick Pan",
        "Pressure Cooker",
        "Cookware Set",
        "Frying Pan",
    ],
    "Home Decor": [
        "Table Lamp",
        "Wall Clock",
        "Cushion Set",
        "Decorative Vase",
    ],
    "Men's Clothing": [
        "Men's T-Shirt",
        "Men's Shirt",
        "Men's Jeans",
        "Men's Jacket",
    ],
    "Women's Clothing": [
        "Women's T-Shirt",
        "Women's Dress",
        "Women's Jeans",
        "Women's Jacket",
    ],
    "Kids' Clothing": [
        "Kids T-Shirt",
        "Kids Dress",
        "Kids Jeans",
        "Kids Jacket",
    ],
    "Footwear": [
        "Running Shoes",
        "Casual Shoes",
        "Sandals",
        "Sports Shoes",
    ],
    "Staples": [
        "Rice",
        "Wheat Flour",
        "Cooking Oil",
        "Sugar",
    ],
    "Snacks": [
        "Biscuits",
        "Chips",
        "Namkeen",
        "Chocolate",
    ],
    "Beverages": [
        "Tea",
        "Coffee",
        "Juice",
        "Soft Drink",
    ],
    "Packaged Food": [
        "Breakfast Cereal",
        "Instant Noodles",
        "Pasta",
        "Ready Meal",
    ],
    "Skincare": [
        "Face Wash",
        "Moisturizer",
        "Sunscreen",
        "Face Cream",
    ],
    "Haircare": [
        "Shampoo",
        "Conditioner",
        "Hair Oil",
        "Hair Serum",
    ],
    "Bath & Body": [
        "Body Wash",
        "Soap",
        "Body Lotion",
        "Deodorant",
    ],
    "Grooming": [
        "Shaving Kit",
        "Trimmer",
        "Beard Oil",
        "Razor",
    ],
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def random_date(start_date, end_date):
    """
    Generate a random date between two dates.
    """

    delta = end_date - start_date

    random_days = random.randint(0, delta.days)

    return start_date + timedelta(days=random_days)


def choose_region():
    """
    Choose a region using realistic weighted probabilities.
    """

    return random.choices(
        ["South", "West", "North", "East"],
        weights=[0.30, 0.28, 0.24, 0.18],
        k=1
    )[0]


# ============================================================
# GENERATE CUSTOMERS
# ============================================================

def generate_customers():

    customers = []

    for i in range(1, NUM_CUSTOMERS + 1):

        region = choose_region()

        city, state = random.choice(
            REGIONS[region]
        )

        signup_date = random_date(
            datetime(2022, 1, 1),
            END_DATE
        )

        customers.append({
            "CustomerID": f"C{i:05d}",
            "CustomerName": fake.name(),
            "Gender": random.choice(
                ["Male", "Female"]
            ),
            "Age": random.randint(18, 70),
            "City": city,
            "State": state,
            "Region": region,
            "SignupDate": signup_date.date(),
        })

    return pd.DataFrame(customers)


# ============================================================
# GENERATE PRODUCTS
# ============================================================

def generate_products():

    products = []

    product_id = 1

    # Create a complete list of category/subcategory pairs
    subcategory_list = []

    for category, subcategories in CATEGORIES.items():

        for subcategory in subcategories:

            subcategory_list.append(
                (category, subcategory)
            )

    total_subcategories = len(subcategory_list)

    # Determine how many products each subcategory receives
    base_products = (
        NUM_PRODUCTS // total_subcategories
    )

    remainder = (
        NUM_PRODUCTS % total_subcategories
    )

    for index, (category, subcategory) in enumerate(
        subcategory_list
    ):

        products_for_subcategory = base_products

        # Distribute remaining products evenly
        if index < remainder:
            products_for_subcategory += 1

        for product_number in range(
            products_for_subcategory
        ):

            base_name = random.choice(
                PRODUCT_NAMES[subcategory]
            )

            # Add a model/version identifier
            model_letter = chr(
                65 + (product_number % 5)
            )

            product_name = (
                f"{base_name} "
                f"{model_letter}{product_number + 1}"
            )

            # ------------------------------------------------
            # Price ranges by category
            # ------------------------------------------------

            if category == "Electronics":

                price = random.uniform(
                    1000,
                    80000
                )

            elif category == "Home & Kitchen":

                price = random.uniform(
                    500,
                    30000
                )

            elif category == "Clothing":

                price = random.uniform(
                    400,
                    8000
                )

            elif category == "Grocery":

                price = random.uniform(
                    50,
                    1500
                )

            else:

                price = random.uniform(
                    100,
                    5000
                )

            price = round(
                price,
                2
            )

            # Cost is 55%–85% of selling price
            cost_ratio = random.uniform(
                0.55,
                0.85
            )

            cost = round(
                price * cost_ratio,
                2
            )

            products.append({
                "ProductID": f"P{product_id:04d}",
                "ProductName": product_name,
                "Category": category,
                "SubCategory": subcategory,
                "UnitCost": cost,
                "UnitPrice": price,
            })

            product_id += 1

    return pd.DataFrame(products)


# ============================================================
# GENERATE STORES
# ============================================================

def generate_stores():

    stores = []

    for i in range(
        1,
        NUM_STORES + 1
    ):

        region = choose_region()

        city, state = random.choice(
            REGIONS[region]
        )

        store_type = random.choices(
            [
                "Mall",
                "High Street",
                "Neighborhood"
            ],
            weights=[
                0.30,
                0.35,
                0.35
            ],
            k=1
        )[0]

        stores.append({
            "StoreID": f"S{i:03d}",
            "StoreName": (
                f"RetailCo {city} {i}"
            ),
            "City": city,
            "State": state,
            "Region": region,
            "StoreType": store_type,
        })

    return pd.DataFrame(stores)


# ============================================================
# GENERATE TRANSACTIONS
# ============================================================

def generate_transactions(
    customers,
    products,
    stores
):

    transactions = []

    customer_ids = (
        customers["CustomerID"]
        .tolist()
    )

    product_ids = (
        products["ProductID"]
        .tolist()
    )

    store_ids = (
        stores["StoreID"]
        .tolist()
    )

    for i in range(
        1,
        NUM_TRANSACTIONS + 1
    ):

        order_date = random_date(
            START_DATE,
            END_DATE
        )

        customer_id = random.choice(
            customer_ids
        )

        product_id = random.choice(
            product_ids
        )

        store_id = random.choice(
            store_ids
        )

        # Retrieve product information
        product = products[
            products["ProductID"] == product_id
        ].iloc[0]

        # Quantity distribution
        quantity = random.choices(
            [1, 2, 3, 4, 5],
            weights=[
                0.55,
                0.25,
                0.12,
                0.06,
                0.02
            ],
            k=1
        )[0]

        # ----------------------------------------------------
        # Discount logic
        # ----------------------------------------------------

        if product["Category"] == "Clothing":

            discount = random.choice(
                [
                    0,
                    0.05,
                    0.10,
                    0.15,
                    0.20
                ]
            )

        else:

            discount = random.choice(
                [
                    0,
                    0,
                    0,
                    0.05,
                    0.10
                ]
            )

        # ----------------------------------------------------
        # Payment method
        # ----------------------------------------------------

        payment_method = random.choices(
            [
                "UPI",
                "Credit Card",
                "Debit Card",
                "Cash",
                "Net Banking"
            ],
            weights=[
                0.40,
                0.22,
                0.18,
                0.12,
                0.08
            ],
            k=1
        )[0]

        transactions.append({
            "OrderID": f"O{i:06d}",
            "OrderDate": order_date,
            "CustomerID": customer_id,
            "ProductID": product_id,
            "StoreID": store_id,
            "Quantity": quantity,
            "Discount": discount,
            "PaymentMethod": payment_method,
        })

    return pd.DataFrame(transactions)


# ============================================================
# INJECT DATA QUALITY PROBLEMS
# ============================================================

def inject_data_quality_issues(
    customers,
    products,
    stores,
    transactions
):

    # --------------------------------------------------------
    # ISSUE 1: Missing customer cities
    # --------------------------------------------------------

    missing_customer_rows = random.sample(
        list(customers.index),
        30
    )

    customers.loc[
        missing_customer_rows,
        "City"
    ] = np.nan

    # --------------------------------------------------------
    # ISSUE 2: Inconsistent category names
    # --------------------------------------------------------

    category_rows = random.sample(
        list(products.index),
        10
    )

    for idx in category_rows:

        category = products.loc[
            idx,
            "Category"
        ]

        if category == "Electronics":

            products.loc[
                idx,
                "Category"
            ] = "electronics"

        elif category == "Clothing":

            products.loc[
                idx,
                "Category"
            ] = "clothes"

        elif category == "Grocery":

            products.loc[
                idx,
                "Category"
            ] = "GROCERY"

    # --------------------------------------------------------
    # ISSUE 3: Product-name formatting problems
    # --------------------------------------------------------

    product_rows = random.sample(
        list(products.index),
        10
    )

    for idx in product_rows:

        products.loc[
            idx,
            "ProductName"
        ] = (
            "  "
            + products.loc[
                idx,
                "ProductName"
            ]
            + " "
        )

    # --------------------------------------------------------
    # ISSUE 4: Missing discounts
    # --------------------------------------------------------

    discount_rows = random.sample(
        list(transactions.index),
        15
    )

    transactions.loc[
        discount_rows,
        "Discount"
    ] = np.nan

    # --------------------------------------------------------
    # ISSUE 5: Negative quantities
    # --------------------------------------------------------

    quantity_rows = random.sample(
        list(transactions.index),
        5
    )

    transactions.loc[
        quantity_rows,
        "Quantity"
    ] = -transactions.loc[
        quantity_rows,
        "Quantity"
    ]

    # --------------------------------------------------------
    # ISSUE 6: Duplicate transactions
    # --------------------------------------------------------

    duplicate_rows = transactions.sample(
        5,
        random_state=SEED
    )

    transactions = pd.concat(
        [
            transactions,
            duplicate_rows
        ],
        ignore_index=True
    )

    return (
        customers,
        products,
        stores,
        transactions
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print("Generating customers...")

    customers = generate_customers()

    print("Generating products...")

    products = generate_products()

    print("Generating stores...")

    stores = generate_stores()

    print("Generating transactions...")

    transactions = generate_transactions(
        customers,
        products,
        stores
    )

    print(
        "Injecting data-quality issues..."
    )

    (
        customers,
        products,
        stores,
        transactions
    ) = inject_data_quality_issues(
        customers,
        products,
        stores,
        transactions
    )

    # ========================================================
    # SAVE RAW FILES
    # ========================================================

    customers.to_csv(
        os.path.join(
            RAW_DIR,
            "customers_raw.csv"
        ),
        index=False
    )

    products.to_csv(
        os.path.join(
            RAW_DIR,
            "products_raw.csv"
        ),
        index=False
    )

    stores.to_csv(
        os.path.join(
            RAW_DIR,
            "stores_raw.csv"
        ),
        index=False
    )

    transactions.to_csv(
        os.path.join(
            RAW_DIR,
            "transactions_raw.csv"
        ),
        index=False
    )

    # ========================================================
    # FINAL OUTPUT
    # ========================================================

    print()
    print("====================================")
    print("DATA GENERATION COMPLETE")
    print("====================================")

    print(
        f"Customers:    {len(customers):,}"
    )

    print(
        f"Products:     {len(products):,}"
    )

    print(
        f"Stores:       {len(stores):,}"
    )

    print(
        f"Transactions: {len(transactions):,}"
    )

    print()
    print("Files saved to:")
    print(RAW_DIR)


# ============================================================
# RUN SCRIPT
# ============================================================

if __name__ == "__main__":
    main()