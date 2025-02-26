"""
Example of creating a social media gallery with NOTunsplash SDK
"""
import os
from notunsplash import Unsplash
from notunsplash.errors import UnsplashError, UnsplashAuthError

def create_social_gallery(theme: str, num_images: int = 6) -> str:
    """Create a responsive image gallery with proper attribution"""
    try:
        client = Unsplash(access_key=os.getenv("UNSPLASH_ACCESS_KEY"))
        
        # Search for photos
        photos = client.search_photos(
            query=theme,
            per_page=num_images
        )
        
        # Create a complete HTML page with responsive grid
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Social Media Gallery - {theme}</title>
    <style>
        .gallery {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            padding: 20px;
        }}
        .image-card {{
            position: relative;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .image-card img {{
            width: 100%;
            height: 300px;
            object-fit: cover;
            display: block;
        }}
        .attribution {{
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: rgba(0, 0, 0, 0.7);
            color: white;
            padding: 8px;
            font-size: 12px;
        }}
        .attribution a {{
            color: white;
            text-decoration: none;
        }}
        .attribution a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="gallery">
        {"".join(f'''
        <div class="image-card">
            <img src="{photo.urls['regular']}" 
                 alt="{photo.description or photo.alt_description or 'Gallery image'}">
            <div class="attribution">
                {photo.attribution.html}
            </div>
        </div>
        ''' for photo in photos)}
    </div>
</body>
</html>"""
    except UnsplashAuthError as e:
        return f"""<!DOCTYPE html>
<html>
<body>
    <p>Authentication error: {e}</p>
</body>
</html>"""
    except UnsplashError as e:
        return f"""<!DOCTYPE html>
<html>
<body>
    <p>API error: {e}</p>
</body>
</html>"""

def main():
    # Get access key from environment variable
    if not os.getenv("UNSPLASH_ACCESS_KEY"):
        print("Please set UNSPLASH_ACCESS_KEY environment variable")
        return

    # Get user input
    theme = input("Enter a theme for your gallery (e.g., 'food'): ").strip()
    try:
        num_images = int(input("Enter number of images (1-30): ").strip())
        num_images = max(1, min(30, num_images))  # Limit between 1 and 30
    except ValueError:
        num_images = 6  # Default if invalid input
    
    # Create gallery
    html = create_social_gallery(theme, num_images)
    
    # Save to file
    output_file = "social_gallery.html"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"\nGallery has been saved to {output_file}")
    print("Open it in a web browser to see the result!")

if __name__ == "__main__":
    main()
