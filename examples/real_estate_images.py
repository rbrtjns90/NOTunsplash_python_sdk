"""
Example program to fetch real estate related images from Unsplash
Includes proper attribution as required by Unsplash guidelines
"""
import sys
import os
from pathlib import Path
from datetime import datetime
import requests
from typing import Dict, List, Optional
import json

# Add the parent directory to Python path to import the package
sys.path.append(str(Path(__file__).parent.parent))
from notunsplash import Unsplash

class RealEstateImageFetcher:
    def __init__(self, access_key: str, output_dir: str = "downloaded_images"):
        """Initialize the image fetcher"""
        self.client = Unsplash(access_key=access_key)
        self.output_dir = output_dir
        self.attribution_dir = os.path.join(output_dir, "attribution")
        
        # Create output directories if they don't exist
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.attribution_dir, exist_ok=True)

    def fetch_images(self, query: str, num_images: int = 1) -> List[Dict]:
        """
        Fetch images for a specific query
        
        Args:
            query: Search query for photos
            num_images: Number of images to fetch
            
        Returns:
            List of photo metadata
        """
        print(f"\nFetching {query} images...")
        
        # Search for photos
        search_results = self.client.search_photos(query, per_page=num_images)
        photos = search_results["results"]
        
        # Process each photo
        results = []
        for photo in photos:
            # Download the image
            image_filename = f"{query}_{photo.id}.jpg"
            image_path = os.path.join(self.output_dir, image_filename)
            
            response = requests.get(photo.urls.regular)
            with open(image_path, "wb") as f:
                f.write(response.content)
            print(f"Downloaded: {image_filename}")
            
            # Print photo info
            print(f"Photo by: {photo.user.name}")
            print(f"Description: {photo.description or 'No description'}")
            print(f"Likes: {photo.likes}")
            
            # Save attribution
            print("Attribution:")
            print(photo.attribution.get_text())
            print("---")
            
            # Save attribution metadata
            attribution_filename = f"{query}_{photo.id}_attribution.json"
            attribution_path = os.path.join(self.attribution_dir, attribution_filename)
            with open(attribution_path, "w") as f:
                json.dump(photo.attribution.metadata, f, indent=2)
            
            results.append({
                "id": photo.id,
                "filename": image_filename,
                "attribution_file": attribution_filename,
                "photographer": photo.user.name,
                "description": photo.description,
                "likes": photo.likes,
                "urls": photo.urls.__dict__,
                "downloaded_at": datetime.now().isoformat()
            })
        
        return results

def main():
    # Replace with your actual Unsplash API access key
    ACCESS_KEY = "7jaFq17KqaXvGdtcvi0FZAIgtV0iEjxD9KHkUtaJ--I"
    
    # Create the image fetcher
    fetcher = RealEstateImageFetcher(
        access_key=ACCESS_KEY,
        output_dir="real_estate_images"
    )
    
    # Fetch images for different categories
    categories = [
        "luxury-home",
        "interior",
        "apartment",
        "agent",
        "team"
    ]
    
    all_results = {}
    for category in categories:
        results = fetcher.fetch_images(category, num_images=1)
        all_results[category] = results
    
    # Save all results to a single JSON file
    with open("real_estate_images/all_results.json", "w") as f:
        json.dump(all_results, f, indent=2)
    
    print("\nAttribution files have been saved in: real_estate_images/attribution")

if __name__ == "__main__":
    main()
