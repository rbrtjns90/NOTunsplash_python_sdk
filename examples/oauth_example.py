"""
Example demonstrating OAuth authentication flow with NOTunsplash SDK
"""
import os
from notunsplash import Unsplash
from notunsplash.errors import UnsplashAuthError

def main():
    # Get credentials from environment variables
    access_key = os.getenv("UNSPLASH_ACCESS_KEY")
    secret_key = os.getenv("UNSPLASH_SECRET_KEY")
    redirect_uri = os.getenv("UNSPLASH_REDIRECT_URI")

    if not all([access_key, secret_key, redirect_uri]):
        print("Please set the following environment variables:")
        print("- UNSPLASH_ACCESS_KEY")
        print("- UNSPLASH_SECRET_KEY")
        print("- UNSPLASH_REDIRECT_URI")
        return

    try:
        # Initialize with OAuth credentials
        client = Unsplash(
            access_key=access_key,
            secret_key=secret_key
        )
        
        # Generate authorization URL
        auth_url = client.get_oauth_url(
            redirect_uri=redirect_uri,
            scope=["public", "write_likes"]  # Optional: defaults to ["public"]
        )
        print(f"\nStep 1: Visit this URL to authorize:")
        print(auth_url)
        
        # Get the authorization code from user input
        print("\nStep 2: After authorization, you'll be redirected to your redirect URI")
        print("Copy the 'code' parameter from the URL and paste it below")
        auth_code = input("Enter the authorization code: ").strip()
        
        # Exchange code for token
        print("\nStep 3: Exchanging authorization code for access token...")
        token = client.get_oauth_token(
            code=auth_code,
            redirect_uri=redirect_uri
        )
        
        # Set token for authenticated requests
        client.set_oauth_token(token["access_token"])
        print("Successfully authenticated!")
        
        # Example of using an authenticated endpoint
        print("\nStep 4: Testing authenticated endpoint...")
        photos = client.search_photos(query="sunset", per_page=1)
        if photos:
            photo_id = photos[0].id
            client.like_photo(photo_id)
            print(f"Successfully liked photo: {photo_id}")
        
    except UnsplashAuthError as e:
        print(f"Authentication error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
