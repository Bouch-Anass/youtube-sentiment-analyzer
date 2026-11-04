import pandas as pd
import joblib

from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Load datasets
train = pd.read_csv("data/processed/train.csv")
test = pd.read_csv("data/processed/test.csv")

# TF-IDF
vectorizer = TfidfVectorizer(
    max_features=20000,
    ngram_range=(1, 2),
    min_df=2
)

X_train = vectorizer.fit_transform(train["text"])
X_test = vectorizer.transform(test["text"])

# Train model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, train["label"])

# Evaluation
predictions = model.predict(X_test)

print("Accuracy:", accuracy_score(test["label"], predictions))
print("\nClassification Report:")
print(classification_report(test["label"], predictions))

# Save model
Path("models").mkdir(exist_ok=True)

joblib.dump(model, "models/sentiment_model.joblib")
joblib.dump(vectorizer, "models/tfidf_vectorizer.joblib")

print("\nModel and vectorizer saved.")