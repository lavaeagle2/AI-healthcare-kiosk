import joblib

# Load model and encoder once
model = joblib.load("model.pkl")
mlb = joblib.load("encoder.pkl")

def predict_disease(symptoms_list):
    # Clean input
    symptoms_list = [s.strip().lower() for s in symptoms_list]

    # Filter unknown symptoms
    known = set(mlb.classes_)
    filtered = [s for s in symptoms_list if s in known]

    if not filtered:
        return "Unknown"

    # Transform + predict
    X = mlb.transform([filtered])
    prediction = model.predict(X)[0]

    return prediction