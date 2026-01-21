import os
import pandas as pd
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "medicines.csv")

# Load once
df = pd.read_csv(DATA_PATH)

# Normalize disease names ONCE
df["disease_norm"] = df["disease"].str.strip().str.lower()

def recommend_medicine(disease: str) -> str:
    if not disease:
        return "Consult a doctor"

    disease_norm = disease.strip().lower()

    matches = df[df["disease_norm"] == disease_norm]

    if matches.empty:
        return "Consult a doctor"

    # Pick exactly ONE random medicine
    return random.choice(matches["medicines"].tolist())
