import os
import json
import numpy as np
from skimage import measure
from PIL import Image
import cv2

# Paths to your images and masks
images_dir = r"\\192.168.200.5\Buero\Projekte\Automatic damage detection\labelstudio-sam2\Conversion\source_images"
masks_dir = r"\\192.168.200.5\Buero\Projekte\Automatic damage detection\labelstudio-sam2\Conversion\masks"
output_json = r"\\192.168.200.5\Buero\Projekte\Automatic damage detection\labelstudio-sam2\Conversion\coco.json"

# Initialize COCO format dictionary
coco = {
    "info": {
        "description": "Dataset",
        "version": "1.0",
        "year": 2024,
    },
    "licenses": [],
    "images": [],
    "annotations": [],
    "categories": []
}

# Define your categories
categories = [
    {"id": 1, "name": "Connections", "supercategory": "none"},
    {"id": 2, "name": "Cracks", "supercategory": "none"},
    {"id": 3, "name": "Roots", "supercategory": "none"},
]
coco['categories'] = categories

annotation_id = 1

# Helper function to get category id from name
def get_category_id(category_name):
    for category in categories:
        if category['name'] == category_name:
            return category['id']
    return None

# Iterate over masks
for mask_filename in os.listdir(masks_dir):
    print(mask_filename)
    if mask_filename.endswith('.png'):
        # Parse mask filename
        parts = mask_filename.split('-')
        image_filename = f'{parts[0]}-{parts[1]}.jpg'  # Assuming task-4925.jpg format for image filename
        category_name = parts[7]  # Extracts the category name like "Connections"
        
        # Get corresponding image
        image_path = os.path.join(images_dir, image_filename)
        if not os.path.exists(image_path):
            continue

        image_id = int(parts[1])  # Assuming task-4925 => image_id = 4925
        
        # Read image and get its dimensions
        image = Image.open(image_path)
        width, height = image.size
        
        # Add image info to COCO dictionary (if not already added)
        if not any(img['id'] == image_id for img in coco['images']):
            coco['images'].append({
                "id": image_id,
                "file_name": image_filename,
                "width": width,
                "height": height
            })
        
        # Process mask
        mask_path = os.path.join(masks_dir, mask_filename)
        mask = np.array(Image.open(mask_path).convert('1'))  # Convert to binary
        
        # Find contours (bounding polygons)
        contours = measure.find_contours(mask, 0.5)
        
        for contour in contours:
            contour = np.flip(contour, axis=1)
            segmentation = contour.ravel().tolist()

            # Ensure the segmentation has more than 4 points to form a valid polygon
            if len(segmentation) >= 6:
                # Calculate bounding box for completeness (not used in YOLO format)
                x, y, w, h = cv2.boundingRect(contour.astype(np.int32))

                # Add annotation info to COCO dictionary
                coco['annotations'].append({
                    "id": annotation_id,
                    "image_id": image_id,
                    "category_id": get_category_id(category_name),
                    "segmentation": [segmentation],
                    "bbox": [x, y, w, h],
                    "area": w * h,
                    "iscrowd": 0
                })
                annotation_id += 1

# Save to JSON
with open(output_json, 'w') as f:
    json.dump(coco, f, indent=4)

print(f"COCO annotations saved to {output_json}")
