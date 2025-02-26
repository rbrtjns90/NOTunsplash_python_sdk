# NOTunsplash Python SDK

A Python SDK for interacting with the Unsplash API, providing a clean and type-safe interface with comprehensive error handling and proper attribution support.

## Features

- Complete Unsplash API integration
- OAuth 2.0 authentication flow
- Built-in attribution handling (HTML, Markdown, reStructuredText, Plain text)
- Type hints for better IDE support
- Comprehensive error handling
- Easy-to-use data models
- Extensive test coverage

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

## Photo URLs and Hotlinking

Unlike most APIs, Unsplash **requires** that you use the image URLs returned by the API directly in your applications (hotlinking). This is intentional and helps Unsplash:
- Track photo views accurately
- Provide valuable statistics to photographers
- Monitor how photos are being used
- Ensure photographers get proper exposure for their work

### Available URL Formats

When you get a photo from the API, it comes with several URL options:

```python
from notunsplash import Unsplash

client = Unsplash(access_key="your_access_key")
photos = client.search_photos(query="nature", per_page=1)

if photos:
    photo = photos[0]
    urls = photo.urls  # Dictionary of available URLs
    
    # Available formats:
    raw = urls["raw"]      # Raw photo file
    full = urls["full"]    # Full resolution
    regular = urls["regular"]  # 1080px width
    small = urls["small"]   # 400px width
    thumb = urls["thumb"]   # 200px width
```

### Best Practices

1. **Direct Usage**: Always use the URLs directly from the API response. Do not:
   - Download and re-host the images
   - Modify the URLs (except for URL parameters)
   - Cache the images on your own servers

2. **Choose the Right Size**:
   ```python
   # For blog headers or hero images
   photo.urls["regular"]  # 1080px width
   
   # For thumbnails or previews
   photo.urls["small"]    # 400px width
   
   # For very small previews
   photo.urls["thumb"]    # 200px width
   ```

3. **Track Downloads**: If a user downloads the full-resolution image, notify Unsplash:
   ```python
   client.download_photo(photo.id)  # Tracks the download event
   ```

### Example: Responsive Images

Here's how to use different sizes responsively in HTML:

```html
<picture>
    <source media="(min-width: 1080px)" srcset="${photo.urls['regular']}">
    <source media="(min-width: 400px)" srcset="${photo.urls['small']}">
    <img src="${photo.urls['thumb']}" 
         alt="${photo.description or photo.alt_description or 'Photo'}"
         loading="lazy">
</picture>
```

Remember: Always pair photo URLs with proper attribution as shown in the Attribution section.

## Photo Usage and Download Tracking

Unsplash requires tracking photo usage to provide accurate statistics to photographers. This motivates contributors to share more photos and helps build a better library for everyone.

### When to Track Downloads

You must track a download whenever a user performs an action similar to downloading, such as:
- Setting an image as a header/background
- Inserting an image into a blog post
- Using the image in a presentation
- Any action where the photo is being used

### How to Track Downloads

```python
from notunsplash import Unsplash
from notunsplash.errors import UnsplashError

client = Unsplash(access_key="your_access_key")

# Example: User chooses a photo for their blog
photos = client.search_photos(query="nature", per_page=1)
if photos:
    photo = photos[0]
    
    # 1. Use the photo URL in your application
    image_url = photo.urls["regular"]
    
    # 2. Track the usage asynchronously
    try:
        client.download_photo(photo.id)  # This uses the correct download_location endpoint
    except UnsplashError as e:
        # Log the error but don't fail the whole request
        print(f"Failed to track photo usage: {e}")
```

### Best Practices

1. **Track Asynchronously**: Always track downloads asynchronously to avoid slowing down your application
   ```python
   # In your async function
   try:
       client.download_photo(photo.id)
   except Exception as e:
       # Log but don't block the main flow
       print(f"Download tracking failed: {e}")
   ```

2. **Handle Errors Gracefully**: Don't let tracking failures affect your main application flow
   ```python
   def use_photo(photo_id: str) -> None:
       try:
           # Main functionality
           photo = client.get_photo(photo_id)
           display_image(photo.urls["regular"])
           
           # Track usage separately
           try:
               client.download_photo(photo_id)
           except Exception as e:
               log_error(f"Failed to track photo usage: {e}")
       except Exception as e:
           # Handle main functionality errors
           raise
   ```

3. **Track All Usage**: Remember to track whenever a photo is used, not just when it's downloaded
   ```python
   class BlogPost:
       def add_header_image(self, photo_id: str) -> None:
           photo = client.get_photo(photo_id)
           self.header_url = photo.urls["regular"]
           
           # Track usage since we're using the photo
           try:
               client.download_photo(photo_id)
           except Exception as e:
               log_error(f"Usage tracking failed: {e}")
   ```

Note: The download tracking endpoint is purely for event tracking, similar to pageview events in analytics. Use `photo.urls` for embedding images, not the download endpoint.

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
