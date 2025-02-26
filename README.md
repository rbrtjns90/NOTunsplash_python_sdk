# NOTunsplash Python SDK

A Python SDK for interacting with the Unsplash API, providing a clean and type-safe interface with comprehensive error handling and proper attribution support.

## Features

- Complete Unsplash API integration
- OAuth 2.0 authentication flow
- Built-in attribution handling (HTML, Markdown, reStructuredText, Plain text)
- Type hints for better IDE support
- Comprehensive error handling
- Easy-to-use data models

## Installation

```bash
pip install notunsplash
```

## Requirements

- Python 3.8 or higher
- requests>=2.31.0
- python-dateutil>=2.8.2
- urllib3>=2.0.7

## Quick Start

Basic usage of the SDK to search for photos:

```python
from notunsplash import Unsplash

# Initialize with your access key
client = Unsplash(access_key="your_access_key")

# Search for photos
photos = client.search_photos(
    query="nature",    # Query is a required parameter
    page=1,           # Optional: default is 1
    per_page=10       # Optional: default is 10
)

for photo in photos:
    print(f"Photo by {photo.user.name}")
    print(f"Description: {photo.description or 'No description'}")
    print(f"URLs available: {photo.urls}")  # Dictionary of URLs
    print(f"Regular size URL: {photo.urls['regular']}")
    print(f"Attribution: {photo.attribution.html}")
```

For a complete working example, see [examples/quickstart.py](examples/quickstart.py).

## OAuth Authentication

Example of implementing OAuth authentication flow:

```python
from notunsplash import Unsplash
from notunsplash.errors import UnsplashAuthError

try:
    # Initialize with OAuth credentials
    client = Unsplash(
        access_key="your_access_key",
        secret_key="your_secret_key"  # Required for OAuth
    )
    
    # Generate authorization URL
    auth_url = client.get_oauth_url(
        redirect_uri="your_redirect_uri",
        scope=["public", "write_likes"]  # Optional: defaults to ["public"]
    )
    print(f"Visit this URL to authorize: {auth_url}")
    
    # After user authorization, exchange code for token
    token = client.get_oauth_token(
        code="authorization_code",
        redirect_uri="your_redirect_uri"  # Must match the original redirect_uri
    )
    
    # Set token for authenticated requests
    client.set_oauth_token(token["access_token"])
    
    # Now you can use authenticated endpoints
    client.like_photo("photo_id")
    
except UnsplashAuthError as e:
    print(f"Authentication error: {e}")
```

For a complete working example with interactive OAuth flow, see [examples/oauth_example.py](examples/oauth_example.py).

## Real World Examples

### Creating a Blog Header

Create a responsive blog header with proper attribution:

```python
def create_blog_header(topic: str) -> str:
    client = Unsplash(access_key="your_access_key")
    
    # Search for a photo
    photos = client.search_photos(
        query=topic,
        per_page=1
    )
    
    if not photos:
        return "<p>No suitable images found.</p>"
    
    photo = photos[0]
    
    return f"""
        <header class="blog-header">
            <img src="{photo.urls['regular']}" 
                 alt="{photo.description or photo.alt_description or 'Blog header image'}">
            <div class="attribution">
                {photo.attribution.html}
            </div>
        </header>
    """
```

For a complete working example with responsive styling, see [examples/blog_header.py](examples/blog_header.py).

### Creating a Social Media Gallery

Create a responsive image gallery for social media:

```python
def create_social_gallery(theme: str, num_images: int = 6) -> str:
    client = Unsplash(access_key="your_access_key")
    
    # Search for photos
    photos = client.search_photos(
        query=theme,
        per_page=num_images
    )
    
    # Generate HTML gallery
    html = '<div class="gallery">'
    for photo in photos:
        html += f"""
            <div class="image-card">
                <img src="{photo.urls['regular']}" 
                     alt="{photo.description or photo.alt_description or 'Gallery image'}">
                <div class="attribution">
                    {photo.attribution.html}
                </div>
            </div>
        """
    html += "</div>"
    return html
```

For a complete working example with responsive grid layout, see [examples/social_gallery.py](examples/social_gallery.py).

## Attribution

Unsplash requires proper attribution for all photos. This SDK makes it easy with multiple attribution formats:

```python
# Get a photo
photo = client.get_photo("photo-id")

# HTML attribution
print(photo.attribution.html)
# Output: Photo by <a href="https://unsplash.com/@photographer">Photographer Name</a> on <a href="https://unsplash.com">Unsplash</a>

# Markdown attribution
print(photo.attribution.markdown)
# Output: Photo by [Photographer Name](https://unsplash.com/@photographer) on [Unsplash](https://unsplash.com)

# reStructuredText attribution
print(photo.attribution.rst)
# Output: Photo by `Photographer Name <https://unsplash.com/@photographer>`_ on `Unsplash <https://unsplash.com>`_

# Plain text attribution
print(photo.attribution.text)
# Output: Photo by Photographer Name (https://unsplash.com/@photographer) on Unsplash (https://unsplash.com)
```

## Available Models

The SDK provides rich models for all Unsplash entities:

- `Photo`: Complete photo metadata including URLs and attribution
- `User`: User profile data and statistics
- `Collection`: Photo collection metadata
- `Topic`: Editorial topic information

## Error Handling

The SDK provides two types of exceptions for error handling:

```python
from notunsplash import Unsplash
from notunsplash.errors import UnsplashError, UnsplashAuthError

client = Unsplash(access_key="your_access_key")

try:
    # Example of general error handling
    photo = client.get_photo("invalid-id")
except UnsplashAuthError as e:
    print(f"Authentication error: {e}")  # Handles authentication-specific errors
except UnsplashError as e:
    print(f"API error: {e}")  # Handles all other API errors

# Example of OAuth-specific error handling
try:
    client.like_photo("photo-id")
except UnsplashAuthError as e:
    print(f"Authentication required: {e}")
except UnsplashError as e:
    print(f"API error: {e}")
```

The SDK uses two main exception types:
- `UnsplashAuthError`: Raised for authentication-related errors (invalid API key, missing OAuth token, etc.)
- `UnsplashError`: Base exception class for all other API errors (rate limits, invalid requests, server errors, etc.)

## Development

To set up the development environment:

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Robert Jones

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
