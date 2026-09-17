import os
import pandas as pd
import numpy as np


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

RAW_DIR = os.path.join(
    BASE_DIR,
    "data",
    "raw"
)


# ============================================================
# LOAD DATA
# ============================================================

def load_data():

    customers = pd.read_csv(
        os.path.join(
            RAW_DIR,
            "customers_raw.csv"
        )
    )

    products = pd.read_csv(
        os.path.join(
            RAW_DIR,
            "products_raw.csv"
        )
    )

    stores = pd.read_csv(
        os.path.join(
            RAW_DIR,
            "stores_raw.csv"
        )
    )

    transactions = pd.read_csv(
        os.path.join(
            RAW_DIR,
            "transactions_raw.csv"
        )
    )

    return (
        customers,
        products,
        stores,
        transactions
    )


# ============================================================
# DATASET SIZE CHECK
# ============================================================

def check_dataset_sizes(
    customers,
    products,
    stores,
    transactions
):

    print("\n")
    print("=" * 65)
    print("1. DATASET SIZE CHECK")
    print("=" * 65)

    print(
        f"Customers      : {len(customers):,}"
    )

    print(
        f"Products       : {len(products):,}"
    )

    print(
        f"Stores         : {len(stores):,}"
    )

    print(
        f"Transactions   : {len(transactions):,}"
    )


# ============================================================
# MISSING VALUE CHECK
# ============================================================

def check_missing_values(
    customers,
    products,
    stores,
    transactions
):

    print("\n")
    print("=" * 65)
    print("2. MISSING VALUE CHECK")
    print("=" * 65)

    datasets = {
        "Customers": customers,
        "Products": products,
        "Stores": stores,
        "Transactions": transactions
    }

    for name, df in datasets.items():

        print(f"\n{name}")

        missing = df.isnull().sum()

        missing = missing[
            missing > 0
        ]

        if missing.empty:

            print(
                "No missing values found."
            )

        else:

            for column, count in missing.items():

                percentage = (
                    count / len(df)
                ) * 100

                print(
                    f"  {column}: "
                    f"{count:,} "
                    f"({percentage:.2f}%)"
                )


# ============================================================
# DUPLICATE CHECK
# ============================================================

def check_duplicates(
    customers,
    products,
    stores,
    transactions
):

    print("\n")
    print("=" * 65)
    print("3. DUPLICATE CHECK")
    print("=" * 65)

    datasets = {
        "Customers": customers,
        "Products": products,
        "Stores": stores
    }

    for name, df in datasets.items():

        duplicates = df.duplicated().sum()

        print(
            f"{name} duplicate rows: "
            f"{duplicates:,}"
        )

    # --------------------------------------------------------
    # Duplicate OrderIDs
    # --------------------------------------------------------

    order_duplicates = (
        transactions["OrderID"]
        .duplicated()
        .sum()
    )

    print(
        f"Transaction duplicate OrderIDs: "
        f"{order_duplicates:,}"
    )

    duplicate_orders = (
        transactions[
            transactions["OrderID"].duplicated(
                keep=False
            )
        ]
        .sort_values("OrderID")
    )

    if not duplicate_orders.empty:

        print(
            "\nDuplicate OrderID examples:"
        )

        columns = [
            "OrderID",
            "OrderDate",
            "CustomerID",
            "ProductID",
            "StoreID",
            "Quantity"
        ]

        print(
            duplicate_orders[
                columns
            ]
            .head(10)
            .to_string(index=False)
        )


# ============================================================
# DATA TYPE CHECK
# ============================================================

