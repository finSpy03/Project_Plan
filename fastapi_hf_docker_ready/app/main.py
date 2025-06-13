from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    df_place = pd.read_csv("data/tourism_with_id.csv")
    df_rating = pd.read_csv("data/tourism_rating.csv")
    df_user = pd.read_csv("data/user.csv")
except Exception as e:
    print("❌ Gagal load data:", e)
    df_place = pd.DataFrame()
    df_rating = pd.DataFrame()
    df_user = pd.DataFrame()

df_place.fillna({
    "Place_Name": "",
    "City": "",
    "Category": "",
    "Rating": 0,
    "Description": "",
    "Lat": 0.0,
    "Long": 0.0
}, inplace=True)

df_rating.fillna({
    "User_Id": "",
    "Place_Id": "",
    "Place_Ratings": 0
}, inplace=True)

df_user.fillna({
    "User_Id": "",
    "User_Name": "Pengguna"
}, inplace=True)

df_comment = df_rating.merge(df_user, on="User_Id", how="left")

def build_maps_url(lat, lon):
    return f"https://www.google.com/maps?q={lat},{lon}"

def get_comments(place_id):
    rows = df_comment[df_comment["Place_Id"] == place_id].copy()
    rows.sort_values("Place_Ratings", ascending=False, inplace=True)
    rows["User_Name"] = rows.get("User_Name", "Pengguna")
    rows["text"] = rows.apply(
        lambda r: f"⭐ {r['User_Name']} ({r['Place_Ratings']}) - Menyukai tempat ini",
        axis=1
    )
    return rows["text"].tolist()[:3]

@app.get("/recommend/location")
def recommend(
    q: str = Query(...),
    top_n: int = Query(5),
    category: str = Query("Semua")
):
    try:
        keyword = q.strip().lower()
        cat = category.strip().lower()

        result = df_place[
            df_place["City"].str.lower().str.contains(keyword, na=False) |
            df_place["Place_Name"].str.lower().str.contains(keyword, na=False)
        ].copy()

        if cat != "semua":
            result = result[result["Category"].str.lower().str.contains(cat, na=False)]

        result["google_maps"] = result.apply(lambda r: build_maps_url(r["Lat"], r["Long"]), axis=1)
        result["comment"] = result["Place_Id"].apply(get_comments)
        result = result.sort_values("Rating", ascending=False).head(top_n)

        return result[[
            "Place_Id", "Place_Name", "City", "Category", "Rating",
            "Description", "google_maps", "comment"
        ]].to_dict(orient="records")

    except Exception as e:
        print("🔥 ERROR:", e)
        return {"error": str(e)}