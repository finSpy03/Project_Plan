from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import tensorflow as tf
import joblib
import numpy as np

app = FastAPI()

# Aktifkan CORS agar frontend bisa fetch ke backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Load & gabungkan data wisata dan rating --- #
try:
    df_place = pd.read_csv("data/tourism_with_id.csv")
    df_rating = pd.read_csv("data/tourism_rating.csv")

    # Gabungkan rata-rata rating
    avg_rating = df_rating.groupby("Place_Id")["Place_Ratings"].mean().reset_index()
    df_place = df_place.merge(avg_rating, on="Place_Id", how="left")

    # Isi nilai kosong agar tidak error saat pencarian
    df_place["City"].fillna("", inplace=True)
    df_place["Place_Name"].fillna("", inplace=True)
    df_place["Place_Ratings"].fillna(0, inplace=True)

    # ✅ Tambahan log: tampilkan daftar kota yang tersedia
    print("KOTA YANG TERSEDIA:", df_place["City"].unique())

except Exception as e:
    print("Gagal memuat data:", e)
    df_place = pd.DataFrame(columns=["Place_Id", "Place_Name", "City", "Place_Ratings"])

# --- Load model rekomendasi dan encoder --- #
try:
    model = tf.keras.models.load_model("app/model/recommendation_model.h5")
    user_encoder = joblib.load("app/model/user_encoder.pkl")
    place_encoder = joblib.load("app/model/place_encoder.pkl")
except Exception as e:
    print("Gagal memuat model ML:", e)
    model = None
    user_encoder = None
    place_encoder = None

class UserRequest(BaseModel):
    user_id: str
    top_n: int = 5

@app.post("/recommend")
def recommend_places(request: UserRequest):
    if model is None or user_encoder is None or place_encoder is None:
        return {"recommended_places": []}
    try:
        user_idx = user_encoder.transform([request.user_id])[0]
    except:
        return {"recommended_places": []}
    total_places = len(place_encoder.classes_)
    user_indices = np.full(total_places, user_idx)
    place_indices = np.arange(total_places)
    preds = model.predict([user_indices, place_indices])
    top_indices = preds.flatten().argsort()[-request.top_n:][::-1]
    top_place_ids = place_encoder.inverse_transform(top_indices)
    return {"recommended_places": top_place_ids.tolist()}

@app.get("/recommend/location")
def recommend_by_location(
    q: str = Query(..., description="Nama kota atau lokasi, contoh: Jakarta"),
    top_n: int = Query(5, description="Jumlah hasil rekomendasi")
):
    if df_place.empty:
        return {"error": "Data belum tersedia"}

    # Filter berdasarkan nama kota yang cocok
    mask = df_place["City"].str.contains(q, case=False, na=False) | \
           df_place["Place_Name"].str.contains(q, case=False, na=False)
    result = df_place[mask]

    # Urutkan berdasarkan rating tertinggi
    top_places = result.sort_values("Place_Ratings", ascending=False).head(top_n)

    # Log hasil pencarian ke terminal
    print("Pencarian:", q, "| Ditemukan:", len(top_places))

    # Pilih kolom untuk frontend
    output = top_places[["Place_Id", "Place_Name", "City", "Place_Ratings"]]

    return output.to_dict(orient="records")
