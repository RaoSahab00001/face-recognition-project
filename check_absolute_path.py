import os

# Use absolute path
image_directory = os.path.join(os.getcwd(), "Face", "Images")

if not os.path.exists(image_directory):
    print(f"Directory not found: {image_directory}")
else:
    print(f"Directory found: {image_directory}")
    for name in os.listdir(image_directory):
        print(name)
