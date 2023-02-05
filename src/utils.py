import requests
import time

API_URL = "https://www.facebook.com/api/graphql/"
HEADERS = {
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
}

def post_request(payload, url=API_URL, headers=HEADERS, max_retry_count=3):
    count = 0
    while count < max_retry_count:
        try:
            response = requests.post(
                url, headers=headers, data=payload, timeout=15)
            return response
        except requests.exceptions.RequestException:
            print("Request error, giving it 10 and retrying")
            time.sleep(10)
            count += 1
    raise requests.exceptions.RequestException("ERROR: Failed to receive response from server after number of retries.")