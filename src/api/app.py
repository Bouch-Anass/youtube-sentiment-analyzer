
from pathlib import Path
from pydantic import BaseModel, Field, field_validator
import joblib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="YouTube Sentiment Analysis API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)

BASE_DIR = Path(__file__).resolve().parents[2]

model = joblib.load(BASE_DIR / "models/sentiment_model.joblib")
vectorizer = joblib.load(BASE_DIR / "models/tfidf_vectorizer.joblib")


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": True
    }


class CommentBatch(BaseModel):
    comments: list[str] = Field(min_length=1)

    @field_validator("comments")
    @classmethod
    def validate_comments(cls, comments):
        if any(not text.strip() for text in comments):
            raise ValueError("Comments cannot be empty")
        return [text.strip() for text in comments]


@app.post("/predict_batch")
def predict_batch(data: CommentBatch):
    X = vectorizer.transform(data.comments)

    predictions = model.predict(X)
    probabilities = model.predict_proba(X)

    labels = {-1: "negative", 0: "neutral", 1: "positive"}

    results = []

    for text, prediction, probs in zip(
        data.comments, predictions, probabilities
    ):
        results.append({
            "comment": text,
            "sentiment": labels[int(prediction)],
            "confidence": round(float(max(probs)), 4)
        })

    counts = {
        sentiment: sum(
            r["sentiment"] == sentiment for r in results
        )
        for sentiment in labels.values()
    }

    total = len(results)

    return {
        "results": results,
        "statistics": {
            "total": total,
            "counts": counts,
            "percentages": {
                k: round(v / total * 100, 2)
                for k, v in counts.items()
            }
        }
    }
