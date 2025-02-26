"""Test client functionality"""
import pytest
from notunsplash import Unsplash, UnsplashError, UnsplashAuthError

# Test photo IDs from Unsplash
TEST_PHOTO_ID = "cavaNWU_JMM"
TEST_PHOTO_ID_2 = "ys0rBJK-k6Q"

def test_client_initialization():
    """Test client initialization"""
    client = Unsplash(access_key="test_key")
    assert client.access_key == "test_key"
    assert client.api_base_url == "https://api.unsplash.com"

def test_client_initialization_with_custom_url():
    """Test client initialization with custom URL"""
    client = Unsplash(access_key="test_key", api_base_url="https://custom.api.com")
    assert client.api_base_url == "https://custom.api.com"

def test_client_initialization_without_key():
    """Test client initialization without key"""
    with pytest.raises(UnsplashAuthError, match="Access key is required"):
        Unsplash(access_key="")

def test_search_photos(client):
    """Test photo search functionality"""
    results = client.search_photos("nature", page=1, per_page=1)
    assert len(results) > 0
    assert results[0].id is not None
    assert results[0].urls is not None
    assert results[0].user is not None

def test_get_photo(client):
    """Test getting a single photo"""
    photo = client.get_photo(TEST_PHOTO_ID)
    assert photo.id == TEST_PHOTO_ID
    assert photo.urls is not None
    assert photo.user is not None

def test_like_photo_unauthorized(client):
    """Test liking a photo without auth"""
    with pytest.raises(UnsplashAuthError):
        client.like_photo(TEST_PHOTO_ID)

def test_unlike_photo_unauthorized(client):
    """Test unliking a photo without auth"""
    with pytest.raises(UnsplashAuthError):
        client.unlike_photo(TEST_PHOTO_ID)

def test_download_photo(client):
    """Test tracking a photo download"""
    result = client.download_photo(TEST_PHOTO_ID_2)
    assert result is not None

def test_error_handling(client):
    """Test error handling"""
    with pytest.raises(UnsplashError) as exc_info:
        client.get_photo("nonexistent-photo-id")
    
    assert "404" in str(exc_info.value)
    assert "Asset" in str(exc_info.value)
