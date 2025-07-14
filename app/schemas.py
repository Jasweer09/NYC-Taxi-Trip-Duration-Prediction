from pydantic import BaseModel

class TripInput(BaseModel):
    
    passenger_count: int
    vendor_id: int
    pickup_longitude: float
    pickup_latitude: float
    dropoff_longitude: float
    dropoff_latitude: float
    store_and_fwd_flag: int
    trip_hour: int
    is_peak_hour: int
    trip_dayofweek: int 
