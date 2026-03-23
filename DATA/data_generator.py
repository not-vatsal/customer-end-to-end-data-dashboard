import pandas as pd
import numpy as np
from faker import Faker
import random



def random_date_format(date):
    formats = [
        "%Y-%m-%d",  # 2024-03-15
        "%d/%m/%Y",  # 15/03/2024
        "%m-%d-%Y"   # 03-15-2024
    ]
    fmt = random.choice(formats)
    return date.strftime(fmt)
fake = Faker()

# Create customers
customers = []
for i in range(100):
    if i%25 == 0 and i!=0:
        customers.append({
            "customer_id": i,
            "name": fake.name(),
            "email": customers[-1]["email"]  ,
            "region": random.choice(["North", "South", "East", "West", None]),
            "signup_date": fake.date_between(start_date='-2y', end_date='today')
        })
    elif i%20==0 and i!=0:
        customers.append(customers[-1])
    else:
        customers.append({
            "customer_id": i,
            "name": fake.name(),
            "email": fake.email() if random.random() > 0.1 else None,
            "region": random.choice(["North", "South", "East", "West", None]),
            "signup_date": fake.date_between(start_date='-2y', end_date='today')
        })
    

customers_df = pd.DataFrame(customers)

# Create products
products = []
for i in range(20):
    products.append({
        "product_id": i,
        "product_name": f"Product_{i}",
        "category": random.choice(["Electronics", "Clothing", "Home"]),
        "unit_price": round(random.uniform(100, 1000), 2)
    })

products_df = pd.DataFrame(products)

# Create orders
orders = []
for i in range(300):
    product = random.choice(products)
    orders.append({
        "order_id": i,
        "customer_id": random.randint(0, 99),
        "product": product["product_name"],
        "amount": round(random.uniform(100, 1000), 2) if random.random() > 0.1 else None,
        "order_date": random_date_format(fake.date_between(start_date='-1y', end_date='today')),
        "status": random.choice(["completed", "pending", "done", "canceled"])
    })

orders_df = pd.DataFrame(orders)

# Save files
customers_df.to_csv("DATA/customers.csv", index=False)
orders_df.to_csv("DATA/orders.csv", index=False)
products_df.to_csv("DATA/products.csv", index=False)

print("Datasets created!")