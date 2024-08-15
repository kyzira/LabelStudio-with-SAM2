import json
import os


json_path = r"C:\Users\K3000\Downloads\info.json" 
with open(json_path, 'r') as file:
    data = json.load(file)

# Extract the mapping from the JSON file
image_to_task_map = {}
for entry in data:
    original_image_path = entry["image"].split('/')[-1]  # Extract the original image name (removing everything before the last /)
    task_id = entry["id"]
    image_to_task_map[original_image_path] = f'task-{task_id}'

# Directory containing source images
source_images_dir = r"C:\Users\K3000\Downloads\source"

# Rename the files
for original_image_name, task_name in image_to_task_map.items():
    original_image_path = os.path.join(source_images_dir, original_image_name)
    if os.path.exists(original_image_path):
        new_image_name = f'{task_name}.jpg'  # Assumes images are in JPG format; adjust as needed
        new_image_path = os.path.join(source_images_dir, new_image_name)
        os.rename(original_image_path, new_image_path)
        print(f'Renamed {original_image_name} to {new_image_name}')
    else:
        print(f'Image {original_image_name} not found in the directory.')

