from pyspark.sql import SparkSession
from pyspark.sql.functions import when, col

# Initialize SparkSession
spark = SparkSession.builder \
    .appName("NYC_Taxi_Preprocessing") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Load processed parquet data
df = spark.read.parquet("data/processed/")

# Encode categorical feature
df = df.withColumn("store_and_fwd_flag", when(col("store_and_fwd_flag") == 'Y', 1).otherwise(0))

# Create is_peak_hour feature
df = df.withColumn(
    "is_peak_hour",
    when((col("trip_hour").between(7, 9)) | (col("trip_hour").between(16, 19)), 1).otherwise(0)
)

# Drop unneeded columns (corrected the typo)
columns_to_drop = ["id", "pickup_datetime", "dropoff_datetime", "pickup_ts", "dropoff_ts"]
df = df.drop(*columns_to_drop)

df.select([col(c).isNull().alias(c) for c in df.columns]).summary("count").show()

# Drop rows with null values
df = df.dropna()

# Log row count and schema
print(f"Remaining records after dropna: {df.count()}")
print("Final training columns:")
df.printSchema()

# Save final clean dataset
df.write.mode("overwrite").parquet("data/final/")
print("Preprocessed data with peak hour saved to: data/final/")
