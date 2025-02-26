"""Mock response data for testing"""

MOCK_PHOTO_RESPONSE = {
    "id": "test123",
    "created_at": "2024-02-25T10:00:00Z",
    "updated_at": "2024-02-25T10:00:00Z",
    "width": 5000,
    "height": 3333,
    "color": "#60544D",
    "blur_hash": "LPF=_[M{tRoft7j[WBfQ~qM{IoWB",
    "downloads": 100,
    "likes": 150,
    "liked_by_user": False,
    "description": "A beautiful mountain landscape",
    "urls": {
        "raw": "https://images.unsplash.com/photo-123?ixid=123",
        "full": "https://images.unsplash.com/photo-123?ixid=123&w=1080",
        "regular": "https://images.unsplash.com/photo-123?ixid=123&w=1080&q=80",
        "small": "https://images.unsplash.com/photo-123?ixid=123&w=400&q=80",
        "thumb": "https://images.unsplash.com/photo-123?ixid=123&w=200&q=80"
    },
    "user": {
        "id": "user123",
        "username": "testphotographer",
        "name": "Test Photographer",
        "portfolio_url": "https://example.com",
        "bio": "Nature photographer",
        "location": "Mountain View, CA",
        "total_collections": 5,
        "total_likes": 100,
        "total_photos": 50,
        "links": {
            "self": "https://api.unsplash.com/users/testphotographer",
            "html": "https://unsplash.com/@testphotographer",
            "photos": "https://api.unsplash.com/users/testphotographer/photos",
            "likes": "https://api.unsplash.com/users/testphotographer/likes",
            "portfolio": "https://api.unsplash.com/users/testphotographer/portfolio"
        }
    }
}

MOCK_SEARCH_RESPONSE = {
    "total": 1,
    "total_pages": 1,
    "results": [MOCK_PHOTO_RESPONSE]
}

MOCK_COLLECTION_RESPONSE = {
    "id": "collection123",
    "title": "Test Collection",
    "description": "A collection of test photos",
    "published_at": "2024-02-25T10:00:00Z",
    "total_photos": 1,
    "private": False,
    "cover_photo": MOCK_PHOTO_RESPONSE,
    "user": MOCK_PHOTO_RESPONSE["user"]
}

MOCK_TOPIC_RESPONSE = {
    "id": "topic123",
    "slug": "test-topic",
    "title": "Test Topic",
    "description": "A test topic",
    "published_at": "2024-02-25T10:00:00Z",
    "updated_at": "2024-02-25T10:00:00Z",
    "total_photos": 100,
    "links": {
        "self": "https://api.unsplash.com/topics/test-topic",
        "html": "https://unsplash.com/t/test-topic",
        "photos": "https://api.unsplash.com/topics/test-topic/photos"
    },
    "status": "open",
    "owners": [MOCK_PHOTO_RESPONSE["user"]],
    "cover_photo": MOCK_PHOTO_RESPONSE
}
