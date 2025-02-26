"""
Example of using the Unsplash SDK to fetch and organize real estate listing images
"""
import sys
import os
from pathlib import Path
import json
import shutil
from typing import List, Dict, Optional

# Add the parent directory to Python path to import the package
sys.path.append(str(Path(__file__).parent.parent))
from notunsplash import Unsplash, Photo

class RealEstateImageFetcher:
    """Class to fetch and organize real estate images"""
    
    def __init__(self, access_key: str):
        """Initialize with Unsplash access key"""
        self.client = Unsplash(access_key=access_key)
        self.output_dir = "real_estate_images"
        
        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def fetch_images(self, category: str, num_images: int = 5) -> Optional[List[Dict]]:
        """Fetch images for a real estate category"""
        # Search for photos
        search_results = self.client.search_photos(
            f"real estate {category}",
            per_page=num_images,
            orientation="landscape"
        )
        
        if not search_results:
            print(f"No images found for category: {category}")
            return None
        
        # Create category directory
        category_dir = os.path.join(self.output_dir, category.replace(" ", "_"))
        if not os.path.exists(category_dir):
            os.makedirs(category_dir)
        
        # Process each photo
        results = []
        for i, photo in enumerate(search_results, 1):
            # Save photo metadata
            metadata = {
                "id": photo.id,
                "description": photo.description,
                "urls": photo.urls.__dict__,
                "attribution": photo.attribution.metadata
            }
            
            metadata_file = os.path.join(category_dir, f"photo_{i}_metadata.json")
            with open(metadata_file, "w") as f:
                json.dump(metadata, f, indent=2)
            
            # Generate HTML preview
            html_content = self._generate_preview_html(photo, category)
            html_file = os.path.join(category_dir, f"photo_{i}_preview.html")
            with open(html_file, "w") as f:
                f.write(html_content)
            
            results.append(metadata)
        
        return results
    
    def _generate_preview_html(self, photo: Photo, category: str) -> str:
        """Generate HTML preview for a photo"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Real Estate Image Preview - {category}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .container {{ max-width: 800px; margin: 0 auto; }}
                img {{ max-width: 100%; height: auto; border-radius: 8px; }}
                .attribution {{ margin-top: 10px; font-style: italic; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Real Estate Image Preview - {category}</h1>
                <img src="{photo.urls.regular}" alt="{photo.description or 'Real estate image'}">
                <div class="attribution">
                    {photo.attribution.get_html()}
                </div>
            </div>
        </body>
        </html>
        """

def main():
    # Initialize fetcher with your access key
    fetcher = RealEstateImageFetcher(
        access_key="ACCESS-KEY-HERE"
    )
    
    # Define real estate categories
    categories = [
        "luxury-home",
        "modern-apartment",
        "cozy-cottage",
        "office-space"
    ]
    
    # Fetch images for each category
    for category in categories:
        print(f"\nFetching {category} images...")
        results = fetcher.fetch_images(category, num_images=1)
        
        if results:
            print(f"Successfully downloaded {len(results)} images")
            print(f"Check the '{category}' directory for previews")

if __name__ == "__main__":
    main()
