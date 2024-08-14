import os
import shutil
import random
import numpy as np
from pycocotools.coco import COCO

def polygon_to_bbox(polygon):
    """
    Convert COCO polygon coordinates to bounding box coordinates.
    """
    x_coords = polygon[0::2]
    y_coords = polygon[1::2]
    xmin = min(x_coords)
    xmax = max(x_coords)
    ymin = min(y_coords)
    ymax = max(y_coords)
    return xmin, ymin, xmax - xmin, ymax - ymin

def coco_to_yolo(coco_json, images_dir, output_dir, train_ratio=0.7, val_ratio=0.15, test_ratio=0.15):
    assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 1e-2, "Ratios must sum to 1.0"

    coco = COCO(coco_json)
    categories = coco.loadCats(coco.getCatIds())
    category_dict = {cat['id']: cat['name'] for cat in categories}

    # Get all image IDs and shuffle
    img_ids = coco.getImgIds()
    random.shuffle(img_ids)

    # Split image IDs
    total_images = len(img_ids)
    train_end = int(total_images * train_ratio)
    val_end = train_end + int(total_images * val_ratio)

    train_img_ids = img_ids[:train_end]
    val_img_ids = img_ids[train_end:val_end]
    test_img_ids = img_ids[val_end:]

    # Ensure output directories exist
    for split in ['train', 'val', 'test']:
        os.makedirs(os.path.join(output_dir, 'images', split), exist_ok=True)
        os.makedirs(os.path.join(output_dir, 'labels', split), exist_ok=True)

    def process_images(img_ids, split_name):
        for img_id in img_ids:
            img_info = coco.loadImgs(img_id)[0]
            img_file = img_info['file_name']
            img_path = os.path.join(images_dir, img_file)
            if os.path.exists(img_path):
                shutil.copy(img_path, os.path.join(output_dir, 'images', split_name, img_file))
                ann_ids = coco.getAnnIds(imgIds=img_id)
                anns = coco.loadAnns(ann_ids)

                # Write YOLO format labels
                with open(os.path.join(output_dir, 'labels', split_name, f"{img_file.split('.')[0]}.txt"), 'w') as f:
                    for ann in anns:
                        cat_id = ann['category_id'] - 1  # YOLO expects class IDs to start from 0
                        if ann['segmentation']:
                            polygon = ann['segmentation'][0]  # Use the first polygon if there are multiple
                            xmin, ymin, width, height = polygon_to_bbox(polygon)
                            img_width, img_height = img_info['width'], img_info['height']
                            x_center = (xmin + width / 2) / img_width
                            y_center = (ymin + height / 2) / img_height
                            width /= img_width
                            height /= img_height
                            f.write(f"{cat_id} {x_center} {y_center} {width} {height}\n")

    process_images(train_img_ids, 'train')
    process_images(val_img_ids, 'val')
    process_images(test_img_ids, 'test')

    print("Dataset conversion and split completed.")

# Paths to your dataset
coco_json = r"\\192.168.200.5\Buero\Projekte\Automatic damage detection\labelstudio-sam2\Conversion\coco.json"
images_dir = r"\\192.168.200.5\Buero\Projekte\Automatic damage detection\labelstudio-sam2\Conversion\source_images"
output_dir = r"\\192.168.200.5\Buero\Projekte\Automatic damage detection\labelstudio-sam2\training\dataset"

# Convert COCO dataset to YOLO format and split
coco_to_yolo(coco_json, images_dir, output_dir)
