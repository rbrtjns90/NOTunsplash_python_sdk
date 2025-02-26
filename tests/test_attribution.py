"""Test attribution functionality"""
import pytest
from notunsplash.models import Photo
from tests.data.mock_responses import MOCK_PHOTO_RESPONSE

@pytest.fixture
def photo():
    """Create a test photo instance"""
    return Photo(MOCK_PHOTO_RESPONSE)

def test_html_attribution(photo):
    """Test HTML attribution format"""
    html = photo.attribution.html
    assert "Photo by" in html
    assert photo.user.name in html
    assert '<a href="https://unsplash.com">' in html
    assert photo.user.html_link in html

def test_markdown_attribution(photo):
    """Test Markdown attribution format"""
    markdown = photo.attribution.markdown
    assert "Photo by" in markdown
    assert photo.user.name in markdown
    assert "[Unsplash](https://unsplash.com)" in markdown
    assert photo.user.html_link in markdown

def test_rst_attribution(photo):
    """Test reStructuredText attribution format"""
    rst = photo.attribution.rst
    assert "Photo by" in rst
    assert photo.user.name in rst
    assert "`Unsplash <https://unsplash.com>`_" in rst
    assert photo.user.html_link in rst

def test_text_attribution(photo):
    """Test plain text attribution format"""
    text = photo.attribution.text
    assert "Photo by" in text
    assert photo.user.name in text
    assert "on Unsplash" in text
    assert photo.user.html_link in text

def test_dict_attribution(photo):
    """Test dictionary attribution format"""
    data = photo.attribution.dict
    assert data["name"] == photo.user.name
    assert data["url"] == photo.user.html_link
