from PIL import Image
import os

source_path = r"C:/Users/Dell/.gemini/antigravity/brain/bb4bbb6f-46ee-47ca-9130-c0f42e6b39ca/uploaded_media_1769502550639.png"
dest_path = r"c:\Users\Dell\Desktop\ScrapeWale\static\images\categories\copper.jpg"

def apply_image():
    try:
        # Open the uploaded image
        with Image.open(source_path) as img:
            # Convert to RGB (in case of transparent PNG) and save as JPG
            img = img.convert('RGB')
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            img.save(dest_path, 'JPEG')
            print(f"Successfully converted and saved user image to {dest_path}")
    except Exception as e:
        print(f"Error applying image: {e}")

if __name__ == "__main__":
    apply_image()
