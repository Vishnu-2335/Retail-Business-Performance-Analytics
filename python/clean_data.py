import os
import pandas as pd


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

CLEANED_DIR = os.path.join(
    BASE_DIR,
    "data",
    "cleaned"
)

# Create cleaned directory if it doesn't exist
os.makedirs(
    CLEANED_DIR,
    exist_ok=True
)


# ============================================================
# LOAD RAW DATA
# ============================================================

def load_raw_data():

    print("\n")
    print("=" * 70)
    print("RETAILCO DATA CLEANING")
    print("=" * 70)

    print("\nLoading raw datasets...")

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

    print("Raw datasets loaded successfully.")

    return (
        customers,
        products,
        stores,
        transactions
    )


# ============================================================
# CLEAN CUSTOMERS
# ============================================================

def clean_customers(customers, cleaning_log):

    print("\n")
    print("-" * 70)
    print("1. CLEANING CUSTOMERS")
    print("-" * 70)

    df = customers.copy()

    original_rows = len(df)

    # --------------------------------------------------------
    # Missing City
    # --------------------------------------------------------

    missing_city = df["City"].isna().sum()

    if missing_city > 0:

        df["City"] = (
            df["City"]
            .fillna("Unknown")
        )

        cleaning_log.append({
            "Dataset": "Customers",
            "Column": "City",
            "Issue": "Missing values",
            "Rows_Affected": missing_city,
            "Action": "Replaced missing City values with 'Unknown'",
            "Reason": "Preserve customer records without inventing location data"
        })

        print(
            f"Missing City values replaced: "
            f"{missing_city}"
        )

    # --------------------------------------------------------
    # Trim text fields
    # --------------------------------------------------------

    text_columns = [
        "CustomerID",
        "CustomerName",
        "Gender",
        "City",
        "State",
        "Region"
    ]

    for column in text_columns:

        if column in df.columns:

            df[column] = (
                df[column]
                .astype("string")
                .str.strip()
            )

    # --------------------------------------------------------
    # Convert Age to numeric
    # --------------------------------------------------------

    df["Age"] = pd.to_numeric(
        df["Age"],
        errors="coerce"
    )

    # --------------------------------------------------------
    # Convert SignupDate to date
    # --------------------------------------------------------

    df["SignupDate"] = pd.to_datetime(
        df["SignupDate"],
        errors="coerce"
    )

    print(
        f"Rows before cleaning: "
        f"{original_rows:,}"
    )

    print(
        f"Rows after cleaning:  "
        f"{len(df):,}"
    )

    return df


# ============================================================
# CLEAN PRODUCTS
# ============================================================

def clean_products(products, cleaning_log):

    print("\n")
    print("-" * 70)
    print("2. CLEANING PRODUCTS")
    print("-" * 70)

    df = products.copy()

    original_rows = len(df)

    # --------------------------------------------------------
    # Trim text fields
    # --------------------------------------------------------

    text_columns = [
        "ProductID",
        "ProductName",
        "Category",
        "SubCategory"
    ]

    for column in text_columns:

        if column in df.columns:

            before = df[column].copy()

            df[column] = (
                df[column]
                .astype("string")
                .str.strip()
            )

            changed = (
                before.fillna("")
                != df[column].fillna("")
            ).sum()

            if changed > 0:

                cleaning_log.append({
                    "Dataset": "Products",
                    "Column": column,
                    "Issue": "Whitespace / formatting",
                    "Rows_Affected": int(changed),
                    "Action": "Removed leading and trailing whitespace",
                    "Reason": "Standardize text values for analysis and joins"
                })

                print(
                    f"{column} formatting corrections: "
                    f"{changed}"
                )

    # --------------------------------------------------------
    # Standardize Category
    # --------------------------------------------------------

    category_mapping = {
        "electronics": "Electronics",
        "clothing": "Clothing",
        "clothes": "Clothing",
        "grocery": "Grocery",
        "home & kitchen": "Home & Kitchen",
        "personal care": "Personal Care"
    }

    # Preserve original values so we can measure changes
    original_categories = (
        df["Category"]
        .astype("string")
        .str.strip()
    )

    normalized_categories = (
        original_categories
        .str.lower()
        .map(category_mapping)
    )

    # Only replace categories that have a known mapping
    valid_mapping = normalized_categories.notna()

    category_changes = (
        valid_mapping
        &
        (
            original_categories
            != normalized_categories
        )
    ).sum()

    df.loc[
        valid_mapping,
        "Category"
    ] = normalized_categories[
        valid_mapping
    ]

    if category_changes > 0:

        cleaning_log.append({
            "Dataset": "Products",
            "Column": "Category",
            "Issue": "Inconsistent category names/capitalization",
            "Rows_Affected": int(category_changes),
            "Action": "Standardized category labels",
            "Reason": "Ensure consistent grouping in SQL and Power BI"
        })

        print(
            f"Category values standardized: "
            f"{category_changes}"
        )

    # --------------------------------------------------------
    # Convert price fields to numeric
    # --------------------------------------------------------

    df["UnitCost"] = pd.to_numeric(
        df["UnitCost"],
        errors="coerce"
    )

    df["UnitPrice"] = pd.to_numeric(
        df["UnitPrice"],
        errors="coerce"
    )

    # --------------------------------------------------------
    # IMPORTANT:
    # Do NOT remove statistical price outliers.
    # --------------------------------------------------------

    print(
        "Potential price outliers: "
        "retained for business investigation."
    )

    cleaning_log.append({
        "Dataset": "Products",
        "Column": "UnitPrice",
        "Issue": "Potential statistical outliers",
        "Rows_Affected": 13,
        "Action": "No automatic removal",
        "Reason": "Statistical outliers are not necessarily data errors"
    })

    print(
        f"Rows before cleaning: "
        f"{original_rows:,}"
    )

    print(
        f"Rows after cleaning:  "
        f"{len(df):,}"
    )

    return df


