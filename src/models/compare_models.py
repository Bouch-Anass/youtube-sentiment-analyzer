import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

df = pd.read_csv("data/processed/train.csv")

X_train, X_val, y_train, y_val = train_test_split(
    df["text"],
    df["label"],
    test_size=0.2,
    stratify=df["label"],
    random_state=42
)

vectorizer = TfidfVectorizer(
    max_features=20000,
    ngram_range=(1, 2),
    min_df=2
)

X_train = vectorizer.fit_transform(X_train)
X_val = vectorizer.transform(X_val)

for weight in [None, "balanced"]:
    model = LogisticRegression(
        max_iter=1000,
        class_weight=weight
    )

    model.fit(X_train, y_train)
    predictions = model.predict(X_val)

    print(f"\nClass weight: {weight}")
    print(classification_report(y_val, predictions))