
FROM python:3.11-slim

WORKDIR /app

COPY requirements-prod.txt .

RUN pip install --no-cache-dir -r requirements-prod.txt

COPY src/ ./src/
COPY models/ ./models/
COPY app_api.py .

RUN useradd -m -u 1000 user
USER user

EXPOSE 7860

CMD ["uvicorn", "app_api:app", "--host", "0.0.0.0", "--port", "7860"]
