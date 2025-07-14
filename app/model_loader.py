import mlflow
from pathlib import Path
from app.schemas import TripInput


try:
    model = mlflow.sklearn.load_model("model")
    print("✅ Model loaded successfully", model)
except Exception as e:
    print(f"❌ Error loading model: {str(e)}")

def preprocess_input(data: TripInput):
    try:
        input_array = [
            data.vendor_id,
            data.passenger_count,
            data.pickup_longitude,
            data.pickup_latitude,
            data.dropoff_longitude,
            data.dropoff_latitude,
            data.store_and_fwd_flag,
            data.trip_hour,
            data.is_peak_hour,
            data.trip_dayofweek
        ]
        return input_array
    except Exception as e:
        print(f"❌ Error preprocessing input: {str(e)}")
        return None
