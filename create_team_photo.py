from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder_image(path):
    # Ensure directory exists
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    # Create an image with a nice gradient or solid color
    width, height = 800, 600
    color = (25, 135, 84) # Bootstrap success green-ish
    image = Image.new('RGB', (width, height), color)
    
    draw = ImageDraw.Draw(image)
    
    # Add some text
    text = "Team ScrapeWale"
    
    # Simple logic to center text (approximate if font not loaded perfectly, but Pillow default font is small)
    # We'll try to use a basic method
    
    # Load default font
    # For better text we need a .ttf, but we might not have one. 
    # drawing a simple rectangle border and text
    
    # Draw border
    draw.rectangle([10, 10, width-10, height-10], outline="white", width=5)
    
    # Since we might not have a good font, let's just save it as a colored block with simple text
    # or try to load a system font. 
    # To be safe, I'll just save a colored placeholder.
    
    image.save(path)
    print(f"Image saved to {path}")

if __name__ == "__main__":
    create_placeholder_image(r"c:\Users\Dell\Desktop\ScrapeWale\static\images\team_photo.jpg")
