import os
import snowflake.connector
from dotenv import load_dotenv
from snowflake.connector.errors import Error
load_dotenv()

def get_snowflake_connection():
    """Establishes and returns a Snowflake database connection using environment variables for configuration."""
    try:
        conn = snowflake.connector.connect(
            user=os.getenv("SNOWFLAKE_USER"),
            password=os.getenv("SNOWFLAKE_PASSWORD"),
            account=os.getenv("SNOWFLAKE_ACCOUNT"),
            warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
            database=os.getenv("SNOWFLAKE_DATABASE"),
            schema=os.getenv("SNOWFLAKE_SCHEMA")
        )
        return conn
    except Exception as e:
        print(f"Error connecting to Snowflake: {e}")
        return None


def test_connection():
    """
    Tests the Snowflake connection by running a simple query.
    """
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT CURRENT_VERSION()")
        version = cursor.fetchone()
        print(f"Snowflake connection successful. Version: {version[0]}")
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Snowflake connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_connection()