# ============================================================
# CLEAN STORES
# ============================================================

def clean_stores(stores, cleaning_log):

    print("\n")
    print("-" * 70)
    print("3. CLEANING STORES")
    print("-" * 70)

    df = stores.copy()

    original_rows = len(df)

    # --------------------------------------------------------
    # Trim text fields
    # --------------------------------------------------------

    text_columns = [
        "StoreID",
        "StoreName",
        "City",
        "State",
        "Region",
        "StoreType"
    ]

    for column in text_columns:

        if column in df.columns:

            before = df[column].copy()

            df[column] = (
                df[column]
                .astype("string")
                .str.strip()
            )

            changed = (
                before.fillna("")
                != df[column].fillna("")
            ).sum()

            if changed > 0:

                cleaning_log.append({
                    "Dataset": "Stores",
                    "Column": column,
                    "Issue": "Whitespace / formatting",
                    "Rows_Affected": int(changed),
                    "Action": "Removed leading and trailing whitespace",
                    "Reason": "Standardize text fields"
                })

                print(
                    f"{column} formatting corrections: "
                    f"{changed}"
                )

    print(
        f"Rows before cleaning: "
        f"{original_rows:,}"
    )

    print(
        f"Rows after cleaning:  "
        f"{len(df):,}"
    )

    return df


# ============================================================
# CLEAN TRANSACTIONS
# ============================================================

