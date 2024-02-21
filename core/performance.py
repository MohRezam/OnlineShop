import requests
import time
def measure_requests_time(n=100):
    start = time.time()
    for _ in range(n):
        requests.get('http://127.0.0.1:8000/')
    end = time.time()
    return end - start

print(measure_requests_time(n=100))