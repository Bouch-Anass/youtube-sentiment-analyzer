
# YouTube Sentiment Analyzer

A machine learning application for analyzing YouTube comments and classifying them as positive, neutral, or negative.

The system consists of a Chrome extension, a FastAPI backend, and a machine learning model deployed locally using Docker.

## 1. Project Overview

YouTube videos can receive thousands of comments, making manual sentiment analysis time-consuming.

This project automates the process by extracting comments from a YouTube page, sending them to a machine learning API, and displaying sentiment predictions and statistics.

## 2. Architecture

YouTube Page
    |
    v
Chrome Extension
    |
    v
FastAPI REST API
    |
    v
TF-IDF + Logistic Regression
    |
    v
Sentiment Predictions
    |
    v
Chrome Extension Dashboard

## 3. Technologies

- Python 3.11
- Pandas and scikit-learn
- TF-IDF and Logistic Regression
- FastAPI and Pydantic
- Docker
- JavaScript, HTML, CSS
- Git and GitHub
- Pytest

## 4. Dataset

Dataset: Reddit Sentiment Analysis

Source:
https://github.com/Himanshu-1703/reddit-sentiment-analysis

The dataset contains three sentiment classes:

- -1: Negative
- 0: Neutral
- 1: Positive

After cleaning and duplicate removal:

- Total samples: 36,607
- Training samples: 29,285
- Testing samples: 7,322

An 80/20 stratified split was used.

## 5. Machine Learning

Text vectorization:
- TF-IDF
- Maximum features: 20,000
- N-gram range: (1, 2)

Classifier:
- Logistic Regression
- C = 5
- class_weight = balanced
- max_iter = 1000

Logistic Regression was compared with Linear SVM. It was retained for its competitive classification performance and support for probability estimates.

### Final Performance

| Metric | Value |
|--------|-------|
| Accuracy | 87.50% |
| Macro F1 | 0.86 |
| Negative F1 | 0.80 |
| Neutral F1 | 0.91 |
| Positive F1 | 0.88 |
| Inference (50 comments) | 6.65 ms |
| Local API response (50 comments) | 21.93 ms |

Inference and API response times were measured locally.

## 6. API

The backend provides two endpoints.

### GET /health

Checks the availability of the API and the trained model.

### POST /predict_batch

Accepts a list of comments and returns:

- Predicted sentiment
- Confidence score
- Sentiment counts
- Sentiment percentages

Example request:

```json
{
  "comments": [
    "This video is amazing",
    "This is terrible"
  ]
}
```

## 7. Local Installation

### Requirements

- Python 3.11
- Google Chrome
- Docker Desktop
- Git

### Clone the repository

```bash
git clone <REPOSITORY_URL>
cd <PROJECT_DIRECTORY>
```

Replace the placeholders with the actual GitHub URL and folder name.

### Python environment

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### Run the API locally

```powershell
python -m uvicorn src.api.app:app --reload
```

The API runs at:

http://127.0.0.1:8000

### Run with Docker

```powershell
docker build -t youtube-sentiment-api .
docker run --rm -p 7860:7860 youtube-sentiment-api
```

Docker API:

http://127.0.0.1:7860

API documentation:

http://127.0.0.1:7860/docs

## 8. Chrome Extension Installation

1. Open Chrome.
2. Navigate to chrome://extensions.
3. Enable Developer mode.
4. Click Load unpacked.
5. Select the chrome-extension folder.
6. Open a YouTube video and load its comments.
7. Click Analyze Comments.

The extension currently uses the local Docker API on port 7860.

### Features

- Comment extraction
- Sentiment classification
- Confidence scores
- Sentiment distribution charts
- Sentiment filters
- Dark and light themes
- Copy results
- CSV export

## 9. Testing

The application was tested using Pytest and manual browser tests.

API unit tests: 5 passed.

Docker API integration tests: 8 passed.

Test scenarios included:
- Different batch sizes
- Invalid requests
- Empty comments
- Long comments
- Emojis
- Mixed-language inputs

## 10. Limitations

- The model was trained on Reddit comments rather than YouTube comments.
- Sentiment predictions may be less reliable on slang, sarcasm, emojis, and mixed-language text.
- YouTube loads comments dynamically, so extraction is limited to comments currently loaded on the page.
- The application currently runs locally using Docker.
- Cloud deployment remains pending.

## 11. Future Improvements

- Train or fine-tune on YouTube-specific datasets.
- Improve multilingual sentiment classification.
- Support larger comment collections.
- Add more advanced monitoring and logging.
- Deploy the API to a cloud hosting service.

## 12. Project Status

The local application is operational.

Cloud deployment is not yet implemented.
