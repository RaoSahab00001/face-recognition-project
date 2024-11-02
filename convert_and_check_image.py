from PIL import Image
import os

# Ensure path is correct
image_directory = os.path.join("Face", "Images")

if not os.path.exists(image_directory):
    print(f"Directory not found: {image_directory}")
else:
    print(f"Directory found: {image_directory}")
    for name in os.listdir(image_directory):
        image_path = os.path.join(image_directory, name)
        try:
            with Image.open(image_path) as img:
                rgb_img = img.convert("RGB")
                rgb_img.save(image_path)
                print(f"Converted and saved {name} to RGB format")
                
                # Verify the format
                if rgb_img.mode != "RGB":
                    print(f"Error: {name} is not in RGB format. Current format: {rgb_img.mode}")
                else:
                    print(f"Successfully verified {name} is in RGB format")
        except Exception as e:
            print(f"Error processing {name}: {e}")
