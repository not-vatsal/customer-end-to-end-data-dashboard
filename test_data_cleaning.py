import pytest
import pandas as pd
import numpy as np
from Data_Cleaner.cleaning_customer import clean_customers
from Data_Cleaner.cleaning_orders import parse_date, clean_orders

def test_clean_customers():
    # Setup dummy data
    data = {
        'customer_id': [1, 2, 2],
        'name': [' Alice ', 'Bob', 'Bob '],
        'email': ['ALICE@EXAMPLE.COM', 'invalid-email', 'bob@example.com'],
        'region': [' North ', 'nan', 'South'],
        'signup_date': ['2023-01-01', 'invalid-date', '2023-01-05']
    }
    df = pd.DataFrame(data)
    
    cleaned_df = clean_customers(df)
    
    # 1. Whitespace stripping
    assert cleaned_df.loc[cleaned_df['customer_id'] == 1, 'name'].iloc[0] == 'Alice'
    assert cleaned_df.loc[cleaned_df['customer_id'] == 1, 'region'].iloc[0] == 'North'
    
    # 2. Missing region handling
    assert cleaned_df.loc[cleaned_df['customer_id'] == 2, 'region'].iloc[0] == 'Unknown'
    
    # 3. Email validation and standardization
    assert cleaned_df.loc[cleaned_df['customer_id'] == 1, 'email'].iloc[0] == 'alice@example.com'
    assert cleaned_df.loc[cleaned_df['customer_id'] == 1, 'is_valid_email'].iloc[0] == True
    assert cleaned_df.loc[cleaned_df['email'] == 'invalid-email', 'is_valid_email'].iloc[0] == False
    
    # 4. Duplicate removal (keep latest)
    # The duplicate (Bob) with '2023-01-05' should be kept over 'invalid-date' (NaT)
    assert len(cleaned_df) == 2
    assert cleaned_df.loc[cleaned_df['customer_id'] == 2, 'signup_date'].iloc[0] == pd.Timestamp('2023-01-05')

def test_parse_date():
    # Test multiple formats supported by the custom parser
    assert parse_date("2023-12-31") == pd.Timestamp("2023-12-31")
    assert parse_date("31/12/2023") == pd.Timestamp("2023-12-31")
    assert parse_date("12-31-2023") == pd.Timestamp("2023-12-31")
    assert pd.isna(parse_date("invalid"))

def test_clean_orders():
    # Setup dummy data
    data = {
        'order_id': [101, 102, None, 104], # 102 has same product as 101, None should be dropped
        'customer_id': [1, 2, None, 1],
        'product': ['A', 'A', 'B', 'B'],
        'amount': [10.0, np.nan, 20.0, np.nan],
        'order_date': ['2023-01-01', '31/01/2023', '2023-02-01', '2023-02-02'],
        'status': [' DONE ', 'pending', 'canceled', 'unknown']
    }
    df = pd.DataFrame(data)
    
    cleaned_df = clean_orders(df)
    
    # 1. Drop rows: The row with both order_id=None and customer_id=None should be gone
    assert len(cleaned_df) == 3
    assert not cleaned_df['order_id'].isna().any()
    
    # 2. Imputation: Product A (order 102) should inherit amount from order 101 (10.0)
    assert cleaned_df.loc[cleaned_df['order_id'] == 102, 'amount'].iloc[0] == 10.0
    
    # 3. Status normalization
    assert cleaned_df.loc[cleaned_df['order_id'] == 101, 'status'].iloc[0] == 'completed'
    assert cleaned_df.loc[cleaned_df['order_id'] == 104, 'status'].iloc[0] == 'pending' # 'unknown' maps to NaN, then fillna('pending')