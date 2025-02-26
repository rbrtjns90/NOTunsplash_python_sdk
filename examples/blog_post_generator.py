"""
Example of using the Unsplash SDK to generate blog post images
"""
import sys
from pathlib import Path
from datetime import datetime
import json

# Add the parent directory to Python path to import the package
sys.path.append(str(Path(__file__).parent.parent))
from notunsplash import Unsplash

def create_blog_header(topic: str, style: str = "minimal") -> str:
    """Create a blog header with a featured image and proper attribution"""
    client = Unsplash(access_key="your_access_key")
    
    # Search for a relevant photo
    photos = client.search_photos(
        topic,
        per_page=1,
        orientation="landscape"
    )
    
    if not photos:
        return "<p>No suitable images found.</p>"
    
    photo = photos[0]
    
    # Generate HTML with different styles
    if style == "minimal":
        html = f"""
            <header class="blog-header minimal">
                <img src="{photo.urls['regular']}" 
                     alt="{photo.description or 'Blog header image'}">
                {photo.attribution.html}
            </header>
            <style>
                .blog-header.minimal img {{
                    width: 100%;
                    max-height: 400px;
                    object-fit: cover;
                }}
            </style>
        """
    else:  # style == "overlay"
        html = f"""
            <header class="blog-header overlay">
                <div class="image-container">
                    <img src="{photo.urls['regular']}" 
                         alt="{photo.description or 'Blog header image'}">
                    <div class="attribution-overlay">
                        {photo.attribution.html}
                    </div>
                </div>
            </header>
            <style>
                .blog-header.overlay {{
                    position: relative;
                }}
                .blog-header.overlay img {{
                    width: 100%;
                    max-height: 400px;
                    object-fit: cover;
                }}
                .attribution-overlay {{
                    position: absolute;
                    bottom: 0;
                    left: 0;
                    right: 0;
                    background: rgba(0,0,0,0.7);
                    color: white;
                    padding: 10px;
                }}
            </style>
        """
    
    return html

def generate_blog_post(topic: str, num_images: int = 3) -> str:
    """Generate a sample blog post with Unsplash images and attribution"""
    client = Unsplash(access_key="your_access_key")
    
    # Format topic for title
    title = topic.title()
    post = f"# {title} - A Photo Journey\n"
    
    # Search for photos
    photos = client.search_photos(topic, per_page=num_images)
    if not photos:
        return post
    
    # Add each photo with its description and attribution
    for i, photo in enumerate(photos, 1):
        post += f"\n## Part {i}\n\n"
        post += f"![{photo.description or title}]({photo.urls['regular']})\n\n"
        post += f"{photo.attribution.markdown}\n\n"
        
        if photo.description:
            post += f"{photo.description}\n\n"
    
    return post

def main():
    # Generate a blog post about coffee
    blog_post = generate_blog_post("coffee brewing", num_images=2)
    
    if blog_post:
        # Save the blog post
        with open("coffee_blog_post.md", "w") as f:
            f.write(blog_post)
        
        print("Blog post generated successfully!")
        print("Check coffee_blog_post.md for the result")
    else:
        print("No photos found for the specified topic")

if __name__ == "__main__":
    # Example usage
    header = create_blog_header("coffee shop", style="overlay")
    print(header)
    
    post = generate_blog_post("coffee shop")
    print(post)
    
    main()
