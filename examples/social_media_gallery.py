"""
Example of using the Unsplash SDK to create a social media image gallery with HTML attribution
"""
import sys
import os
from pathlib import Path

# Add the parent directory to Python path to import the package
sys.path.append(str(Path(__file__).parent.parent))
from notunsplash import Unsplash

def create_gallery(theme: str, num_images: int = 6):
    """Create a responsive image gallery with proper attribution"""
    client = Unsplash(access_key="ACCES_KEY")
    
    # Search for photos directly instead of using collections
    search_results = client.search_photos(theme, per_page=num_images)
    if not search_results["results"]:
        return None
    
    # Generate HTML gallery
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Image Gallery</title>
        <style>
            .gallery {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                padding: 20px;
            }
            .image-card {
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .image-card img {
                width: 100%;
                height: 300px;
                object-fit: cover;
            }
            .unsplash-attribution {
                padding: 10px;
                font-size: 0.9em;
                color: #666;
            }
            .unsplash-attribution a {
                color: #333;
                text-decoration: none;
            }
            .unsplash-attribution a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="gallery">
    """
    
    # Add each photo with its attribution
    for photo in search_results["results"]:
        html += f"""
            <div class="image-card">
                <img src="{photo.urls.regular}" alt="{photo.description or 'Unsplash photo'}">
                {photo.attribution.get_html(css_class="unsplash-attribution")}
            </div>
        """
    
    html += """
        </div>
    </body>
    </html>
    """
    
    return html

def main():
    # Create a gallery of nature photos
    gallery_html = create_gallery("nature", num_images=4)
    
    if gallery_html:
        # Save the gallery
        with open("nature_gallery.html", "w") as f:
            f.write(gallery_html)
        
        print("Gallery generated successfully!")
        print("Open nature_gallery.html in your browser to view the result")
    else:
        print("No photos found for the specified theme")

if __name__ == "__main__":
    main()
