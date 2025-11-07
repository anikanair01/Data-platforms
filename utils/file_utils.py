import pandas as pd
import os

def read_csv(file_path: str) -> pd.DataFrame:
    """Reads a CSV file and returns a DataFrame."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    return pd.read_csv(file_path)

def write_csv(df: pd.DataFrame, file_path: str) -> None:
    """Writes a DataFrame to a CSV file."""
    df.to_csv(file_path, index=False)

# Example usage:
if __name__ == "__main__":
    # Create sample data
    data = {'name': ['Alice', 'Bob', 'Carter', 'Doug'], 'age': [25, 30, 24, 36]}
    df = pd.DataFrame(data)

    # Write to CSV
    write_csv(df, '../test_output.csv')

    # Read it back
    df_read = read_csv('../test_output.csv')
    print(df_read)