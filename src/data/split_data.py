import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv("data/processed/reddit_clean.csv")

df = df[df.groupby("text")["label"].transform("nunique") == 1]
df = df.drop_duplicates(subset="text")

train, test = train_test_split(
    df,
    test_size=0.2,
    random_state=42,
    stratify=df["label"]
)

train.to_csv("data/processed/train.csv", index=False)
test.to_csv("data/processed/test.csv", index=False)

print("Training samples:", len(train))
print("Testing samples:", len(test))

print("\nTraining distribution:")
print(train["label"].value_counts().sort_index())

print("\nTesting distribution:")
print(test["label"].value_counts().sort_index())