from fastapi import FastAPI
from app.schemas import TripInput
from app.model_loader import model, preprocess_input
import numpy as np

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Taxi Trip Duration Predictor is live 🎯"}

@app.post("/predict")
def predict_duration(data: TripInput):
    input_array = preprocess_input(data)
    prediction = model.predict([input_array])
    return {"predicted_trip_duration": float(np.round(prediction[0], 2))}
