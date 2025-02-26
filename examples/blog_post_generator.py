"""
Example of using the Unsplash SDK to generate a blog post with images and proper attribution
"""
import sys
from pathlib import Path
from datetime import datetime
import json

# Add the parent directory to Python path to import the package
sys.path.append(str(Path(__file__).parent.parent))
from notunsplash import Unsplash

def generate_blog_post(topic: str, num_images: int = 3):
    """Generate a sample blog post with Unsplash images and attribution"""
    client = Unsplash(access_key="7jaFq17KqaXvGdtcvi0FZAIgtV0iEjxD9KHkUtaJ--I")
    
    # Search for relevant photos
    search_results = client.search_photos(topic, per_page=num_images)
    if not search_results["results"]:
        return None
    
    # Generate markdown blog post
    post = f"# {topic.title()} - A Photo Journey\n\n"
    post += f"_Created on {datetime.now().strftime('%B %d, %Y')}_\n\n"
    
    # Add photos with attribution
    for i, photo in enumerate(search_results["results"], 1):
        # Add photo description
        description = photo.description or f"Image {i}"
        post += f"## {description}\n\n"
        
        # Add photo URL
        post += f"![{description}]({photo.urls.regular})\n\n"
        
        # Add attribution in markdown format
        post += f"_{photo.attribution.get_markdown()}_\n\n"
        
        # Save photo metadata for reference
        metadata = photo.attribution.metadata
        with open(f"photo_{i}_metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)
    
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
    main()
