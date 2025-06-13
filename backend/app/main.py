from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np

app = FastAPI()

# Aktifkan CORS biar frontend bisa akses API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data wisata
try:
    df_place = pd.read_csv("data/tourism_with_id.csv")
except Exception as e:
    print("❌ Gagal memuat file tourism_with_id.csv:", e)
    df_place = pd.DataFrame()

# Isi nilai kosong agar tidak error saat akses kolom
df_place.fillna({
    "Place_Name": "",
    "City": "",
    "Category": "",
    "Rating": 0,
    "Description": "",
    "Lat": 0.0,
    "Long": 0.0
}, inplace=True)

# Buat link ke Google Maps dari koordinat
def build_maps_url(lat, lon):
    return f"https://www.google.com/maps?q={lat},{lon}"

# Endpoint pencarian berdasarkan kota atau nama tempat
@app.get("/recommend/location")
def recommend_by_location(q: str = Query(...), top_n: int = 5):
    q = q.lower()
    try:
        result = df_place[
            df_place["City"].str.lower().str.contains(q, na=False) |
            df_place["Place_Name"].str.lower().str.contains(q, na=False)
        ].copy()

        # Link ke Google Maps dan komentar dummy
        result["google_maps"] = result.apply(lambda row: build_maps_url(row["Lat"], row["Long"]), axis=1)
        result["comment"] = "🔎 Berdasarkan pencarian kata: " + q

        # Urutkan berdasarkan rating tertinggi dan ambil top_n
        result = result.sort_values("Rating", ascending=False).head(top_n)

        return result[[
            "Place_Id",
            "Place_Name",
            "City",
            "Category",
            "Rating",
            "Description",
            "google_maps",
            "comment"
        ]].to_dict(orient="records")
    except Exception as e:
        print("🔥 ERROR:", e)
        return {"error": str(e)}
