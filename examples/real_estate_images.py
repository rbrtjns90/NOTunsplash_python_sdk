"""Example of using the Unsplash SDK to create real estate galleries"""
from notunsplash import Unsplash

def create_real_estate_gallery(category: str, num_images: int = 5) -> str:
    """Create an HTML gallery of real estate photos with proper attribution"""
    client = Unsplash(access_key="your_access_key")
    
    # Search for photos
    photos = client.search_photos(
        f"real estate {category}",
        per_page=num_images,
        orientation="landscape"
    )
    
    # Generate HTML gallery
    html = '<div class="gallery">'
    
    if not photos:
        return html + "</div>"
        
    for photo in photos:
        html += f"""
            <div class="image-card">
                <img src="{photo.urls['regular']}" 
                     alt="{photo.description or 'Real estate photo'}">
                {photo.attribution.html}
            </div>
        """
    html += "</div>"
    
    return html

if __name__ == "__main__":
    # Example usage
    gallery = create_real_estate_gallery("modern homes", num_images=3)
    print(gallery)
