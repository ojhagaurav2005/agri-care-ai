import joblib
import os


MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "crop_disease_model.pkl"
)

model = joblib.load(MODEL_PATH)


def predict_disease(symptoms):
    prediction = model.predict([symptoms])[0]

    probabilities = model.predict_proba([symptoms])[0]
    confidence = max(probabilities)

    return {
        "prediction": prediction,
        "confidence": round(float(confidence) * 100, 2)
    }