import pandas as pd
data=pd.read_csv("DATA/customers.csv")




def clean_customers(df):
    print("Before cleaning:", df.shape)

    # 1. Strip whitespace
    df['name'] = df['name'].astype(str).str.strip()
    df['region'] = df['region'].astype(str).str.strip()

    # 2. Fill missing region
    df['region'] = df['region'].replace(['None', 'nan', ''], pd.NA)
    df['region'] = df['region'].fillna('Unknown')

    # 3. Standardize email
    df['email'] = df['email'].astype(str).str.lower()

    # 4. Validate email
    df['is_valid_email'] = df['email'].apply(
        lambda x: True if ('@' in x and '.' in x) else False
    )

    # Fix cases where email was originally missing
    df.loc[df['email'].isin(['none', 'nan']), 'is_valid_email'] = False

    # 5. Parse signup_date
    df['signup_date'] = pd.to_datetime(df['signup_date'], errors='coerce')

    # Log invalid dates
    invalid_dates = df['signup_date'].isna().sum()
    print(f" Invalid signup_date values: {invalid_dates}")

    # 6. Remove duplicates (keep latest signup_date)
    df = df.sort_values(by='signup_date', ascending=False)

    df = df.drop_duplicates(subset='customer_id', keep='first')

    print("After cleaning:", df.shape)

    return df
data=clean_customers(data)
data.to_csv("DATA/processed/customers_clean.csv", index=False)