from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import pandas as pd
import numpy as np

from app.schemas import TripInput
from app.model_loader import model, preprocess_input

app = FastAPI()
templates = Jinja2Templates(directory="templates")
@app.post("/predict", response_class=HTMLResponse)
def predict_duration(
    request: Request,
    passenger_count: int = Form(...),
    vendor_id: int = Form(...),
    pickup_longitude: float = Form(...),
    pickup_latitude: float = Form(...),
    dropoff_longitude: float = Form(...),
    dropoff_latitude: float = Form(...),
    store_and_fwd_flag: int = Form(...),
    trip_hour: int = Form(...),
    is_peak_hour: int = Form(...),
    trip_dayofweek: int = Form(...)
):
    # Create TripInput Pydantic model instance
    trip_input = TripInput(
        vendor_id=vendor_id,
        passenger_count=passenger_count,
        pickup_longitude=pickup_longitude,
        pickup_latitude=pickup_latitude,
        dropoff_longitude=dropoff_longitude,
        dropoff_latitude=dropoff_latitude,
        store_and_fwd_flag=store_and_fwd_flag,
        trip_hour=trip_hour,
        is_peak_hour=is_peak_hour,
        trip_dayofweek=trip_dayofweek
    )

    # Preprocess input once
    input_array = preprocess_input(trip_input)

    if input_array is None:
        return templates.TemplateResponse("index.html", {"request": request, "error": "Invalid input"})

    # Columns must be in the same order as input_array
    input_df = pd.DataFrame([input_array], columns=[
        'vendor_id', 'passenger_count', 'pickup_longitude', 'pickup_latitude',
        'dropoff_longitude', 'dropoff_latitude', 'store_and_fwd_flag',
        'trip_hour', 'is_peak_hour', 'trip_dayofweek'
    ])

    try:
        prediction = model.predict(input_df)
        result = float(np.round(prediction[0], 2))
        return templates.TemplateResponse("index.html", {
            "request": request,
            "prediction": result
        })
    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": f"Prediction error: {str(e)}"
        })