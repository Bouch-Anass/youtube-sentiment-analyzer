from pathlib import Path
import pandas as pd
import requests

URL = "https://raw.githubusercontent.com/Himanshu-1703/reddit-sentiment-analysis/refs/heads/main/data/reddit.csv"

output = Path("data/raw/reddit.csv")
output.parent.mkdir(parents=True, exist_ok=True)

response = requests.get(URL, timeout=30)
response.raise_for_status()

output.write_bytes(response.content)

df = pd.read_csv(output)

print("Dataset shape:", df.shape)
print("\nColumns:", df.columns.tolist())
print("\nFirst 5 rows:")
print(df.head())

print("\nMissing values:")
print(df.isnull().sum())