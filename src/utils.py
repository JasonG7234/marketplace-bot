import requests
import time

def post_request(url, headers, payload, max_retry_count=3):
    count = 0
    while count < max_retry_count:
        try:
            response = requests.post(
                url, headers, data=payload, timeout=15)
            return response
        except requests.exceptions.RequestException:
            print("Request error, giving it 10 and retrying")
            time.sleep(10)
            count += 1
    raise requests.exceptions.RequestException("ERROR: Failed to receive response from server after number of retries.")