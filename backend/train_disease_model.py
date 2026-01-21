import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import pickle
import os

# Absolute paths (important)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "disease_training.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models", "disease_model.pkl")

# Load dataset
df = pd.read_csv(DATA_PATH)

X = df.drop("disease", axis=1)
y = df["disease"]

# Train model
model = DecisionTreeClassifier()
model.fit(X, y)

# Save model
with open(MODEL_PATH, "wb") as f:
    pickle.dump(model, f)

print("✅ disease_model.pkl created in models/ folder")
