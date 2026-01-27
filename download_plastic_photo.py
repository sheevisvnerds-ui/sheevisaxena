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
    # URL for plastic crates/drums (matching user example)
    # Searching for 'plastic crates', 'recycling plastic drums', 'industrial plastic waste'
    # Image: Piles of colorful plastic crates/containers
    image_url = "https://images.unsplash.com/photo-1621451537084-482c73073a0f?q=80&w=800&auto=format&fit=crop"
    save_path = r"c:\Users\Dell\Desktop\ScrapeWale\static\images\plastic_scrap.jpg"
    download_image(image_url, save_path)
