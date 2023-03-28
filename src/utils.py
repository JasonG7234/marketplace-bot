import requests
import time

API_URL = "https://www.facebook.com/api/graphql/"
HEADERS = {
    "sec-fetch-site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
    "Accept": "*/*",
    "Content-Type": "application/x-www-form-urlencoded",
    "X-FB-LSD": "AVp4CUdbFLA",
    "Origin": "https://www.facebook.com",
    "Connection": "keep-alive",
    "Referer": "https://www.facebook.com/marketplace/103675689671038",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "TE": "trailers"
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