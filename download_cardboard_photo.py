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
    # Image: Cardboard boxes stack
    image_url = "https://images.unsplash.com/photo-1589939705384-5185137a7f0f?q=80&w=800&auto=format&fit=crop"
    save_path = r"c:\Users\Dell\Desktop\ScrapeWale\static\images\cardboard_scrap.jpg"
    download_image(image_url, save_path)
