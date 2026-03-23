import pandas as pd
RAW_DIR="DATA/"
PROCESSED_DIR = "DATA/processed/"


# 🔹 Safe data loader
def load_csv(path):
    try:
        df = pd.read_csv(path)
        if df.empty:
            raise ValueError(f"{path} is empty")
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {path}")
    except pd.errors.EmptyDataError:
        raise ValueError(f"Empty data: {path}")


def main():
    # =========================
    # LOAD DATA
    # =========================
    customers = load_csv(PROCESSED_DIR + "customers_clean.csv")
    orders = load_csv(PROCESSED_DIR + "orders_clean.csv")
    products = load_csv(RAW_DIR + "products.csv")

    # =========================
    # 2.1 MERGING
    # =========================

    # 🔹 Merge 1: orders + customers
    orders_with_customers = pd.merge(
        orders,
        customers,
        on="customer_id",
        how="left"
    )

    # 🔹 Merge 2: + products
    full_data = pd.merge(
        orders_with_customers,
        products,
        left_on="product",
        right_on="product_name",
        how="left"
    )

    # 🔹 Report missing joins
    missing_customers = orders_with_customers['name'].isna().sum()
    missing_products = full_data['product_name'].isna().sum()

    print(f"Orders with no matching customer: {missing_customers}")
    print(f"Orders with no matching product: {missing_products}")

    # =========================
    # 2.2 ANALYSIS
    # =========================

    # Filter only completed orders
    completed = full_data[full_data['status'] == 'completed']

    # 🔹 1. Monthly Revenue
    monthly_revenue = (
        completed.groupby('order_year_month')['amount']
        .sum()
        .reset_index(name='total_revenue')
    )

    monthly_revenue.to_csv(PROCESSED_DIR + "monthly_revenue.csv", index=False)

    # 🔹 2. Top Customers
    top_customers = (
        completed.groupby(['customer_id', 'name', 'region'])['amount']
        .sum()
        .reset_index(name='total_spend')
        .sort_values(by='total_spend', ascending=False)
        .head(10)
    )

    # 🔹 5. Churn calculation (before saving top customers)
    latest_date = pd.to_datetime(full_data['order_date']).max()
    cutoff_date = latest_date - pd.Timedelta(days=90)

    last_orders = (
        completed.groupby('customer_id')['order_date']
        .max()
        .reset_index(name='last_order_date')
    )
    last_orders['last_order_date'] = pd.to_datetime(last_orders['last_order_date'], errors='coerce')

    last_orders['churned'] = last_orders['last_order_date'] < cutoff_date

    # Merge churn info into top customers
    top_customers = pd.merge(
        top_customers,
        last_orders[['customer_id', 'churned']],
        on='customer_id',
        how='left'
    )

    top_customers.to_csv(PROCESSED_DIR + "top_customers.csv", index=False)

    # 🔹 3. Category Performance
    category_performance = (
        completed.groupby('category')
        .agg(
            total_revenue=('amount', 'sum'),
            avg_order_value=('amount', 'mean'),
            num_orders=('amount', 'count')
        )
        .reset_index()
    )

    category_performance.to_csv(PROCESSED_DIR + "category_performance.csv", index=False)

    # 🔹 4. Regional Analysis
    regional_analysis = (
        full_data.groupby('region')
        .agg(
            num_customers=('customer_id', 'nunique'),
            num_orders=('order_id', 'count'),
            total_revenue=('amount', 'sum')
        )
        .reset_index()
    )

    regional_analysis['avg_revenue_per_customer'] = (
        regional_analysis['total_revenue'] / regional_analysis['num_customers']
    )

    regional_analysis.to_csv(PROCESSED_DIR + "regional_analysis.csv", index=False)

    print(" Analysis completed successfully!")


if __name__ == "__main__":
    main()