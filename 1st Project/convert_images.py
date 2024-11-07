from PIL import Image
import os

# Use absolute path
image_directory = os.path.join(os.getcwd(), "Face", "Images")

if not os.path.exists(image_directory):
    print(f"Directory not found: {image_directory}")
else:
    print(f"Directory found: {image_directory}")
    for name in os.listdir(image_directory):
        image_path = os.path.join(image_directory, name)
        with Image.open(image_path) as img:
            rgb_img = img.convert("RGB")
            rgb_img.save(image_path)
        print(f"Converted {name} to RGB")
