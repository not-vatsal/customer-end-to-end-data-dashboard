import pandas as pd


# 🔹 Custom date parser
def parse_date(val):
    if pd.isna(val):
        return pd.NaT

    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m-%d-%Y"):
        try:
            return pd.to_datetime(val, format=fmt)
        except:
            continue

    return pd.NaT


def clean_orders(df):
    print("Before cleaning:", df.shape)

    # 1. Parse order_date (multi-format)
    df['order_date'] = df['order_date'].apply(parse_date)

    invalid_dates = df['order_date'].isna().sum()
    print(f" Invalid order_date values: {invalid_dates}")

    # 2. Drop rows where BOTH customer_id and order_id are null
    df = df.dropna(subset=['customer_id', 'order_id'], how='all')

    # 3. Fill missing amount using median per product
    df['amount'] = df['amount'].astype(float)

    df['amount'] = df.groupby('product')['amount'].transform(
        lambda x: x.fillna(x.median())
    )

    # If still null (all values missing for a product)
    df['amount'] = df['amount'].fillna(df['amount'].median())

    # 4. Normalize status
    status_map = {
        'done': 'completed',
        'completed': 'completed',
        'pending': 'pending',
        'canceled': 'cancelled',
        'cancelled': 'cancelled',
        'refunded': 'refunded'
    }

    df['status'] = df['status'].astype(str).str.lower().str.strip()
    df['status'] = df['status'].map(status_map)

    # Optional: fill unknown statuses
    df['status'] = df['status'].fillna('pending')

    # 5. Add order_year_month
    df['order_year_month'] = df['order_date'].dt.to_period('M').astype(str)

    print("After cleaning:", df.shape)

    return df
data=pd.read_csv("DATA/orders.csv")
data=clean_orders(data)
data.to_csv("DATA/processed/orders_clean.csv", index=False)