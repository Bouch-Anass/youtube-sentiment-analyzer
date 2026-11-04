
import time
import statistics
import requests

URL = "http://127.0.0.1:8000/predict_batch"

comments = [
    "This video is amazing",
    "I hate this content",
    "The video was uploaded yesterday",
    "Very helpful explanation",
    "This is disappointing"
] * 10

payload = {"comments": comments}

# Warm up
for _ in range(3):
    response = requests.post(URL, json=payload, timeout=10)
    response.raise_for_status()

times = []

for _ in range(10):
    start = time.perf_counter()

    response = requests.post(URL, json=payload, timeout=10)
    response.raise_for_status()

    elapsed = (time.perf_counter() - start) * 1000
    times.append(elapsed)

print("Comments per request:", len(comments))
print("Average response time:", round(statistics.mean(times), 2), "ms")
print("Minimum response time:", round(min(times), 2), "ms")
print("Maximum response time:", round(max(times), 2), "ms")
print("Predictions returned:", response.json()["statistics"]["total"])
