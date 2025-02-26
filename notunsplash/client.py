"""
Unsplash API client
"""
from typing import Dict, List, Optional
import requests
from .models import Photo, Collection, Topic
from .errors import UnsplashError, UnsplashAuthError

class Unsplash:
    """Client for the Unsplash API"""
    
    def __init__(self, access_key: str, api_base_url: str = "https://api.unsplash.com"):
        """Initialize the client with an access key"""
        if not access_key:
            raise UnsplashAuthError("Access key is required")
        self.access_key = access_key
        self.api_base_url = api_base_url
        self.session = requests.Session()
        self.session.headers.update(self._auth_headers())
    
    def _auth_headers(self) -> Dict[str, str]:
        """Get authentication headers"""
        return {
            "Authorization": f"Client-ID {self.access_key}",
            "Accept-Version": "v1"
        }
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """Make a request to the Unsplash API"""
        url = f"{self.api_base_url}/{endpoint.lstrip('/')}"
        
        # Headers are already set in the session
        response = self.session.request(method, url, **kwargs)
        
        if response.status_code == 401:
            raise UnsplashAuthError("OAuth error: The access token is invalid")
        elif response.status_code == 403:
            raise UnsplashAuthError("Authentication required for this endpoint")
        elif not response.ok:
            error_msg = response.json().get('errors', [response.text])[0]
            raise UnsplashError(f"API request failed: {response.status_code} - {error_msg}")
        
        return response.json()
    
    def search_photos(self, query: str, page: int = 1, per_page: int = 10,
                     orientation: Optional[str] = None) -> List[Photo]:
        """Search for photos"""
        params = {
            "query": query,
            "page": page,
            "per_page": per_page
        }
        if orientation:
            params["orientation"] = orientation
            
        data = self._request("GET", "/search/photos", params=params)
        return [Photo.from_dict(item) for item in data["results"]]
    
    def get_photo(self, photo_id: str) -> Photo:
        """Get a single photo"""
        data = self._request("GET", f"/photos/{photo_id}")
        return Photo.from_dict(data)
    
    def like_photo(self, photo_id: str) -> None:
        """Like a photo (requires authentication)"""
        try:
            self._request("POST", f"/photos/{photo_id}/like")
        except UnsplashError as e:
            if "OAuth" in str(e):
                raise UnsplashAuthError("Authentication required to like photos")
            raise
    
    def unlike_photo(self, photo_id: str) -> None:
        """Unlike a photo (requires authentication)"""
        try:
            self._request("DELETE", f"/photos/{photo_id}/like")
        except UnsplashError as e:
            if "OAuth" in str(e):
                raise UnsplashAuthError("Authentication required to unlike photos")
            raise
    
    def download_photo(self, photo_id: str) -> Dict:
        """Track a photo download"""
        return self._request("GET", f"/photos/{photo_id}/download")
