import pandas as pd
from utils.snowflake_connector import get_snowflake_connection
from snowflake.connector.pandas_tools import write_pandas

def ingest_to_bronze(csv_path, bronze_table_name):
    """
    Ingests raw data from a CSV file into the Snowflake Bronze layer.
    """
    try:
        # Load raw data from CSV
        df = pd.read_csv(csv_path)
        print(f"Loaded {len(df)} rows from {csv_path}")

        # Connect to Snowflake
        conn = get_snowflake_connection()
        if conn is None:
            raise Exception("Failed to connect to Snowflake.")

        # Write to Snowflake Bronze layer
        success, nchunks, nrows, _ = write_pandas(
            conn=conn,
            df=df,
            table_name=bronze_table_name,
            auto_create_table=True,  # Creates table if it doesn't exist
            overwrite=False          # Appends data (set to True to overwrite)
        )

        print(f"Ingested {nrows} rows into '{bronze_table_name}'")
        conn.close()

    except Exception as e:
        print(f"Error during ingestion: {e}")

# Example usage
if __name__ == "__main__":
    csv_path = "C:/Users/anika.nair/Desktop/Vaccinations.csv"
    bronze_table_name = "BRONZE_LAYER_DATA"
    ingest_to_bronze(csv_path, bronze_table_name)