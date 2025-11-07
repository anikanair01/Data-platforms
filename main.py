from unittest.mock import patch, MagicMock
import snowflake.connector

def test_snowflake_connection():
    with patch('snowflake.connector.connect') as mock_connect:
        # Simulate a successful connection and query
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = ['7.0.0']  # Fake version
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        # Your actual connection code
        conn = snowflake.connector.connect(
            user='fake_user',
            password='fake_pass',
            account='fake_account',
            warehouse='fake_warehouse',
            database='fake_db',
            schema='fake_schema'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT CURRENT_VERSION();")
        version = cursor.fetchone()

        print("Mocked Snowflake version:", version[0])


