import os
import django
from django.core.files import File

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scrapewale.settings')
django.setup()

from core.models import ScrapCategory

def update_images():
    # Map category names to filenames (case-insensitive matching for category name)
    # Ensure keys match names in DB (Newspaper, Cardboard, Iron, Plastic, Brass, Copper, E-Waste, Aluminium)
    image_map = {
        "Newspaper": "newspaper.jpg",
        "Cardboard": "cardboard.jpg",
        "Iron": "iron.jpg",
        "Plastic": "plastic.jpg",
        "Brass": "brass.jpg",
        "Copper": "copper.jpg",
        "E-Waste": "ewaste.jpg",
        "Aluminium": "aluminium.jpg"
    }
    
    base_dir = r"c:\Users\Dell\Desktop\ScrapeWale\static\images\categories"

    for cat_name, filename in image_map.items():
        try:
            category = ScrapCategory.objects.get(name__iexact=cat_name)
            file_path = os.path.join(base_dir, filename)
            
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    # distinct filename to avoid overwrites if using same name
                    category.image.save(filename, File(f), save=True)
                    print(f"Updated image for {category.name}")
            else:
                print(f"File not found for {cat_name}: {file_path}")
                
        except ScrapCategory.DoesNotExist:
            print(f"Category '{cat_name}' not found in database. Please ensure it exists.")
        except Exception as e:
            print(f"Error updating {cat_name}: {e}")

if __name__ == "__main__":
    update_images()
