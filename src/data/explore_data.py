from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/processed/reddit_clean.csv")

Path("reports/figures").mkdir(parents=True, exist_ok=True)

# Comment lengths
df["length"] = df["text"].str.len()

print("Text length statistics:")
print(df["length"].describe())

print("\nDuplicate comments:")
print(df.duplicated(subset=["text"]).sum())

# Sentiment distribution
counts = df["label"].value_counts().sort_index()

plt.bar(["Negative", "Neutral", "Positive"], counts.values)
plt.title("Sentiment Distribution")
plt.ylabel("Number of comments")
plt.tight_layout()
plt.savefig("reports/figures/sentiment_distribution.png")
plt.close()

# Text length distribution
plt.hist(df["length"], bins=50)
plt.title("Comment Length Distribution")
plt.xlabel("Number of characters")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("reports/figures/text_lengths.png")
plt.close()

print("\nFigures saved in reports/figures/")