def check_data_types(
    customers,
    products,
    stores,
    transactions
):

    print("\n")
    print("=" * 65)
    print("4. DATA TYPE CHECK")
    print("=" * 65)

    datasets = {
        "Customers": customers,
        "Products": products,
        "Stores": stores,
        "Transactions": transactions
    }

    for name, df in datasets.items():

        print(f"\n{name}")

        print(
            df.dtypes.to_string()
        )

    # --------------------------------------------------------
    # Explicit numeric validation
    # --------------------------------------------------------

    print("\nNumeric field validation:")

    numeric_columns = {
        "Customers": [
            ("Age", customers["Age"])
        ],

        "Products": [
            ("UnitCost", products["UnitCost"]),
            ("UnitPrice", products["UnitPrice"])
        ],

        "Transactions": [
            ("Quantity", transactions["Quantity"]),
            ("Discount", transactions["Discount"])
        ]
    }

    for dataset_name, columns in numeric_columns.items():

        for column_name, series in columns:

            converted = pd.to_numeric(
                series,
                errors="coerce"
            )

            invalid_count = (
                series.notna()
                & converted.isna()
            ).sum()

            print(
                f"  {dataset_name} - "
                f"{column_name}: "
                f"{invalid_count:,} "
                f"non-numeric values"
            )


# ============================================================
# DATE CHECK
# ============================================================

def check_dates(transactions):

    print("\n")
    print("=" * 65)
    print("5. DATE CHECK")
    print("=" * 65)

    transaction_dates = pd.to_datetime(
        transactions["OrderDate"],
        errors="coerce"
    )

    invalid_dates = (
        transaction_dates.isna().sum()
    )

    print(
        f"Invalid transaction dates: "
        f"{invalid_dates:,}"
    )

    if invalid_dates > 0:

        print(
            "\nInvalid date examples:"
        )

        invalid_rows = transactions[
            transaction_dates.isna()
        ]

        print(
            invalid_rows[
                [
                    "OrderID",
                    "OrderDate"
                ]
            ]
            .head(10)
            .to_string(index=False)
        )

    valid_dates = (
        transaction_dates.dropna()
    )

    if not valid_dates.empty:

        print(
            f"\nEarliest valid transaction date: "
            f"{valid_dates.min().date()}"
        )

        print(
            f"Latest valid transaction date: "
            f"{valid_dates.max().date()}"
        )

    # --------------------------------------------------------
    # Future dates
    # --------------------------------------------------------

    future_dates = (
        transaction_dates
        > pd.Timestamp.today()
    ).sum()

    print(
        f"Future transaction dates: "
        f"{future_dates:,}"
    )


# ============================================================
# QUANTITY CHECK
# ============================================================

def check_quantities(transactions):

    print("\n")
    print("=" * 65)
    print("6. QUANTITY CHECK")
    print("=" * 65)

    # Convert safely
    quantity_numeric = pd.to_numeric(
        transactions["Quantity"],
        errors="coerce"
    )

    # --------------------------------------------------------
    # Non-numeric values
    # --------------------------------------------------------

    non_numeric = (
        transactions["Quantity"].notna()
        & quantity_numeric.isna()
    ).sum()

    print(
        f"Non-numeric quantities: "
        f"{non_numeric:,}"
    )

    if non_numeric > 0:

        print(
            "\nNon-numeric quantity examples:"
        )

        invalid_quantity_rows = transactions[
            transactions["Quantity"].notna()
            & quantity_numeric.isna()
        ]

        print(
            invalid_quantity_rows[
                [
                    "OrderID",
                    "Quantity",
                    "ProductID",
                    "CustomerID"
                ]
            ]
            .head(10)
            .to_string(index=False)
        )

    # --------------------------------------------------------
    # Negative values
    # --------------------------------------------------------

    negative_quantity = (
        quantity_numeric < 0
    ).sum()

    zero_quantity = (
        quantity_numeric == 0
    ).sum()

    print(
        f"\nNegative quantities: "
        f"{negative_quantity:,}"
    )

    print(
        f"Zero quantities: "
        f"{zero_quantity:,}"
    )

    if negative_quantity > 0:

        print(
            "\nNegative quantity examples:"
        )

        negative_rows = transactions[
            quantity_numeric < 0
        ]

        print(
            negative_rows[
                [
                    "OrderID",
                    "Quantity",
                    "ProductID",
                    "CustomerID"
                ]
            ]
            .head(10)
            .to_string(index=False)
        )


# ============================================================
# DISCOUNT CHECK
# ============================================================

