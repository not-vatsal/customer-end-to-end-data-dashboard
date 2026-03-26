from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from pathlib import Path

app = FastAPI()

# ✅ Enable CORS (important)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (fine for assignment)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Paths
if "app" in str(Path(__file__)):
    BASE_DIR=Path(__file__).parent

    DATA_DIR = BASE_DIR / "data" / "processed"
else:
    BASE_DIR=Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data" / "processed"



print(DATA_DIR)
# 🔹 Helper function to read CSV safely
def read_csv(file_name):
    file_path = DATA_DIR / file_name
    try:
        df = pd.read_csv(file_path)
        return df.to_dict(orient="records")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"{file_name} not found")


# =========================
# 🔹 API ENDPOINTS
# =========================


@app.get("/")
def read_root():
    return {"message": "Welcome to the Sales Dashboard API"}
@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/revenue")
def get_revenue():
    return read_csv("monthly_revenue.csv")


@app.get("/api/top-customers")
def get_top_customers():
    return read_csv("top_customers.csv")


@app.get("/api/categories")
def get_categories():
    return read_csv("category_performance.csv")


@app.get("/api/regions")
def get_regions():
    return read_csv("regional_analysis.csv")
if __name__=="__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)