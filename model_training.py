import os
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Dot, Flatten, Dense
import joblib
import numpy as np
from keras.losses import MeanSquaredError

# Pastikan path folder model output
os.makedirs("backend/app/model", exist_ok=True)

# 1. Load data rating
rating = pd.read_csv("data/tourism_rating.csv")

# 2. Encode user dan tempat jadi angka
user_enc = LabelEncoder()
place_enc = LabelEncoder()
rating['user'] = user_enc.fit_transform(rating['User_Id'])
rating['place'] = place_enc.fit_transform(rating['Place_Id'])

# 3. Hitung jumlah unik user dan tempat
n_users = rating['user'].nunique()
n_places = rating['place'].nunique()

# 4. Bangun model rekomendasi (Matrix Factorization)
user_input = Input(shape=(1,))
place_input = Input(shape=(1,))
user_embed = Embedding(n_users, 64)(user_input)
place_embed = Embedding(n_places, 64)(place_input)
dot = Dot(axes=2)([user_embed, place_embed])
dot = Flatten()(dot)
out = Dense(1)(dot)

model = Model(inputs=[user_input, place_input], outputs=out)
model.compile(optimizer='adam', loss=MeanSquaredError())

# 5. Latih model
print("🔁 Training model...")
model.fit([rating['user'], rating['place']], rating['Place_Ratings'], epochs=5)
print("✅ Model training selesai.")

# 6. Simpan model & encoder
model.save("backend/app/model/recommendation_model.h5")
joblib.dump(user_enc, "backend/app/model/user_encoder.pkl")
joblib.dump(place_enc, "backend/app/model/place_encoder.pkl")
print("✅ Model dan encoder berhasil disimpan.")
