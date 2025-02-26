"""Tests for example scripts"""
import pytest
from unittest.mock import Mock, patch
from examples.blog_post_generator import generate_blog_post
from examples.real_estate_images import create_real_estate_gallery
from examples.social_media_gallery import create_social_gallery
from notunsplash import Unsplash
from tests.data.mock_responses import MOCK_PHOTO_RESPONSE

@pytest.fixture
def mock_client():
    """Create a mock Unsplash client"""
    client = Mock(spec=Unsplash)
    photo = Mock()
    photo.id = MOCK_PHOTO_RESPONSE["id"]
    photo.description = MOCK_PHOTO_RESPONSE["description"]
    photo.urls = MOCK_PHOTO_RESPONSE["urls"]
    photo.user = Mock()
    photo.user.name = MOCK_PHOTO_RESPONSE["user"]["name"]
    photo.user.html_link = f"https://unsplash.com/@{MOCK_PHOTO_RESPONSE['user']['username']}"
    photo.attribution = Mock()
    photo.attribution.html = f'Photo by <a href="{photo.user.html_link}">{photo.user.name}</a> on <a href="https://unsplash.com">Unsplash</a>'
    photo.attribution.markdown = f'Photo by [{photo.user.name}]({photo.user.html_link}) on [Unsplash](https://unsplash.com)'
    client.search_photos.return_value = [photo] * 3
    return client

def test_blog_post_generator(mock_client):
    """Test blog post generator"""
    with patch("examples.blog_post_generator.Unsplash", return_value=mock_client):
        post = generate_blog_post("nature", num_images=2)
        assert "# Nature - A Photo Journey" in post
        assert "![" in post
        assert "Test Photographer" in post
        assert "https://unsplash.com" in post
        assert mock_client.search_photos.call_count == 1
        mock_client.search_photos.assert_called_with("nature", per_page=2)

def test_real_estate_gallery(mock_client):
    """Test real estate gallery generator"""
    with patch("examples.real_estate_images.Unsplash", return_value=mock_client):
        html = create_real_estate_gallery("modern", num_images=2)
        assert '<div class="gallery">' in html
        assert '<div class="image-card">' in html
        assert '<img src="' in html
        assert 'Test Photographer' in html
        assert 'https://unsplash.com' in html
        assert mock_client.search_photos.call_count == 1
        mock_client.search_photos.assert_called_with(
            "real estate modern",
            per_page=2,
            orientation="landscape"
        )

def test_social_media_gallery(mock_client):
    """Test social media gallery generator"""
    with patch("examples.social_media_gallery.Unsplash", return_value=mock_client):
        html = create_social_gallery("food", num_images=2)
        assert '<div class="gallery">' in html
        assert '<div class="image-card">' in html
        assert '<img src="' in html
        assert 'Test Photographer' in html
        assert 'https://unsplash.com' in html
        assert 'grid-template-columns' in html
        assert mock_client.search_photos.call_count == 1
        mock_client.search_photos.assert_called_with("food", per_page=2)

def test_blog_post_generator_error_handling(mock_client):
    """Test blog post generator error handling"""
    mock_client.search_photos.side_effect = Exception("API Error")
    with patch("examples.blog_post_generator.Unsplash", return_value=mock_client):
        with pytest.raises(Exception) as exc:
            generate_blog_post("nature")
        assert str(exc.value) == "API Error"

def test_real_estate_gallery_error_handling(mock_client):
    """Test real estate gallery error handling"""
    mock_client.search_photos.side_effect = Exception("API Error")
    with patch("examples.real_estate_images.Unsplash", return_value=mock_client):
        with pytest.raises(Exception) as exc:
            create_real_estate_gallery("modern")
        assert str(exc.value) == "API Error"

def test_social_media_gallery_error_handling(mock_client):
    """Test social media gallery error handling"""
    mock_client.search_photos.side_effect = Exception("API Error")
    with patch("examples.social_media_gallery.Unsplash", return_value=mock_client):
        with pytest.raises(Exception) as exc:
            create_social_gallery("food")
        assert str(exc.value) == "API Error"

def test_blog_post_generator_no_results(mock_client):
    """Test blog post generator with no results"""
    mock_client.search_photos.return_value = []
    with patch("examples.blog_post_generator.Unsplash", return_value=mock_client):
        post = generate_blog_post("nonexistent")
        assert "# Nonexistent - A Photo Journey" in post
        assert len(post.split("\n")) == 2  # Only title and newline

def test_real_estate_gallery_no_results(mock_client):
    """Test real estate gallery with no results"""
    mock_client.search_photos.return_value = []
    with patch("examples.real_estate_images.Unsplash", return_value=mock_client):
        html = create_real_estate_gallery("nonexistent")
        assert '<div class="gallery">' in html
        assert '<div class="image-card">' not in html

def test_social_media_gallery_no_results(mock_client):
    """Test social media gallery with no results"""
    mock_client.search_photos.return_value = []
    with patch("examples.social_media_gallery.Unsplash", return_value=mock_client):
        html = create_social_gallery("nonexistent")
        assert '<div class="gallery">' in html
        assert '<div class="image-card">' not in html