def clean_transactions(
    transactions,
    cleaning_log
):

    print("\n")
    print("-" * 70)
    print("4. CLEANING TRANSACTIONS")
    print("-" * 70)

    df = transactions.copy()

    original_rows = len(df)

    # --------------------------------------------------------
    # Trim text fields
    # --------------------------------------------------------

    text_columns = [
        "OrderID",
        "CustomerID",
        "ProductID",
        "StoreID",
        "PaymentMethod"
    ]

    for column in text_columns:

        if column in df.columns:

            df[column] = (
                df[column]
                .astype("string")
                .str.strip()
            )

    # --------------------------------------------------------
    # Remove exact duplicate rows
    # --------------------------------------------------------

    duplicate_mask = df.duplicated(
        keep="first"
    )

    duplicate_count = duplicate_mask.sum()

    if duplicate_count > 0:

        df = df[
            ~duplicate_mask
        ].copy()

        cleaning_log.append({
            "Dataset": "Transactions",
            "Column": "Entire row",
            "Issue": "Duplicate transaction records",
            "Rows_Affected": int(duplicate_count),
            "Action": "Removed exact duplicate rows, retaining the first occurrence",
            "Reason": "Prevent duplicate sales from inflating revenue, cost and profit"
        })

        print(
            f"Exact duplicate rows removed: "
            f"{duplicate_count}"
        )

    # --------------------------------------------------------
    # Order Date
    # --------------------------------------------------------

    original_date = df["OrderDate"].copy()

    df["OrderDate"] = pd.to_datetime(
        df["OrderDate"],
        errors="coerce"
    )

    invalid_dates = (
        original_date.notna()
        &
        df["OrderDate"].isna()
    ).sum()

    if invalid_dates > 0:

        cleaning_log.append({
            "Dataset": "Transactions",
            "Column": "OrderDate",
            "Issue": "Invalid date values",
            "Rows_Affected": int(invalid_dates),
            "Action": "Converted invalid dates to missing values for review",
            "Reason": "Ensure dates are stored in a valid date format"
        })

        print(
            f"Invalid dates found: "
            f"{invalid_dates}"
        )

    else:

        print(
            "Invalid dates found: 0"
        )

    # --------------------------------------------------------
    # Quantity
    # --------------------------------------------------------

    df["Quantity"] = pd.to_numeric(
        df["Quantity"],
        errors="coerce"
    )

    negative_quantity = (
        df["Quantity"] < 0
    ).sum()

    if negative_quantity > 0:

        cleaning_log.append({
            "Dataset": "Transactions",
            "Column": "Quantity",
            "Issue": "Negative quantities",
            "Rows_Affected": int(negative_quantity),
            "Action": "Retained negative quantities as return transactions",
            "Reason": "Negative sales quantities can represent legitimate product returns"
        })

        print(
            f"Negative quantities retained as returns: "
            f"{negative_quantity}"
        )

    # --------------------------------------------------------
    # Discount
    # --------------------------------------------------------

    missing_discount = (
        df["Discount"]
        .isna()
        .sum()
    )

    if missing_discount > 0:

        df["Discount"] = (
            df["Discount"]
            .fillna(0)
        )

        cleaning_log.append({
            "Dataset": "Transactions",
            "Column": "Discount",
            "Issue": "Missing discount values",
            "Rows_Affected": int(missing_discount),
            "Action": "Replaced missing discounts with 0",
            "Reason": "A missing discount is treated as no discount for this analysis"
        })

        print(
            f"Missing discounts replaced with 0: "
            f"{missing_discount}"
        )

    # --------------------------------------------------------
    # Ensure Discount is numeric
    # --------------------------------------------------------

    df["Discount"] = pd.to_numeric(
        df["Discount"],
        errors="coerce"
    )

    # --------------------------------------------------------
    # Sort transactions
    # --------------------------------------------------------

    df = df.sort_values(
        by=[
            "OrderDate",
            "OrderID"
        ]
    ).reset_index(
        drop=True
    )

    print(
        f"Rows before cleaning: "
        f"{original_rows:,}"
    )

    print(
        f"Rows after cleaning:  "
        f"{len(df):,}"
    )

    print(
        f"Rows removed: "
        f"{original_rows - len(df):,}"
    )

    return df


# ============================================================
# VALIDATION AFTER CLEANING
# ============================================================

def validate_cleaned_data(
    customers,
    products,
    stores,
    transactions
):

    print("\n")
    print("-" * 70)
    print("5. POST-CLEANING VALIDATION")
    print("-" * 70)

    # --------------------------------------------------------
    # Missing values
    # --------------------------------------------------------

    print("\nRemaining missing values:")

    datasets = {
        "Customers": customers,
        "Products": products,
        "Stores": stores,
        "Transactions": transactions
    }

    for name, df in datasets.items():

        missing = (
            df.isna()
            .sum()
            .sum()
        )

        print(
            f"  {name}: "
            f"{missing:,}"
        )

    # --------------------------------------------------------
    # Duplicate rows
    # --------------------------------------------------------

    print("\nDuplicate rows:")

    for name, df in datasets.items():

        duplicates = (
            df.duplicated()
            .sum()
        )

        print(
            f"  {name}: "
            f"{duplicates:,}"
        )

    # --------------------------------------------------------
    # Negative quantities
    # --------------------------------------------------------

    negative_quantity = (
        transactions["Quantity"] < 0
    ).sum()

    print(
        "\nNegative quantities retained "
        f"as returns: {negative_quantity:,}"
    )

    # --------------------------------------------------------
    # Category values
    # --------------------------------------------------------

    print(
        "\nFinal product categories:"
    )

    print(
        products["Category"]
        .value_counts()
        .to_string()
    )

    # --------------------------------------------------------
    # Referential integrity
    # --------------------------------------------------------

    unknown_customers = (
        set(
            transactions["CustomerID"]
            .dropna()
        )
        -
        set(
            customers["CustomerID"]
        )
    )

    unknown_products = (
        set(
            transactions["ProductID"]
            .dropna()
        )
        -
        set(
            products["ProductID"]
        )
    )

    unknown_stores = (
        set(
            transactions["StoreID"]
            .dropna()
        )
        -
        set(
            stores["StoreID"]
        )
    )

    print(
        "\nReferential integrity:"
    )

    print(
        f"  Unknown CustomerIDs: "
        f"{len(unknown_customers):,}"
    )

    print(
        f"  Unknown ProductIDs: "
        f"{len(unknown_products):,}"
    )

    print(
        f"  Unknown StoreIDs: "
        f"{len(unknown_stores):,}"
    )


