from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, to_timestamp, hour, dayofweek
from pyspark.sql.types import StructType, StringType, IntegerType, DoubleType

# Initialize SparkSession
spark = SparkSession.builder \
    .appName("NYC_Taxi_Kafka_Consumer") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Define the schema for the data
schema = StructType() \
    .add("id", StringType()) \
    .add("vendor_id", IntegerType()) \
    .add("pickup_datetime", StringType()) \
    .add("dropoff_datetime", StringType()) \
    .add("passenger_count", IntegerType()) \
    .add("pickup_longitude", DoubleType()) \
    .add("pickup_latitude", DoubleType()) \
    .add("dropoff_longitude", DoubleType()) \
    .add("dropoff_latitude", DoubleType()) \
    .add("store_and_fwd_flag", StringType()) \
    .add("trip_duration", IntegerType())

# Read streaming data from Kafka
raw_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "nyc_taxi_data") \
    .option("startingOffsets", "earliest") \
    .load()

# Convert Kafka 'value' column from bytes to string
json_df = raw_df.selectExpr("CAST(value AS STRING) as json")

# Parse the JSON column and apply schema
parsed_df = json_df.select(from_json(col("json"), schema).alias("data")).select("data.*")

# Data cleaning and feature engineering
processed_df = parsed_df \
    .dropna() \
    .withColumn("pickup_ts", to_timestamp(col("pickup_datetime"))) \
    .withColumn("dropoff_ts", to_timestamp(col("dropoff_datetime"))) \
    .withColumn("trip_dayofweek", dayofweek("pickup_ts")) \
    .withColumn("trip_hour", hour("pickup_ts"))

# Write the processed data to Parquet format
query = processed_df.writeStream \
    .outputMode("append") \
    .format("parquet") \
    .option("path", "data/processed/") \
    .option("checkpointLocation", "data/checkpoints/") \
    .start()

query.awaitTermination()
