# NotUnsplash Python SDK

A Python wrapper for the [Unsplash API](https://unsplash.com/documentation) that makes it easy to interact with Unsplash's services programmatically.

## Features

- Simple and intuitive interface for the Unsplash API
- First-class attribution support with multiple formats (HTML, Markdown, RST, Text)
- Type hints for better IDE integration
- Comprehensive error handling
- Proper rate limit handling
- Clean and modern object-oriented design

## Installation

```bash
pip install notunsplash
```

Or install from source:

```bash
git clone https://github.com/yourusername/notunsplash-python-sdk.git
cd notunsplash-python-sdk
pip install -e .
```

## Quick Start

### Basic Usage

```python
from notunsplash import Unsplash

# Initialize with your access key
client = Unsplash(access_key="your_access_key")

# Search for photos
photos = client.search_photos("nature", page=1, per_page=10)
for photo in photos:
    print(f"Photo ID: {photo.id}")
    print(f"Description: {photo.description}")
    print(f"Regular URL: {photo.urls.regular}")
    print(f"Attribution: {photo.attribution.get_text()}")
    print("---")

# Get a single photo
photo = client.get_photo("photo_id")
print(f"Photo by {photo.user.name}")

# Like/Unlike photos (requires authentication)
try:
    client.like_photo("photo_id")
    client.unlike_photo("photo_id")
except UnsplashAuthError as e:
    print("Authentication required:", e)
```

## Error Handling

The SDK provides specific error types for better error handling:

```python
from notunsplash import Unsplash, UnsplashError, UnsplashAuthError

client = Unsplash(access_key="your_access_key")

try:
    # Try to like a photo without authentication
    client.like_photo("photo_id")
except UnsplashAuthError as e:
    print("Authentication error:", e)
except UnsplashError as e:
    print("General API error:", e)
```

## Attribution

Unsplash requires proper attribution for all photos. The SDK makes it easy to generate correct attribution in multiple formats:

```python
from notunsplash import Unsplash

# Initialize client and get a photo
client = Unsplash(access_key="your_access_key")
photo = client.get_photo("photo_id")

# Get attribution in different formats
print(photo.attribution.get_html())  # HTML format
print(photo.attribution.get_markdown())  # Markdown format
print(photo.attribution.get_rst())  # reStructuredText format
print(photo.attribution.get_text())  # Plain text format

# Get complete metadata
metadata = photo.attribution.metadata
print(metadata)
```

### Customizing HTML Attribution

You can customize the CSS class used in HTML attribution:

```python
# Custom CSS class
html_attribution = photo.attribution.get_html(css_class="my-custom-attribution")

# No CSS class
html_attribution = photo.attribution.get_html(css_class=None)
```

## Example Programs

The SDK comes with several example programs demonstrating different use cases:

### Blog Post Generator

Create a markdown blog post with Unsplash images and proper attribution:

```python
from notunsplash import Unsplash
from datetime import datetime

def generate_blog_post(topic: str, num_images: int = 3):
    client = Unsplash(access_key="your_access_key")
    
    # Search for photos
    photos = client.search_photos(topic, per_page=num_images)
    
    # Generate markdown blog post
    post = f"# {topic.title()} - A Photo Journey\n\n"
    
    for photo in photos:
        # Add photo with markdown attribution
        description = photo.description or "Unsplash photo"
        post += f"![{description}]({photo.urls.regular})\n\n"
        post += f"_{photo.attribution.get_markdown()}_\n\n"
    
    return post
```

### Real Estate Gallery

Create an HTML gallery of real estate photos with proper attribution:

```python
from notunsplash import Unsplash

def create_real_estate_gallery(category: str, num_images: int = 5):
    client = Unsplash(access_key="your_access_key")
    
    # Search for photos
    photos = client.search_photos(
        f"real estate {category}",
        per_page=num_images,
        orientation="landscape"
    )
    
    # Generate HTML gallery
    html = "<div class='gallery'>"
    for photo in photos:
        html += f"""
            <div class="image-card">
                <img src="{photo.urls.regular}" 
                     alt="{photo.description or 'Real estate photo'}">
                {photo.attribution.get_html(css_class="photo-credit")}
            </div>
        """
    html += "</div>"
    
    return html
```

### Social Media Gallery

Create a responsive image gallery for social media:

```python
from notunsplash import Unsplash

def create_social_gallery(theme: str, num_images: int = 6):
    client = Unsplash(access_key="your_access_key")
    
    # Search for photos
    photos = client.search_photos(theme, per_page=num_images)
    
    # Generate HTML gallery with CSS Grid
    html = """
    <style>
        .gallery {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }
        .image-card img {
            width: 100%;
            height: 300px;
            object-fit: cover;
        }
    </style>
    <div class="gallery">
    """
    
    for photo in photos:
        html += f"""
            <div class="image-card">
                <img src="{photo.urls.regular}" 
                     alt="{photo.description or 'Social media photo'}">
                {photo.attribution.get_html()}
            </div>
        """
    
    html += "</div>"
    return html
```

## Development

To set up the development environment:

```bash
# Clone the repository
git clone https://github.com/yourusername/notunsplash-python-sdk.git
cd notunsplash-python-sdk

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
