import requests
from typing import Optional, Dict, Any
import time


class HTTPClient:
    def __init__(self, timeout: int = 10, max_retries: int = 3):
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def get(self, url: str, headers: Optional[Dict[str, str]] = None,
            params: Optional[Dict[str, Any]] = None) -> Optional[requests.Response]:
        for attempt in range(self.max_retries):
            try:
                response = self.session.get(
                    url,
                    headers=headers,
                    params=params,
                    timeout=self.timeout
                )
                response.raise_for_status()
                return response
            except requests.exceptions.RequestException as e:
                if attempt == self.max_retries - 1:
                    print(f"Error fetching {url}: {e}")
                    return None
                time.sleep(2 ** attempt)  # Exponential backoff

        return None

    def post(self, url: str, data: Optional[Dict[str, Any]] = None,
             json: Optional[Dict[str, Any]] = None,
             headers: Optional[Dict[str, str]] = None) -> Optional[requests.Response]:
        for attempt in range(self.max_retries):
            try:
                response = self.session.post(
                    url,
                    data=data,
                    json=json,
                    headers=headers,
                    timeout=self.timeout
                )
                response.raise_for_status()
                return response
            except requests.exceptions.RequestException as e:
                if attempt == self.max_retries - 1:
                    print(f"Error posting to {url}: {e}")
                    return None
                time.sleep(2 ** attempt)

        return None

    def close(self):
        self.session.close()
