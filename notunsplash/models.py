"""
Data models for the Unsplash API
"""
from typing import Dict, Optional, List
from datetime import datetime
from dateutil.parser import parse as parse_date
from .attribution import Attribution

class User:
    """Unsplash user model"""
    def __init__(self, data: Dict):
        self.id = data.get("id")
        self.username = data.get("username")
        self.name = data.get("name")
        self.portfolio_url = data.get("portfolio_url")
        self.bio = data.get("bio")
        self.location = data.get("location")
        self.total_collections = data.get("total_collections", 0)
        self.total_likes = data.get("total_likes", 0)
        self.total_photos = data.get("total_photos", 0)
        self.html_link = f"https://unsplash.com/@{self.username}"
        
        # Links
        links = data.get("links", {})
        self.html_link = links.get("html")
        self.photos_link = links.get("photos")
        self.likes_link = links.get("likes")
        self.portfolio_link = links.get("portfolio")
        
        # Profile image URLs
        profile_image = data.get("profile_image", {})
        self.profile_small = profile_image.get("small")
        self.profile_medium = profile_image.get("medium")
        self.profile_large = profile_image.get("large")

class Photo:
    """Unsplash photo model"""
    def __init__(self, data: Dict):
        # Basic metadata
        self.id = data.get("id")
        self.created_at = parse_date(data.get("created_at")) if data.get("created_at") else None
        self.updated_at = parse_date(data.get("updated_at")) if data.get("updated_at") else None
        self.width = data.get("width")
        self.height = data.get("height")
        self.color = data.get("color")
        self.blur_hash = data.get("blur_hash")
        self.downloads = data.get("downloads", 0)
        self.likes = data.get("likes", 0)
        self.liked_by_user = data.get("liked_by_user", False)
        self.description = data.get("description")
        self.alt_description = data.get("alt_description")
        
        # URLs
        urls = data.get("urls", {})
        self.urls = {
            "raw": urls.get("raw"),
            "full": urls.get("full"),
            "regular": urls.get("regular"),
            "small": urls.get("small"),
            "thumb": urls.get("thumb")
        }
        
        # Links
        links = data.get("links", {})
        self.html_link = links.get("html")
        self.download_link = links.get("download")
        
        # User info
        user_data = data.get("user", {})
        self.user = User(user_data) if user_data else None
        
        # Location info
        location = data.get("location", {})
        self.location = {
            "name": location.get("name"),
            "city": location.get("city"),
            "country": location.get("country"),
            "position": location.get("position", {})
        }
        
        # Exif data
        exif = data.get("exif", {})
        self.exif = {
            "make": exif.get("make"),
            "model": exif.get("model"),
            "exposure_time": exif.get("exposure_time"),
            "aperture": exif.get("aperture"),
            "focal_length": exif.get("focal_length"),
            "iso": exif.get("iso")
        }
        self._raw = data
        self.attribution = Attribution(self)

class Collection:
    """Unsplash collection model"""
    def __init__(self, data: Dict):
        self.id = data.get("id")
        self.title = data.get("title")
        self.description = data.get("description")
        self.published_at = parse_date(data.get("published_at")) if data.get("published_at") else None
        self.updated_at = parse_date(data.get("updated_at")) if data.get("updated_at") else None
        self.curated = data.get("curated", False)
        self.featured = data.get("featured", False)
        self.total_photos = data.get("total_photos", 0)
        self.private = data.get("private", False)
        self.share_key = data.get("share_key")
        
        # Links
        links = data.get("links", {})
        self.html_link = links.get("html")
        self.photos_link = links.get("photos")
        self.related_link = links.get("related")
        
        # Cover photo
        cover_photo = data.get("cover_photo", {})
        self.cover_photo = Photo(cover_photo) if cover_photo else None
        
        # User info
        user_data = data.get("user", {})
        self.user = User(user_data) if user_data else None

class Topic:
    """Unsplash topic model"""
    def __init__(self, data: Dict):
        self.id = data.get("id")
        self.slug = data.get("slug")
        self.title = data.get("title")
        self.description = data.get("description")
        self.published_at = parse_date(data.get("published_at")) if data.get("published_at") else None
        self.updated_at = parse_date(data.get("updated_at")) if data.get("updated_at") else None
        self.featured = data.get("featured", False)
        self.total_photos = data.get("total_photos", 0)
        self.status = data.get("status", "unknown")
        self.owners = [User(owner) for owner in data.get("owners", [])]
        self.cover_photo = Photo(data.get("cover_photo")) if data.get("cover_photo") else None
        self._raw = data
        
        # Links
        links = data.get("links", {})
        self.html_link = links.get("html")
        self.photos_link = links.get("photos")
        
        # Preview photos
        preview_photos = data.get("preview_photos", [])
        self.preview_photos = [Photo(photo) for photo in preview_photos] if preview_photos else []
