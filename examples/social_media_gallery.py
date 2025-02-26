"""
Example of using the Unsplash SDK to create social media galleries
"""
import sys
import os
from pathlib import Path

# Add the parent directory to Python path to import the package
sys.path.append(str(Path(__file__).parent.parent))
from notunsplash import Unsplash

def create_social_gallery(theme: str, num_images: int = 6) -> str:
    """Create a responsive image gallery for social media"""
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
                <img src="{photo.urls['regular']}" 
                     alt="{photo.description or 'Social media photo'}">
                {photo.attribution.html}
            </div>
        """
    
    html += "</div>"
    return html

if __name__ == "__main__":
    # Example usage
    gallery = create_social_gallery("food", num_images=4)
    print(gallery)
