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
    # URL for broken items/junk (broken glass, waste)
    # Searching for 'broken glass', 'rubble', 'waste' - focusing on 'broken things'
    # This URL represents broken glass/rubble/waste pile
    image_url = "https://images.unsplash.com/photo-1605600659908-0ef719419d41?q=80&w=800&auto=format&fit=crop"
    save_path = r"c:\Users\Dell\Desktop\ScrapeWale\static\images\broken_scrap.jpg"
    download_image(image_url, save_path)
