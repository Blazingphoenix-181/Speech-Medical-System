from flask import Flask, request, jsonify
from flask_cors import CORS
from disease_predictor import predict_disease
from medicine_recommender import recommend_medicine

app = Flask(__name__)
CORS(app) 

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    text = data.get("text", "")

    disease = predict_disease(text)
    medicines = recommend_medicine(disease)

    return jsonify({
        "transcript": text,
        "disease": disease,
        "medicines": medicines
    })

if __name__ == "__main__":
    app.run(debug=True)