def check_discounts(transactions):

    print("\n")
    print("=" * 65)
    print("7. DISCOUNT CHECK")
    print("=" * 65)

    discount_numeric = pd.to_numeric(
        transactions["Discount"],
        errors="coerce"
    )

    missing_discount = (
        transactions["Discount"]
        .isna()
        .sum()
    )

    non_numeric_discount = (
        transactions["Discount"].notna()
        & discount_numeric.isna()
    ).sum()

    negative_discount = (
        discount_numeric < 0
    ).sum()

    excessive_discount = (
        discount_numeric > 1
    ).sum()

    print(
        f"Missing discounts: "
        f"{missing_discount:,}"
    )

    print(
        f"Non-numeric discounts: "
        f"{non_numeric_discount:,}"
    )

    print(
        f"Negative discounts: "
        f"{negative_discount:,}"
    )

    print(
        f"Discounts greater than 100%: "
        f"{excessive_discount:,}"
    )


# ============================================================
# PRODUCT PRICE CHECK
# ============================================================

def check_product_prices(products):

    print("\n")
    print("=" * 65)
    print("8. PRODUCT PRICE CHECK")
    print("=" * 65)

    unit_cost = pd.to_numeric(
        products["UnitCost"],
        errors="coerce"
    )

    unit_price = pd.to_numeric(
        products["UnitPrice"],
        errors="coerce"
    )

    negative_cost = (
        unit_cost < 0
    ).sum()

    negative_price = (
        unit_price < 0
    ).sum()

    zero_cost = (
        unit_cost == 0
    ).sum()

    zero_price = (
        unit_price == 0
    ).sum()

    cost_greater_than_price = (
        unit_cost > unit_price
    ).sum()

    print(
        f"Negative UnitCost: "
        f"{negative_cost:,}"
    )

    print(
        f"Negative UnitPrice: "
        f"{negative_price:,}"
    )

    print(
        f"Zero UnitCost: "
        f"{zero_cost:,}"
    )

    print(
        f"Zero UnitPrice: "
        f"{zero_price:,}"
    )

    print(
        f"Cost greater than selling price: "
        f"{cost_greater_than_price:,}"
    )


# ============================================================
# OUTLIER CHECK
# ============================================================

def check_price_outliers(products):

    print("\n")
    print("=" * 65)
    print("9. PRODUCT PRICE OUTLIER CHECK")
    print("=" * 65)

    prices = pd.to_numeric(
        products["UnitPrice"],
        errors="coerce"
    )

    prices = prices.dropna()

    if prices.empty:

        print(
            "No valid prices available."
        )

        return

    # --------------------------------------------------------
    # IQR method
    # --------------------------------------------------------

    q1 = prices.quantile(0.25)
    q3 = prices.quantile(0.75)

    iqr = q3 - q1

    lower_bound = (
        q1 - 1.5 * iqr
    )

    upper_bound = (
        q3 + 1.5 * iqr
    )

    outlier_mask = (
        (prices < lower_bound)
        | (prices > upper_bound)
    )

    outlier_count = (
        outlier_mask.sum()
    )

    print(
        f"Q1: ₹{q1:,.2f}"
    )

    print(
        f"Q3: ₹{q3:,.2f}"
    )

    print(
        f"IQR: ₹{iqr:,.2f}"
    )

    print(
        f"Upper outlier threshold: "
        f"₹{upper_bound:,.2f}"
    )

    print(
        f"Potential price outliers: "
        f"{outlier_count:,}"
    )

    if outlier_count > 0:

        print(
            "\nPotential outlier examples:"
        )

        outlier_products = products.loc[
            outlier_mask
        ].copy()

        print(
            outlier_products[
                [
                    "ProductID",
                    "ProductName",
                    "Category",
                    "UnitCost",
                    "UnitPrice"
                ]
            ]
            .sort_values(
                "UnitPrice",
                ascending=False
            )
            .head(10)
            .to_string(index=False)
        )


# ============================================================
# CATEGORY CONSISTENCY CHECK
# ============================================================

