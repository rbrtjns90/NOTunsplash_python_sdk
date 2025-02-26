"""Tests for the attribution functionality"""
import pytest
from notunsplash.models import Photo
from notunsplash.attribution import Attribution
from tests.data.mock_responses import MOCK_PHOTO_RESPONSE

@pytest.fixture
def photo():
    """Create a test photo instance"""
    return Photo.from_dict(MOCK_PHOTO_RESPONSE)

def test_html_attribution(photo):
    """Test HTML attribution generation"""
    attribution = photo.attribution
    html = attribution.html
    
    assert 'href="https://unsplash.com/@testphotographer"' in html
    assert 'Test Photographer' in html
    assert 'href="https://unsplash.com"' in html
    assert 'Unsplash' in html

def test_markdown_attribution(photo):
    """Test Markdown attribution generation"""
    attribution = photo.attribution
    markdown = attribution.markdown
    
    assert '[Test Photographer](https://unsplash.com/@testphotographer)' in markdown
    assert '[Unsplash](https://unsplash.com)' in markdown

def test_rst_attribution(photo):
    """Test reStructuredText attribution generation"""
    attribution = photo.attribution
    rst = attribution.rst
    
    assert '`Test Photographer <https://unsplash.com/@testphotographer>`_' in rst
    assert '`Unsplash <https://unsplash.com>`_' in rst

def test_text_attribution(photo):
    """Test plain text attribution generation"""
    attribution = photo.attribution
    text = attribution.text
    
    assert 'Test Photographer' in text
    assert 'Unsplash' in text
    assert 'https://unsplash.com' in text

def test_dict_attribution(photo):
    """Test dictionary representation of attribution"""
    attribution = photo.attribution
    data = attribution.to_dict()
    
    assert data["photographer_name"] == "Test Photographer"
    assert data["photographer_url"] == "https://unsplash.com/@testphotographer"
    assert data["photo_url"] == f"https://unsplash.com/photos/{photo.id}"
