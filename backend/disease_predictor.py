import os
import pickle
import pandas as pd

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "disease_model.pkl")

# Load model
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

# MUST match disease_training.csv exactly (except 'disease')
symptoms = [
    "fever",
    "headache",
    "cough",
    "allergy",
    "body_pain",
    "sore_throat",
    "diarrhea",
    "stomach_pain"
]

# Bengali → English symptom mapping
BENGALI_SYMPTOM_MAP = {
    "জ্বর": "fever",
    "মাথাব্যথা": "headache",
    "মাথা ব্যথা": "headache",
    "কাশি": "cough",
    "গলা ব্যথা": "sore_throat",
    "গলা ব্যাথা": "sore_throat",
    "শরীর ব্যথা": "body_pain",
    "দুর্বল": "fatigue",   # not used but safe
    "ক্লান্ত": "fatigue", # not used but safe
    "ডায়রিয়া": "diarrhea",
    "পাতলা পায়খানা": "diarrhea",
    "পেট ব্যথা": "stomach_pain"
}

import os
import pickle
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "disease_model.pkl")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

symptoms = [
    "fever",
    "headache",
    "cough",
    "allergy",
    "body_pain",
    "sore_throat",
    "diarrhea",
    "stomach_pain"
]

BENGALI_SYMPTOM_MAP = {
    "জ্বর": "fever",
    "মাথাব্যথা": "headache",
    "কাশি": "cough",
    "গলা ব্যথা": "sore_throat",
    "শরীর ব্যথা": "body_pain",
    "ডায়রিয়া": "diarrhea",
    "পাতলা পায়খানা": "diarrhea",
    "পেট ব্যথা": "stomach_pain"
}

def predict_disease(text: str) -> str:
    text = text.lower().strip()

    # Bengali → English
    for bn, en in BENGALI_SYMPTOM_MAP.items():
        if bn in text:
            text += f" {en}"

    # 🔒 HARD RULES (NO ML ALLOWED)
    if "fever" in text and not any(x in text for x in ["diarrhea", "stomach"]):
        return "Viral Fever"
    if "headache" in text and "fever" not in text:
        return "Migraine"
    if any(x in text for x in ["diarrhea", "loose motion", "stomach pain"]):
        return "Stomach Infection"

    if "headache" in text and "fever" not in text:
        return "Migraine"

    if "allergy" in text:
        return "Allergy"

    if "cough" in text and "sore throat" in text:
        return "Cold"

    # 🧠 ML ONLY FOR UNCLEAR CASES
    vector = [1 if s.replace("_", " ") in text else 0 for s in symptoms]
    df = pd.DataFrame([vector], columns=symptoms)

    return model.predict(df)[0]