def check_categories(products):

    print("\n")
    print("=" * 65)
    print("10. CATEGORY CONSISTENCY CHECK")
    print("=" * 65)

    print(
        "\nCategory values found:"
    )

    categories = (
        products["Category"]
        .value_counts(
            dropna=False
        )
    )

    print(
        categories.to_string()
    )

    # --------------------------------------------------------
    # Normalized category values
    # --------------------------------------------------------

    normalized_categories = (
        products["Category"]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    print(
        "\nNormalized category groups:"
    )

    print(
        normalized_categories
        .value_counts(
            dropna=False
        )
        .to_string()
    )

    # --------------------------------------------------------
    # Subcategories
    # --------------------------------------------------------

    print(
        "\nSubcategory values found:"
    )

    subcategories = (
        products["SubCategory"]
        .value_counts(
            dropna=False
        )
    )

    print(
        subcategories.to_string()
    )


# ============================================================
# PRODUCT NAME FORMATTING CHECK
# ============================================================

def check_product_names(products):

    print("\n")
    print("=" * 65)
    print("11. PRODUCT NAME FORMATTING CHECK")
    print("=" * 65)

    product_names = (
        products["ProductName"]
        .astype("string")
    )

    leading_spaces = (
        product_names.str.startswith(" ")
        .sum()
    )

    trailing_spaces = (
        product_names.str.endswith(" ")
        .sum()
    )

    print(
        f"Names with leading spaces: "
        f"{leading_spaces:,}"
    )

    print(
        f"Names with trailing spaces: "
        f"{trailing_spaces:,}"
    )

    if leading_spaces > 0 or trailing_spaces > 0:

        print(
            "\nFormatting issue examples:"
        )

        formatting_mask = (
            product_names.str.startswith(" ")
            |
            product_names.str.endswith(" ")
        )

        print(
            products.loc[
                formatting_mask,
                [
                    "ProductID",
                    "ProductName"
                ]
            ]
            .head(10)
            .to_string(index=False)
        )


# ============================================================
# REFERENTIAL INTEGRITY CHECK
# ============================================================

def check_referential_integrity(
    customers,
    products,
    stores,
    transactions
):

    print("\n")
    print("=" * 65)
    print("12. REFERENTIAL INTEGRITY CHECK")
    print("=" * 65)

    customer_ids = set(
        customers["CustomerID"]
    )

    product_ids = set(
        products["ProductID"]
    )

    store_ids = set(
        stores["StoreID"]
    )

    transaction_customer_ids = set(
        transactions[
            "CustomerID"
        ]
        .dropna()
    )

    transaction_product_ids = set(
        transactions[
            "ProductID"
        ]
        .dropna()
    )

    transaction_store_ids = set(
        transactions[
            "StoreID"
        ]
        .dropna()
    )

    missing_customers = (
        transaction_customer_ids
        - customer_ids
    )

    missing_products = (
        transaction_product_ids
        - product_ids
    )

    missing_stores = (
        transaction_store_ids
        - store_ids
    )

    print(
        f"Transactions referencing "
        f"unknown customers: "
        f"{len(missing_customers):,}"
    )

    print(
        f"Transactions referencing "
        f"unknown products: "
        f"{len(missing_products):,}"
    )

    print(
        f"Transactions referencing "
        f"unknown stores: "
        f"{len(missing_stores):,}"
    )

    # --------------------------------------------------------
    # Show examples
    # --------------------------------------------------------

    if missing_customers:

        print(
            "\nUnknown CustomerIDs:"
        )

        print(
            list(
                missing_customers
            )[:10]
        )

    if missing_products:

        print(
            "\nUnknown ProductIDs:"
        )

        print(
            list(
                missing_products
            )[:10]
        )

    if missing_stores:

        print(
            "\nUnknown StoreIDs:"
        )

        print(
            list(
                missing_stores
            )[:10]
        )


# ============================================================
# CUSTOMER DATA CHECK
# ============================================================

def check_customer_data(customers):

    print("\n")
    print("=" * 65)
    print("13. CUSTOMER DATA CHECK")
    print("=" * 65)

    age_numeric = pd.to_numeric(
        customers["Age"],
        errors="coerce"
    )

    invalid_age_low = (
        age_numeric < 0
    ).sum()

    invalid_age_high = (
        age_numeric > 100
    ).sum()

    invalid_age_type = (
        customers["Age"].notna()
        & age_numeric.isna()
    ).sum()

    print(
        f"Age below 0: "
        f"{invalid_age_low:,}"
    )

    print(
        f"Age above 100: "
        f"{invalid_age_high:,}"
    )

    print(
        f"Non-numeric ages: "
        f"{invalid_age_type:,}"
    )

    print(
        "\nGender values:"
    )

    print(
        customers["Gender"]
        .value_counts(
            dropna=False
        )
        .to_string()
    )

    print(
        "\nRegion values:"
    )

    print(
        customers["Region"]
        .value_counts(
            dropna=False
        )
        .to_string()
    )


# ============================================================
# STORE DATA CHECK
# ============================================================

def check_store_data(stores):

    print("\n")
    print("=" * 65)
    print("14. STORE DATA CHECK")
    print("=" * 65)

    print(
        "\nStore types:"
    )

    print(
        stores["StoreType"]
        .value_counts(
            dropna=False
        )
        .to_string()
    )

    print(
        "\nStore regions:"
    )

    print(
        stores["Region"]
        .value_counts(
            dropna=False
        )
        .to_string()
    )


# ============================================================
# TRANSACTION SUMMARY
# ============================================================

def transaction_summary(
    transactions,
    products
):

    print("\n")
    print("=" * 65)
    print("15. TRANSACTION SUMMARY")
    print("=" * 65)

    # --------------------------------------------------------
    # Safely convert quantity
    # --------------------------------------------------------

    quantity = pd.to_numeric(
        transactions["Quantity"],
        errors="coerce"
    )

    discount = pd.to_numeric(
        transactions["Discount"],
        errors="coerce"
    )

    print(
        f"Total quantity recorded "
        f"(valid numeric rows): "
        f"{quantity.sum():,.0f}"
    )

    print(
        f"Average quantity per valid row: "
        f"{quantity.mean():.2f}"
    )

    # --------------------------------------------------------
    # Merge product information
    # --------------------------------------------------------

    merged = transactions.merge(

        products[
            [
                "ProductID",
                "Category",
                "UnitCost",
                "UnitPrice"
            ]
        ],

        on="ProductID",

        how="left"
    )

    merged["QuantityNumeric"] = (
        pd.to_numeric(
            merged["Quantity"],
            errors="coerce"
        )
    )

    merged["DiscountNumeric"] = (
        pd.to_numeric(
            merged["Discount"],
            errors="coerce"
        )
    )

    # Missing discount is temporarily treated
    # as zero ONLY for this diagnostic estimate.
    merged["DiscountForEstimate"] = (
        merged["DiscountNumeric"]
        .fillna(0)
    )

    # --------------------------------------------------------
    # Revenue
    # --------------------------------------------------------

    merged["Revenue"] = (

        merged["QuantityNumeric"]

        * merged["UnitPrice"]

        * (
            1
            - merged["DiscountForEstimate"]
        )
    )

    # --------------------------------------------------------
    # Cost
    # --------------------------------------------------------

    merged["Cost"] = (

        merged["QuantityNumeric"]

        * merged["UnitCost"]
    )

    # --------------------------------------------------------
    # Profit
    # --------------------------------------------------------

    merged["Profit"] = (
        merged["Revenue"]
        - merged["Cost"]
    )

    print(
        f"Estimated revenue: "
        f"₹{merged['Revenue'].sum():,.2f}"
    )

    print(
        f"Estimated cost: "
        f"₹{merged['Cost'].sum():,.2f}"
    )

    print(
        f"Estimated profit: "
        f"₹{merged['Profit'].sum():,.2f}"
    )


# ============================================================
# FINAL DATA QUALITY SUMMARY
# ============================================================

def print_final_summary(
    customers,
    products,
    stores,
    transactions
):

    print("\n")
    print("=" * 65)
    print("16. DATA QUALITY SUMMARY")
    print("=" * 65)

    # --------------------------------------------------------
    # Missing values
    # --------------------------------------------------------

    customer_missing = (
        customers.isna()
        .sum()
        .sum()
    )

    product_missing = (
        products.isna()
        .sum()
        .sum()
    )

    store_missing = (
        stores.isna()
        .sum()
        .sum()
    )

    transaction_missing = (
        transactions.isna()
        .sum()
        .sum()
    )

    # --------------------------------------------------------
    # Duplicate OrderIDs
    # --------------------------------------------------------

    duplicate_orders = (
        transactions["OrderID"]
        .duplicated()
        .sum()
    )

    # --------------------------------------------------------
    # Invalid dates
    # --------------------------------------------------------

    invalid_dates = (
        pd.to_datetime(
            transactions["OrderDate"],
            errors="coerce"
        )
        .isna()
        .sum()
    )

    # --------------------------------------------------------
    # Invalid quantities
    # --------------------------------------------------------

    quantity_numeric = pd.to_numeric(
        transactions["Quantity"],
        errors="coerce"
    )

    non_numeric_quantity = (
        transactions["Quantity"].notna()
        & quantity_numeric.isna()
    ).sum()

    negative_quantity = (
        quantity_numeric < 0
    ).sum()

    # --------------------------------------------------------
    # Referential integrity
    # --------------------------------------------------------

    missing_customer_ids = (
        set(
            transactions["CustomerID"]
            .dropna()
        )
        -
        set(
            customers["CustomerID"]
        )
    )

    missing_product_ids = (
        set(
            transactions["ProductID"]
            .dropna()
        )
        -
        set(
            products["ProductID"]
        )
    )

    missing_store_ids = (
        set(
            transactions["StoreID"]
            .dropna()
        )
        -
        set(
            stores["StoreID"]
        )
    )

    # --------------------------------------------------------
    # Print summary
    # --------------------------------------------------------

    print(
        f"Customer missing cells: "
        f"{customer_missing:,}"
    )

    print(
        f"Product missing cells: "
        f"{product_missing:,}"
    )

    print(
        f"Store missing cells: "
        f"{store_missing:,}"
    )

    print(
        f"Transaction missing cells: "
        f"{transaction_missing:,}"
    )

    print(
        f"Duplicate OrderIDs: "
        f"{duplicate_orders:,}"
    )

    print(
        f"Invalid dates: "
        f"{invalid_dates:,}"
    )

    print(
        f"Non-numeric quantities: "
        f"{non_numeric_quantity:,}"
    )

    print(
        f"Negative quantities: "
        f"{negative_quantity:,}"
    )

    print(
        f"Unknown CustomerIDs: "
        f"{len(missing_customer_ids):,}"
    )

    print(
        f"Unknown ProductIDs: "
        f"{len(missing_product_ids):,}"
    )

    print(
        f"Unknown StoreIDs: "
        f"{len(missing_store_ids):,}"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 65)
    print("RETAILCO RAW DATA QUALITY ASSESSMENT")
    print("=" * 65)

    print(
        "\nLoading raw datasets..."
    )

    (
        customers,
        products,
        stores,
        transactions
    ) = load_data()

    # --------------------------------------------------------
    # Run checks
    # --------------------------------------------------------

    check_dataset_sizes(
        customers,
        products,
        stores,
        transactions
    )

    check_missing_values(
        customers,
        products,
        stores,
        transactions
    )

    check_duplicates(
        customers,
        products,
        stores,
        transactions
    )

    check_data_types(
        customers,
        products,
        stores,
        transactions
    )

    check_dates(
        transactions
    )

    check_quantities(
        transactions
    )

    check_discounts(
        transactions
    )

    check_product_prices(
        products
    )

    check_price_outliers(
        products
    )

    check_categories(
        products
    )

    check_product_names(
        products
    )

    check_referential_integrity(
        customers,
        products,
        stores,
        transactions
    )

    check_customer_data(
        customers
    )

    check_store_data(
        stores
    )

    transaction_summary(
        transactions,
        products
    )

    print_final_summary(
        customers,
        products,
        stores,
        transactions
    )

    # --------------------------------------------------------
    # Finished
    # --------------------------------------------------------

    print("\n")
    print("=" * 65)
    print("DATA QUALITY ASSESSMENT COMPLETE")
    print("=" * 65)

    print(
        "\nIMPORTANT:"
    )

    print(
        "No files were modified."
    )

    print(
        "The raw datasets remain unchanged."
    )

    print(
        "\nNext step:"
    )

    print(
        "Review the findings and document "
        "the cleaning decisions before "
        "creating the cleaned datasets."
    )


# ============================================================
# RUN SCRIPT
# ============================================================

if __name__ == "__main__":

    main()