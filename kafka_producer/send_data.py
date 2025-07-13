
from kafka import KafkaProducer
import json
import time
import pandas as pd

# Load CSV data (subset for testing)
df = pd.read_csv('data/raw/nyc_trip_data.csv')

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic = "nyc_taxi_data"

# Send data in batches
batch_size = 10
for i in range(0, len(df), batch_size):
    batch = df[i:i+batch_size].to_dict(orient="records")

    for record in batch:
        producer.send(topic, value=record)

    print(f"✅ Sent batch {i // batch_size + 1}")
    time.sleep(1)

producer.flush()
producer.close()
