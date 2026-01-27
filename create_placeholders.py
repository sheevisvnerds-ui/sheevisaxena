from PIL import Image, ImageDraw
import os

def create_placeholder(name, color, text):
    path = rf"c:\Users\Dell\Desktop\ScrapeWale\static\images\categories\{name}.jpg"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    width, height = 800, 600
    image = Image.new('RGB', (width, height), color)
    draw = ImageDraw.Draw(image)
    
    # Draw simple border
    draw.rectangle([20, 20, width-20, height-20], outline="white", width=10)
    
    # We won't add text as we might lack fonts, but the color will distinguish it.
    # Brass: Goldish, Copper: Reddish-Orange
    
    image.save(path)
    print(f"Created placeholder for {name} at {path}")

if __name__ == "__main__":
    # Brass: Golden/Yellowish
    create_placeholder("brass", (181, 166, 66), "Brass")
    
    # Copper: Reddish/Orange
    create_placeholder("copper", (184, 115, 51), "Copper")
