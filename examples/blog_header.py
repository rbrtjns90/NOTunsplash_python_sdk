"""
Example of creating a blog header with NOTunsplash SDK
"""
import os
from notunsplash import Unsplash
from notunsplash.errors import UnsplashError, UnsplashAuthError

def create_blog_header(topic: str) -> str:
    """Create a blog header with a photo and proper attribution"""
    try:
        client = Unsplash(access_key=os.getenv("UNSPLASH_ACCESS_KEY"))
        
        # Search for a photo
        photos = client.search_photos(
            query=topic,
            per_page=1
        )
        
        if not photos:
            return "<p>No suitable images found.</p>"
        
        photo = photos[0]
        
        # Track the photo usage asynchronously
        try:
            client.download_photo(photo.id)
        except Exception as e:
            # Log the error but don't fail the whole request
            print(f"Warning: Failed to track photo usage: {e}")
        
        # Create a header with responsive image and attribution
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blog Header Example</title>
    <style>
        .blog-header {{
            position: relative;
            width: 100%;
            max-height: 500px;
            overflow: hidden;
        }}
        .blog-header img {{
            width: 100%;
            height: auto;
            object-fit: cover;
        }}
        .attribution {{
            position: absolute;
            bottom: 10px;
            right: 10px;
            background: rgba(0, 0, 0, 0.7);
            color: white;
            padding: 5px 10px;
            border-radius: 3px;
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
    <header class="blog-header">
        <picture>
            <source media="(min-width: 1080px)" srcset="{photo.urls['regular']}">
            <source media="(min-width: 400px)" srcset="{photo.urls['small']}">
            <img src="{photo.urls['thumb']}" 
                 alt="{photo.description or photo.alt_description or 'Blog header image'}"
                 loading="lazy">
        </picture>
        <div class="attribution">
            {photo.attribution.html}
        </div>
    </header>
</body>
</html>"""
    except UnsplashAuthError as e:
        return f"<p>Authentication error: {e}</p>"
    except UnsplashError as e:
        return f"<p>API error: {e}</p>"

def main():
    # Get access key from environment variable
    if not os.getenv("UNSPLASH_ACCESS_KEY"):
        print("Please set UNSPLASH_ACCESS_KEY environment variable")
        return

    # Create blog header
    topic = input("Enter a topic for your blog header (e.g., 'coffee shop'): ").strip()
    html = create_blog_header(topic)
    
    # Save to file
    output_file = "blog_header.html"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"\nBlog header has been saved to {output_file}")
    print("Open it in a web browser to see the result!")

if __name__ == "__main__":
    main()
