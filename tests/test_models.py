"""Tests for the data models"""
import pytest
from datetime import datetime
from notunsplash.models import Photo, User, Collection, Topic
from tests.data.mock_responses import (
    MOCK_PHOTO_RESPONSE,
    MOCK_COLLECTION_RESPONSE,
    MOCK_TOPIC_RESPONSE
)

def test_user_model():
    """Test User model creation and properties"""
    user_data = MOCK_PHOTO_RESPONSE["user"]
    user = User(user_data)
    
    assert user.id == user_data["id"]
    assert user.username == user_data["username"]
    assert user.name == user_data["name"]
    assert user.portfolio_url == user_data.get("portfolio_url")
    assert user.bio == user_data.get("bio")
    assert user.location == user_data.get("location")
    assert user.total_collections == user_data["total_collections"]
    assert user.total_likes == user_data["total_likes"]
    assert user.total_photos == user_data["total_photos"]
    assert user.html_link == user_data["links"]["html"]

def test_photo_model():
    """Test Photo model creation and properties"""
    photo = Photo(MOCK_PHOTO_RESPONSE)
    
    assert photo.id == MOCK_PHOTO_RESPONSE["id"]
    assert isinstance(photo.created_at, datetime)
    assert isinstance(photo.updated_at, datetime)
    assert photo.width == MOCK_PHOTO_RESPONSE["width"]
    assert photo.height == MOCK_PHOTO_RESPONSE["height"]
    assert photo.color == MOCK_PHOTO_RESPONSE["color"]
    assert photo.blur_hash == MOCK_PHOTO_RESPONSE["blur_hash"]
    assert photo.downloads == MOCK_PHOTO_RESPONSE["downloads"]
    assert photo.likes == MOCK_PHOTO_RESPONSE["likes"]
    assert photo.liked_by_user == MOCK_PHOTO_RESPONSE["liked_by_user"]
    assert photo.description == MOCK_PHOTO_RESPONSE.get("description")
    
    # Test URLs
    assert photo.urls["raw"] == MOCK_PHOTO_RESPONSE["urls"]["raw"]
    assert photo.urls["full"] == MOCK_PHOTO_RESPONSE["urls"]["full"]
    assert photo.urls["regular"] == MOCK_PHOTO_RESPONSE["urls"]["regular"]
    assert photo.urls["small"] == MOCK_PHOTO_RESPONSE["urls"]["small"]
    assert photo.urls["thumb"] == MOCK_PHOTO_RESPONSE["urls"]["thumb"]
    
    # Test user relationship
    assert photo.user is not None
    assert photo.user.id == MOCK_PHOTO_RESPONSE["user"]["id"]

def test_collection_model():
    """Test Collection model creation and properties"""
    collection = Collection(MOCK_COLLECTION_RESPONSE)
    
    assert collection.id == MOCK_COLLECTION_RESPONSE["id"]
    assert collection.title == MOCK_COLLECTION_RESPONSE["title"]
    assert collection.description == MOCK_COLLECTION_RESPONSE.get("description")
    assert isinstance(collection.published_at, datetime)
    assert collection.total_photos == MOCK_COLLECTION_RESPONSE["total_photos"]
    assert collection.private == MOCK_COLLECTION_RESPONSE["private"]
    
    # Test relationships
    assert collection.cover_photo is not None
    assert collection.cover_photo.id == MOCK_COLLECTION_RESPONSE["cover_photo"]["id"]
    assert collection.user is not None
    assert collection.user.id == MOCK_COLLECTION_RESPONSE["user"]["id"]

def test_topic_model():
    """Test Topic model creation and properties"""
    topic = Topic(MOCK_TOPIC_RESPONSE)
    
    assert topic.id == MOCK_TOPIC_RESPONSE["id"]
    assert topic.slug == MOCK_TOPIC_RESPONSE["slug"]
    assert topic.title == MOCK_TOPIC_RESPONSE["title"]
    assert topic.description == MOCK_TOPIC_RESPONSE.get("description")
    assert isinstance(topic.published_at, datetime)
    assert isinstance(topic.updated_at, datetime)
    assert topic.total_photos == MOCK_TOPIC_RESPONSE["total_photos"]
    assert topic.status == MOCK_TOPIC_RESPONSE["status"]
    
    # Test relationships
    assert topic.cover_photo is not None
    assert topic.cover_photo.id == MOCK_TOPIC_RESPONSE["cover_photo"]["id"]
    assert len(topic.owners) == len(MOCK_TOPIC_RESPONSE["owners"])
    assert topic.owners[0].username == MOCK_TOPIC_RESPONSE["owners"][0]["username"]
