"""Test configuration and fixtures"""
import pytest
from unittest.mock import MagicMock
from notunsplash import Unsplash
from tests.data.mock_responses import (
    MOCK_PHOTO_RESPONSE,
    MOCK_SEARCH_RESPONSE,
    MOCK_COLLECTION_RESPONSE,
    MOCK_TOPIC_RESPONSE
)

@pytest.fixture
def mock_response():
    """Create a mock response object"""
    response = MagicMock()
    response.status_code = 200
    response.ok = True
    response.json.return_value = MOCK_PHOTO_RESPONSE
    return response

@pytest.fixture
def mock_requests(monkeypatch):
    """Mock requests library"""
    requests = MagicMock()
    session = MagicMock()
    session.headers = MagicMock()
    
    def mock_request(*args, **kwargs):
        method = args[0]
        endpoint = args[1]
        
        # Create base response
        response = MagicMock()
        response.ok = True
        response.status_code = 200
        
        # Handle like/unlike endpoints
        if method in ('POST', 'DELETE') and '/like' in endpoint:
            response.status_code = 403
            response.ok = False
            response.json.return_value = {'errors': ['Authentication required for this endpoint']}
            return response
            
        # Handle search photos endpoint
        if 'search/photos' in endpoint:
            response.status_code = 200
            response.json.return_value = MOCK_SEARCH_RESPONSE
            return response
            
        # Handle error test
        if endpoint == '/photos/nonexistent':
            response.status_code = 404
            response.ok = False
            response.json.return_value = {'errors': ['Resource not found']}
            return response
            
        # Default success response for photo endpoints
        if '/photos/' in endpoint:
            response.json.return_value = MOCK_PHOTO_RESPONSE
            return response
            
        # Default success response
        response.json.return_value = {'success': True}
        return response

    session.request.side_effect = mock_request
    requests.Session.return_value = session
    monkeypatch.setattr('notunsplash.client.requests', requests)
    return requests

@pytest.fixture
def client():
    """Create a test client"""
    return Unsplash(access_key="7jaFq17KqaXvGdtcvi0FZAIgtV0iEjxD9KHkUtaJ--I")
