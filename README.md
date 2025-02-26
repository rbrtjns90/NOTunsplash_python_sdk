# NotUnsplash Python SDK

A comprehensive Python library for interacting with the Unsplash API, featuring robust error handling, OAuth support, and proper attribution.

## Features

- Full Unsplash API support
- OAuth 2.0 authentication
- Proper attribution handling (HTML, Markdown, reStructuredText)
- 97% test coverage
- Modern Python type hints
- Comprehensive error handling
- Easy to use models

## Installation

```bash
pip install notunsplash
```

## Quick Start

```python
from notunsplash import Unsplash

# Initialize with your access key
client = Unsplash(access_key="your-access-key")

# Search for photos
photos = client.search_photos("nature", per_page=10)
for photo in photos:
    print(f"Photo by {photo.user.name}: {photo.urls['regular']}")
    # Get attribution
    print(photo.attribution.html)  # HTML format
    print(photo.attribution.markdown)  # Markdown format
```

## OAuth Authentication

```python
# Initialize with both access key and secret key for OAuth
client = Unsplash(
    access_key="your-access-key",
    secret_key="your-secret-key"
)

# Generate authorization URL
auth_url = client.get_oauth_url(
    redirect_uri="your-redirect-uri",
    scope=["public", "write_likes"]
)

# Exchange code for access token
token = client.get_oauth_token(
    code="authorization-code",
    redirect_uri="your-redirect-uri"
)

# Set access token for authenticated requests
client.set_oauth_token(token["access_token"])
```

## Attribution

Proper attribution is required when using Unsplash photos. The SDK provides multiple attribution formats:

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

## Models

The SDK provides rich models for Unsplash entities:

- `Photo`: Full photo metadata, URLs, and attribution
- `User`: User profile information and statistics
- `Collection`: Photo collection details
- `Topic`: Editorial topic information

## Error Handling

The SDK provides comprehensive error handling:

```python
from notunsplash.errors import UnsplashAuthError

try:
    # This requires authentication
    client.like_photo("photo-id")
except UnsplashAuthError as e:
    print(f"Authentication error: {e}")
```

## Development

### Requirements

- Python 3.8+
- pytest for testing
- requests for HTTP
- python-dateutil for date parsing

### Testing

The SDK has comprehensive test coverage (97%):

```bash
# Run tests with coverage
pytest tests/ -v --cov=notunsplash

# Current test status:
# 22 tests passing
# 97% code coverage
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Unsplash](https://unsplash.com) for their amazing API
- All the photographers who share their work on Unsplash
