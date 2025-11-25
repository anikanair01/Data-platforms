import os
import logging
from pyspark.sql.functions import col, to_date
from dotenv import load_dotenv
from common.Spark_session import get_spark_session
from utils.snowflake_connector import get_snowflake_connection # ✅ Helper for Snowflake connection

# ✅ Load environment variables
load_dotenv()

# ✅ Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# ✅ Initialize Spark session
spark = get_spark_session()

# ✅ Bronze tables list
bronze_tables = [
    "BRONZE_VACCINATIONS",
    "BRONZE_INDEX",
    "BRONZE_DEMOGRAPHICS",
    "BRONZE_EPIDEMIOLOGY",
    "BRONZE_GEOGRAPHY",
    "BRONZE_HOSPITALIZATIONS"
]

# ✅ Cleaning rules
cleaning_rules = {
    "BRONZE_VACCINATIONS": lambda df: df.dropDuplicates().withColumn("DATE", to_date(col("DATE"))),
    "BRONZE_INDEX": lambda df: df.dropDuplicates(),
    "BRONZE_DEMOGRAPHICS": lambda df: df.dropDuplicates(),
    "BRONZE_EPIDEMIOLOGY": lambda df: df.dropDuplicates().withColumn("REPORT_DATE", to_date(col("REPORT_DATE"))),
    "BRONZE_GEOGRAPHY": lambda df: df.dropDuplicates(),
    "BRONZE_HOSPITALIZATIONS": lambda df: df.dropDuplicates()
}

# ✅ Paths for Bronze layer (if reading from files)
bronze_path = os.getenv("BRONZE_PATH", "/data/bronze/")

# ✅ Snowflake options for Silver schema
snowflake_options = get_snowflake_connection(schema="PUBLIC")

# ✅ Process each table
for table in bronze_tables:
    try:
        logging.info(f"Processing {table} → Silver")

        # Read Bronze data (from local or Snowflake)
        df = spark.read.format("parquet").load(os.path.join(bronze_path, table.lower()))

        # Apply cleaning
        clean_func = cleaning_rules.get(table, lambda x: x)
        df_clean = clean_func(df)

        # Determine Silver table name
        silver_table = table.replace("BRONZE", "SILVER")

        # ✅ Write cleaned data to Snowflake Silver table
        df_clean.write.format("snowflake") \
            .options(**snowflake_options) \
            .option("dbtable", silver_table) \
            .mode("overwrite") \
            .save()

        logging.info(f"✅ Loaded {silver_table} into Snowflake")
    except Exception as e:
        logging.error(f"❌ Failed for {table}: {str(e)}")
