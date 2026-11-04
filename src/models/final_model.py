import time
from pathlib import Path

import pandas as pd
import joblib
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, ConfusionMatrixDisplay

train = pd.read_csv("data/processed/train.csv")
test = pd.read_csv("data/processed/test.csv")

vectorizer = TfidfVectorizer(
    max_features=20000,
    ngram_range=(1, 2),
    min_df=2
)

X_train = vectorizer.fit_transform(train["text"])
X_test = vectorizer.transform(test["text"])

model = LogisticRegression(
    C=5,
    max_iter=1000,
    class_weight="balanced"
)

model.fit(X_train, train["label"])

predictions = model.predict(X_test)

accuracy = accuracy_score(test["label"], predictions)
report = classification_report(test["label"], predictions)

print(f"Accuracy: {accuracy:.4f}")
print(report)

Path("models").mkdir(exist_ok=True)
Path("reports/figures").mkdir(parents=True, exist_ok=True)

joblib.dump(model, "models/sentiment_model.joblib")
joblib.dump(vectorizer, "models/tfidf_vectorizer.joblib")

ConfusionMatrixDisplay.from_predictions(
    test["label"],
    predictions,
    labels=[-1, 0, 1],
    display_labels=["Negative", "Neutral", "Positive"],
    cmap="Blues"
)

plt.tight_layout()
plt.savefig("reports/figures/confusion_matrix.png")
plt.close()

batch = test["text"].iloc[:50]

for _ in range(3):
    model.predict(vectorizer.transform(batch))

times = []

for _ in range(20):
    start = time.perf_counter()
    model.predict(vectorizer.transform(batch))
    times.append((time.perf_counter() - start) * 1000)

average_time = sum(times) / len(times)

print(f"Average inference time (50 comments): {average_time:.2f} ms")

Path("reports/performance.txt").write_text(
    f"Accuracy: {accuracy:.4f}\n\n"
    f"{report}\n"
    f"Inference time (50 comments): {average_time:.2f} ms\n",
    encoding="utf-8"
)

print("Final model and reports saved.")