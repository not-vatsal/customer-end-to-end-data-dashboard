# End-to-End Data Engineering Pipeline & Dashboard

A professional data engineering assignment featuring a complete pipeline from raw data cleaning to a fullstack analytical dashboard. 

## 🚀 Overview
This project implements a robust data pipeline that:
1.  **Cleanses** raw customer and order data using Python and Pandas.
2.  **Analyzes** business metrics including monthly revenue, top customers, and regional performance.
3.  **Serves** processed insights through a FastAPI backend.
4.  **Visualizes** data in a modern, responsive web dashboard.

---

## 📂 Project Structure
```bash
.
├── Data_Cleaner/           # Data cleaning modules (Customers & Orders)
│   ├── cleaning_customer.py
│   └── cleaning_orders.py
├── backend/                # FastAPI application & Docker config
│   ├── backend.py
│   ├── dockerfile
│   └── requirements.txt
├── frontend/               # Vanilla JS Dashboard
│   ├── index.html
│   ├── script.js
│   └── style.css
├── data/                   # Data storage (Raw & Processed)
│   ├── raw/                # Input CSV files
│   └── processed/          # Analytical outputs
├── analyze.py              # Data merging and business logic
├── data_generator.py       # Script to populate raw data
├── docker-compose.yaml     # Container orchestration
└── test_data_cleaning.py   # Pytest suite
```

---

## 🛠️ Setup & Execution

### Prerequisites
- Python 3.9+
- Docker & Docker Compose (optional for containerized run)

### 1. Data Generation & Pipeline
First, populate the datasets and run the cleaning/analysis pipeline:
```bash
# Generate dummy data
python DATA/data_generator.py

# Clean customer data
python Data_Cleaner/cleaning_customer.py

# Clean orders data
python Data_Cleaner/cleaning_orders.py

# Run analysis and generate insights
python analyze.py
```

### 2. Backend (FastAPI)
Run the backend locally:
```bash
cd backend
pip install -r requirements.txt
python backend.py
```
Or via Docker:
```bash
docker compose up --build
```

### 3. Frontend Dashboard
Simply open `frontend/index.html` in your browser. The dashboard automatically connects to the backend at `localhost:8000`.

---

## 📊 Pipeline Logic

### Data Cleaning
*   **Customers**: Removes duplicates, normalizes emails, parses dates, trims whitespace, and fills missing regions with "Unknown".
*   **Orders**: Handles multiple date formats, drops rows with missing IDs, imputes missing amounts using product medians, and normalizes order statuses.

### Analytical Insights
*   **Monthly Revenue**: Aggregated completed orders by month.
*   **Top Customers**: Identifies top 10 high-value customers with a "Churn" flag (no orders in 90 days).
*   **Category Performance**: Revenue and order count per product category.
*   **Regional Analysis**: Customer density and revenue metrics per region.

---

## ✅ Testing
Run the comprehensive test suite to verify cleaning logic:
```bash
pytest test_data_cleaning.py -v
```

## 📝 Assumptions
- Missing product amounts are imputed using the **median** of that specific product to maintain statistical consistency.
- The **Churn Flag** is set for customers whose last completed order was more than 90 days before the latest order in the dataset.
- The system defaults to **'pending'** for any unrecognized order status.
