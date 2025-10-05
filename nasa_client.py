import requests
from typing import Dict, List, Optional
class NASAClient:
    def __init__(self, api_key: str):  # Corrected from _init_ to __init__
        self.api_key = api_key
        self.base_apod = "https://api.nasa.gov/planetary/apod"
        self.base_search = "https://images-api.nasa.gov/search"

    def _get(self, url: str, params: dict = {}) -> dict:
        params["api_key"] = self.api_key
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    def get_apod(self, date: Optional[str] = None, hd: bool = True) -> Dict:
        params = {"hd": hd}
        if date:
            params["date"] = date
        return self._get(self.base_apod, params)

    def search_images(self, query: str, media_type: Optional[List[str]] = None, page: int = 1) -> Dict:
        if media_type is None:
            media_type = []  # Default to empty list if no media_type is provided
        params = {"q": query, "page": page}
        if media_type:
            params["media_type"] = ",".join(media_type)
        return requests.get(self.base_search, params=params, timeout=10).json()