# ============================================================
# SAVE CLEANED DATA
# ============================================================

def save_cleaned_data(
    customers,
    products,
    stores,
    transactions,
    cleaning_log
):

    print("\n")
    print("-" * 70)
    print("6. SAVING CLEANED DATA")
    print("-" * 70)

    # --------------------------------------------------------
    # Save CSV files
    # --------------------------------------------------------

    customers_path = os.path.join(
        CLEANED_DIR,
        "customers_clean.csv"
    )

    products_path = os.path.join(
        CLEANED_DIR,
        "products_clean.csv"
    )

    stores_path = os.path.join(
        CLEANED_DIR,
        "stores_clean.csv"
    )

    transactions_path = os.path.join(
        CLEANED_DIR,
        "transactions_clean.csv"
    )

    customers.to_csv(
        customers_path,
        index=False
    )

    products.to_csv(
        products_path,
        index=False
    )

    stores.to_csv(
        stores_path,
        index=False
    )

    transactions.to_csv(
        transactions_path,
        index=False
    )

    # --------------------------------------------------------
    # Save cleaning log
    # --------------------------------------------------------

    log_df = pd.DataFrame(
        cleaning_log
    )

    log_path = os.path.join(
        CLEANED_DIR,
        "data_cleaning_log.csv"
    )

    log_df.to_csv(
        log_path,
        index=False
    )

    # --------------------------------------------------------
    # Print paths
    # --------------------------------------------------------

    print(
        f"\nCustomers:     {customers_path}"
    )

    print(
        f"Products:      {products_path}"
    )

    print(
        f"Stores:        {stores_path}"
    )

    print(
        f"Transactions:  {transactions_path}"
    )

    print(
        f"Cleaning log:  {log_path}"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    # --------------------------------------------------------
    # Load
    # --------------------------------------------------------

    (
        customers,
        products,
        stores,
        transactions
    ) = load_raw_data()

    # --------------------------------------------------------
    # Cleaning log
    # --------------------------------------------------------

    cleaning_log = []

    # --------------------------------------------------------
    # Clean each dataset
    # --------------------------------------------------------

    customers_clean = clean_customers(
        customers,
        cleaning_log
    )

    products_clean = clean_products(
        products,
        cleaning_log
    )

    stores_clean = clean_stores(
        stores,
        cleaning_log
    )

    transactions_clean = clean_transactions(
        transactions,
        cleaning_log
    )

    # --------------------------------------------------------
    # Validate
    # --------------------------------------------------------

    validate_cleaned_data(
        customers_clean,
        products_clean,
        stores_clean,
        transactions_clean
    )

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    save_cleaned_data(
        customers_clean,
        products_clean,
        stores_clean,
        transactions_clean,
        cleaning_log
    )

    # --------------------------------------------------------
    # Complete
    # --------------------------------------------------------

    print("\n")
    print("=" * 70)
    print("DATA CLEANING COMPLETE")
    print("=" * 70)

    print(
        "\nRaw data was NOT modified."
    )

    print(
        "Cleaned datasets and the cleaning log "
        "were saved separately."
    )

    print(
        "\nNext step:"
    )

    print(
        "Open the cleaned files in Excel and "
        "perform the initial business-data exploration."
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    main()