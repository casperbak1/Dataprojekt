# Initialize packages 

import os
import glob
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd
import imageio
import numpy as np
import random
import shutil

# Load data

# Define paths to the source images and the destination for processed images
source_folder = os.path.join("Pipeline_data", "Raw_data") # Source folder for raw images
clean_data_folder = os.path.join("Pipeline_data", "Clean Data")
overbite_folder = os.path.join(clean_data_folder, "Overbite Data")
bolton_folder = os.path.join(clean_data_folder, "Bolton Data")


# Make sure the output folders exist
# Create directories if they do not exist
os.makedirs(clean_data_folder, exist_ok=True)
os.makedirs(overbite_folder, exist_ok=True)
os.makedirs(bolton_folder, exist_ok=True)


# Load all image files from the source folder
image_files = [f for f in os.listdir(source_folder) if f.lower().endswith((".png", ".jpg", ".jpeg"))] # f.lower er bare lowercase
print(f"Loaded {len(image_files)} images from {source_folder}")

# Check dimension
width, height = None, None # Initialization af width og height

for file in image_files:
    image_path = os.path.join(source_folder, file) # Folder and file name
    img = Image.open(image_path) # Open image
    
    if width is None and height is None:
        width, height = img.size  # Dimension of the first image, used to compare with others
    else:
        assert img.size == (width, height), f"Image {file} has different dimensions!" # Check if all images have the same dimensions

print(f"All images have dimensions: {width}x{height}")

# Spilt images into three parts
split_width = width // 3  # Calculate the width of each part, Every image will get 1/3 of the width

# Process each image 
for file in image_files:
    image_path = os.path.join(source_folder, file)
    img = Image.open(image_path)
    
    base_name = os.path.splitext(file)[0]

    # Remove "_combined" from the base name if it exists
    if "_combined" in base_name:
        base_name = base_name.replace("_combined", "")


    # Avoid repeating suffixes like "lower", "upper", "middle"
    suffixes = ["lower", "upper", "middle"]
    parts = base_name.split("_")

    if parts[-1] in suffixes:
        suffix = parts[-1]
        base_name = "_".join(parts[:-1])  
    else:
        suffix = ""

    # Crop left, middle, right parts of the image
    left_part = img.crop((0, 0, split_width, height))
    middle_part = img.crop((split_width, 0, 2 * split_width, height))
    right_part = img.crop((2 * split_width, 0, width, height))

    # Flip right image 
    right_part = right_part.transpose(Image.FLIP_LEFT_RIGHT)


    # Create the filenames for the images
    left_filename = f"{base_name}_{suffix}_left.png" if suffix else f"{base_name}_left.png"
    middle_filename = f"{base_name}_{suffix}_middle.png" if suffix else f"{base_name}_middle.png"
    right_filename = f"{base_name}_{suffix}_right.png" if suffix else f"{base_name}_right.png"


    # Save the images in the respective folders
    left_part.save(os.path.join(overbite_folder, left_filename))
    middle_part.save(os.path.join(bolton_folder, middle_filename))
    right_part.save(os.path.join(overbite_folder, right_filename))

print(f"Processed {len(image_files)} images and saved to {clean_data_folder}")