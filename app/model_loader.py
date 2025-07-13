import joblib
from pathlib import Path
from app.schemas import TripInput

model = joblib.load(Path("model/random_forest_model.pkl"))

def preprocess_input(data: TripInput):
    return [
        data.passenger_count,
        data.pickup_longitude,
        data.pickup_latitude,
        data.dropoff_longitude,
        data.dropoff_latitude,
        data.store_and_fwd_flag,
        data.trip_hour,
        data.is_peak_hour
    ]
