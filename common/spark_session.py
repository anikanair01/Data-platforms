import spark
from pyspark.sql import SparkSession
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

def get_spark_session():
    return SparkSession.builder \
        .appName("SnowflakePipeline") \
        .master(os.getenv("SPARK_MASTER", "local[*]")) \
        .config("spark.shuffle.push.enabled", "false") \
        .config("spark.jars", os.getenv("SPARK_JARS", "")) \
        .getOrCreate()

def get_snowflake_options(schema):
    account = os.getenv("SNOWFLAKE_ACCOUNT")
    sf_url = account if account.endswith(".snowflakecomputing.com") else account + ".snowflakecomputing.com"
    return {
        "sfURL": sf_url,
        "sfUser": os.getenv("SNOWFLAKE_USER"),
        "sfPassword": os.getenv("SNOWFLAKE_PASSWORD"),
        "sfDatabase": os.getenv("SNOWFLAKE_DATABASE"),
        "sfSchema": schema,
        "sfWarehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
    }

def print_box(message):
    border = "+" + "-" * (len(message) + 2) + "+"
    print(border)
    print(f"| {message} |")
    print(border)

if __name__ == "__main__":
    print("✅ Starting Spark-Snowflake connection test...")
    spark = get_spark_session()

    schema = os.getenv("SNOWFLAKE_SCHEMA", "PUBLIC")
    options = get_snowflake_options(schema)

    try:
        df = spark.read.format("snowflake") \
            .options(**options) \
            .option("query", "SELECT CURRENT_TIMESTAMP") \
            .load()
        timestamp = df.collect()[0][0]  # Get timestamp from Snowflake
        print_box(f"✅ Connection successful at {timestamp}")
    except Exception as e:
        print_box(f"❌ Connection failed at {datetime.now()}")
        print("Error:", str(e))


