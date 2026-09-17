# Retail Business Performance Analytics

An end-to-end retail analytics project focused on analyzing sales, profitability, customer behavior, product performance, regional performance, and trends over time.

## Tech Stack

- Python
- Pandas
- Excel
- Power BI
- DAX

## Dataset

The project uses a fictional retail dataset containing:

| Dataset | Records |
|---|---:|
| Customers | 8,000 |
| Products | 150 |
| Stores | 25 |
| Transactions | 1,000 |

The transaction data includes order, customer, product, store, quantity, discount, payment, revenue, cost, and profit information.

## Data Preparation

Python was used to:

- Generate the dataset
- Validate data quality
- Identify missing values, duplicates, inconsistencies, and outliers
- Clean and standardize the data
- Produce the final cleaned datasets

Excel was then used for initial data exploration and PivotTable analysis.

## Power BI Dashboard

The cleaned data was imported into Power BI and modeled using customer, product, store, transaction, and date tables.

The dashboard contains five pages:

### Executive Overview
- Revenue and profit KPIs
- Revenue by category and region
- Profit by category
- Monthly revenue trend

### Product & Category
- Top 10 products by revenue
- Top 10 products by profit
- Profit margin by category

### Customer Analysis
- Top 10 customers by revenue
- Top 10 customers by profit

### Regional Analysis
- Revenue by region
- Profit by region
- Profit margin by region
- Orders by region
- Monthly revenue by region

### Time Analysis
- Monthly revenue
- Monthly orders
- Monthly profit
- Monthly profit margin
- Revenue by year

## Project Structure

```text
Retail-Business-Analytics/
│
├── data/
│   ├── raw/
│   └── cleaned/
│
├── python/
│   ├── generate_data.py
│   ├── validate_data.py
│   └── clean_data.py
│
├── excel/
│   └── Retail_Business_Analysis.xlsx
│
├── powerbi/
│   └── Retail_Business_Analytics.pbix
│
└── README.md