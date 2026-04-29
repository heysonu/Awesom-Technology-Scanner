import json
import os
from datetime import datetime, timedelta
from typing import Any, Optional
import hashlib


class Cache:
    def __init__(self, cache_dir: str = '.cache', ttl_hours: int = 24):
        self.cache_dir = cache_dir
        self.ttl = timedelta(hours=ttl_hours)
        os.makedirs(cache_dir, exist_ok=True)

    def _get_cache_path(self, key: str) -> str:
        key_hash = hashlib.md5(key.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{key_hash}.json")

    def get(self, key: str) -> Optional[Any]:
        cache_path = self._get_cache_path(key)

        if not os.path.exists(cache_path):
            return None

        try:
            with open(cache_path, 'r') as f:
                data = json.load(f)

            # Check if cache is expired
            cached_time = datetime.fromisoformat(data.get('timestamp', ''))
            if datetime.now() - cached_time > self.ttl:
                os.remove(cache_path)
                return None

            return data.get('value')
        except Exception as e:
            print(f"Error reading cache: {e}")
            return None

    def set(self, key: str, value: Any) -> None:
        cache_path = self._get_cache_path(key)

        try:
            data = {
                'timestamp': datetime.now().isoformat(),
                'value': value
            }

            with open(cache_path, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Error writing cache: {e}")

    def clear(self) -> None:
        try:
            for filename in os.listdir(self.cache_dir):
                file_path = os.path.join(self.cache_dir, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        except Exception as e:
            print(f"Error clearing cache: {e}")

    def cleanup_expired(self) -> None:
        try:
            for filename in os.listdir(self.cache_dir):
                file_path = os.path.join(self.cache_dir, filename)
                if os.path.isfile(file_path):
                    try:
                        with open(file_path, 'r') as f:
                            data = json.load(f)

                        cached_time = datetime.fromisoformat(data.get('timestamp', ''))
                        if datetime.now() - cached_time > self.ttl:
                            os.remove(file_path)
                    except:
                        # Remove corrupted cache files
                        os.remove(file_path)
        except Exception as e:
            print(f"Error cleaning up cache: {e}")
