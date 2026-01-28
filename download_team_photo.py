import urllib.request
import ssl

def download_team_photo(url, path):
    try:
        # Create an unverified context to avoid SSL errors on some systems
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
    # URL for a professional team photo (Unsplash source)
    image_url = "https://images.unsplash.com/photo-1522071820081-009f0129c71c?q=80&w=800&auto=format&fit=crop"
    save_path = r"c:\Users\Dell\Desktop\ScrapeWale\static\images\team_photo.jpg"
    download_team_photo(image_url, save_path)
