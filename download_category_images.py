import urllib.request
import ssl
import os
from PIL import Image, ImageDraw, ImageFont

def create_fallback_image(path, name):
    try:
        # Define colors for categories
        colors = {
            "newspaper": (220, 220, 220), # Light Grey
            "cardboard": (139, 69, 19),   # Saddle Brown
            "iron": (105, 105, 105),      # Dim Grey
            "plastic": (0, 191, 255),     # Deep Sky Blue
            "brass": (184, 134, 11),      # Dark Goldenrod
            "copper": (210, 105, 30),     # Chocolate
            "ewaste": (34, 139, 34),      # Forest Green
            "aluminium": (192, 192, 192)  # Silver
        }
        
        key = os.path.basename(path).replace('.jpg', '').lower()
        color = colors.get(key, (128, 128, 128))
        
        width, height = 800, 600
        image = Image.new('RGB', (width, height), color)
        draw = ImageDraw.Draw(image)
        
        # Draw border
        draw.rectangle([20, 20, width-20, height-20], outline="white", width=10)
        
        # Add Text
        try:
            # Try to use Arial on Windows
            font = ImageFont.truetype("arial.ttf", 60)
        except IOError:
            font = ImageFont.load_default()
            
        text = name.upper()
        # Calculate text position (rough approximation if font.getsize not available in old PIL)
        # using anchor 'mm' (middle-middle) is good in newer Pillow, but fallback to simple draw
        
        # robust centering
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (width - text_width) / 2
        y = (height - text_height) / 2
        
        draw.text((x, y), text, fill="white", font=font)
        
        image.save(path)
        print(f"Generated labeled fallback image for {name} at {path}")
    except Exception as e:
        print(f"Error creating fallback: {e}")

def download_image(urls, path, name):
    # Ensure urls is a list
    if isinstance(urls, str):
        urls = [urls]
        
    os.makedirs(os.path.dirname(path), exist_ok=True)
    context = ssl._create_unverified_context()
    
    for i, url in enumerate(urls):
        try:
            print(f"Attempting source {i+1} for {name}...")
            # Add User-Agent header
            req = urllib.request.Request(
                url, 
                data=None, 
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
            )
            
            with urllib.request.urlopen(req, context=context, timeout=15) as response:
                if response.status == 200:
                    with open(path, 'wb') as f:
                        f.write(response.read())
                    print(f"Image successfully downloaded to {path}")
                    return # Success!
                    
        except Exception as e:
            print(f"Failed source {i+1} for {name}: {e}")
            continue # Try next URL

    # If we are here, ALL downloads failed. Create fallback.
    print(f"All sources failed for {name}. Creating fallback...")
    create_fallback_image(path, name)

if __name__ == "__main__":
    base_dir = r"c:\Users\Dell\Desktop\ScrapeWale\static\images\categories"
    
    # Categories with Primary and Backup URLs
    categories = {
        "newspaper.jpg": [
            "https://images.unsplash.com/photo-1585251315578-83863459c55d?q=80&w=800&auto=format&fit=crop", # Unsplash
            "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/A_stack_of_newspapers.jpg/800px-A_stack_of_newspapers.jpg" # Wikimedia Backup
        ],
        "cardboard.jpg": [
            "https://images.unsplash.com/photo-1589366115933-2a5436605bd2?q=80&w=800&auto=format&fit=crop",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Cardboard_boxes.jpg/800px-Cardboard_boxes.jpg" # Generic backup (if exists, guessing safe one)
        ],
        "iron.jpg": [
            "https://images.unsplash.com/photo-1533236897111-3e94666b27d4?q=80&w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1518709540826-17b514ee5c0c?q=80&w=800&auto=format&fit=crop" # Alternative rusty metal
        ],
        "plastic.jpg": "https://images.unsplash.com/photo-1591193686104-f3ec050e96ce?q=80&w=800&auto=format&fit=crop",
        "brass.jpg": "https://plus.unsplash.com/premium_photo-1664303847960-586318f59035?q=80&w=800&auto=format&fit=crop",
        "copper.jpg": "https://images.unsplash.com/photo-1617711902787-16443c5b9679?q=80&w=800&auto=format&fit=crop",
        "ewaste.jpg": "https://images.unsplash.com/photo-1550989460-0adf9ea622e2?q=80&w=800&auto=format&fit=crop",
        "aluminium.jpg": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?q=80&w=800&auto=format&fit=crop"
    }

    for filename, urls in categories.items():
        save_path = os.path.join(base_dir, filename)
        name = filename.split('.')[0].capitalize()
        download_image(urls, save_path, name)
