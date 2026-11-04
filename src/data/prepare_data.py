import pandas as pd
from pathlib import Path

df = pd.read_csv("data/raw/reddit.csv")

df = df.rename(columns={
    "clean_comment": "text",
    "category": "label"
})

df = df.dropna(subset=["text", "label"])
df["text"] = df["text"].str.strip()
df = df[df["text"] != ""]

df["text"] = df["text"].str.replace(
    r"https?://\S+|www\.\S+|@\w+", "", regex=True
)
df["text"] = df["text"].str.replace(r"\s+", " ", regex=True).str.strip()
df = df[df["text"] != ""]

Path("data/processed").mkdir(parents=True, exist_ok=True)
df.to_csv("data/processed/reddit_clean.csv", index=False)

print("Dataset shape:", df.shape)
print("\nSentiment distribution:")
print(df["label"].value_counts().sort_index())

print("\nPercentages:")
print(df["label"].value_counts(normalize=True).sort_index() * 100)