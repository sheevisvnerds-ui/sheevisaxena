import urllib.request
import ssl

def download_image(url, path):
    try:
        context = ssl._create_unverified_context()
        with urllib.request.urlopen(url, context=context) as response:
            if response.status == 200:
                with open(path, 'wb') as f:
                    f.write(response.read())
                print(f"Image successfully downloaded to {path}")
            else:
                print(f"Failed to download image. Status code: {response.status}")
    except Exception as e:
        print(f"Error downloading image: {e}")

if __name__ == "__main__":
    # URL for scrap/recycling image (Unsplash source)
    # Searching for 'recycling', 'scrap metal', 'waste management'
    # Image: Bales of crushed plastic/paper or metal scrap
    image_url = "https://images.unsplash.com/photo-1532996122724-e3c354a0b15b?q=80&w=800&auto=format&fit=crop"
    save_path = r"c:\Users\Dell\Desktop\ScrapeWale\static\images\scrap_photo.jpg"
    download_image(image_url, save_path)
