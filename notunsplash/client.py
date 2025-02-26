"""Unsplash API client"""
from typing import Dict, List, Optional
import requests
from .models import Photo, Collection, Topic
from .errors import UnsplashError, UnsplashAuthError

class Unsplash:
    """Client for the Unsplash API"""
    
    def __init__(
        self, 
        access_key: str, 
        api_base_url: str = "https://api.unsplash.com",
        oauth_base_url: str = "https://unsplash.com/oauth",
        secret_key: Optional[str] = None
    ):
        """Initialize the client"""
        if not access_key:
            raise UnsplashAuthError("Access key is required")
            
        self.access_key = access_key
        self.secret_key = secret_key
        self.api_base_url = api_base_url
        self.oauth_base_url = oauth_base_url
        
        # Initialize session with default headers
        self.session = requests.Session()
        self.session.headers.update({
            "Accept-Version": "v1",
            "Authorization": f"Client-ID {access_key}"
        })

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
            
        return response.json() if response.content else {}

    def get_oauth_url(
        self,
        redirect_uri: str,
        response_type: str = "code",
        scope: List[str] = None
    ) -> str:
        """Get OAuth authorization URL"""
        if not self.secret_key:
            raise UnsplashAuthError("Secret key is required for OAuth")
            
        scope = scope or ["public"]
        params = {
            "client_id": self.access_key,
            "redirect_uri": redirect_uri,
            "response_type": response_type,
            "scope": "+".join(scope)
        }
        query = "&".join(f"{k}={v}" for k, v in params.items())
        return f"{self.oauth_base_url}/authorize?{query}"

    def get_oauth_token(self, code: str, redirect_uri: str) -> Dict:
        """Exchange authorization code for access token"""
        if not self.secret_key:
            raise UnsplashAuthError("Secret key is required for OAuth token exchange")

        data = {
            "client_id": self.access_key,
            "client_secret": self.secret_key,
            "redirect_uri": redirect_uri,
            "code": code,
            "grant_type": "authorization_code"
        }

        response = self.session.post(
            f"{self.oauth_base_url}/token",
            data=data
        )

        if response.status_code != 200:
            try:
                error_msg = response.json().get('error_description', response.text)
            except (ValueError, AttributeError):
                error_msg = response.text or "Failed to exchange authorization code"
            raise UnsplashAuthError(error_msg)

        return response.json()

    def set_oauth_token(self, access_token: str) -> None:
        """Set OAuth access token for authenticated requests"""
        self.session.headers.update({
            "Authorization": f"Bearer {access_token}"
        })

    def search_photos(self, query: str, page: int = 1, per_page: int = 10) -> List[Photo]:
        """Search for photos"""
        params = {"query": query, "page": page, "per_page": per_page}
        data = self._request("GET", "/search/photos", params=params)
        return [Photo(result) for result in data.get("results", [])]

    def get_photo(self, photo_id: str) -> Photo:
        """Get a single photo"""
        data = self._request("GET", f"/photos/{photo_id}")
        return Photo(data)

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
