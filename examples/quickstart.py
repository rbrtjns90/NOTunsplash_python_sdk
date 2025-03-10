"""
Quick start example showing basic usage of the NOTunsplash SDK
"""
import os
from notunsplash import Unsplash
from notunsplash.errors import UnsplashError, UnsplashAuthError

def main():
    # Get access key from environment variable
    access_key = os.getenv("UNSPLASH_ACCESS_KEY")
    if not access_key:
        print("Please set UNSPLASH_ACCESS_KEY environment variable")
        return

    try:
        # Initialize client
        client = Unsplash(access_key=access_key)

        # Search for photos
        photos = client.search_photos(
            query="nature",    # Query is a required parameter
            page=1,           # Optional: default is 1
            per_page=10       # Optional: default is 10
        )

        print(f"Found {len(photos)} photos:\n")
        
        for photo in photos:
            print(f"Photo by {photo.user.name}")
            print(f"Description: {photo.description or 'No description'}")
            print(f"Regular size URL: {photo.urls['regular']}")
            print(f"Attribution: {photo.attribution.html}")
            print("-" * 80 + "\n")

    except UnsplashAuthError as e:
        print(f"Authentication error: {e}")
    except UnsplashError as e:
        print(f"API error: {e}")

if __name__ == "__main__":
    main()
