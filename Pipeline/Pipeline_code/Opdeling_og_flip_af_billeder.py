# Indlæs pakker

import os
import glob
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd
import imageio
import numpy as np
import random
import shutil

# Indlæs data

# Definer stierne til sample billederne og destinationen for behandlede billeder
source_folder = os.path.join("Pipeline_data", "Raw_data") # Kilde til billederne
clean_data_folder = os.path.join("Pipeline_data", "Clean Data")
overbite_folder = os.path.join(clean_data_folder, "Overbite Data")
bolton_folder = os.path.join(clean_data_folder, "Bolton Data")

# Sørg for output folder eksisterer
os.makedirs(clean_data_folder, exist_ok=True)
os.makedirs(overbite_folder, exist_ok=True)
os.makedirs(bolton_folder, exist_ok=True)

# Indlæs billeder
image_files = [f for f in os.listdir(source_folder) if f.lower().endswith((".png", ".jpg", ".jpeg"))] # f.lower er bare lowercase
print(f"Loaded {len(image_files)} images from {source_folder}")

# Tjek dimension
width, height = None, None # Initialisering

for file in image_files:
    image_path = os.path.join(source_folder, file) # Mappe og billede/fil
    img = Image.open(image_path) # Åben billede på overstående image_path
    
    if width is None and height is None:
        width, height = img.size  # Dimension af første billeder (For sammenligning med andre)
    else:
        assert img.size == (width, height), f"Image {file} has different dimensions!" # img (vores billede) .size (Str.) Skal være lig med width og height, fra billede 1

print(f"✅ All images have dimensions: {width}x{height}")

# Opdel billede i 3
split_width = width // 3  # hvert billede får 1/3 af den originale størrelse

for file in image_files:
    image_path = os.path.join(source_folder, file)
    img = Image.open(image_path)
    
    base_name = os.path.splitext(file)[0]

    # Fjern "_combined" hvis det findes
    if "_combined" in base_name:
        base_name = base_name.replace("_combined", "")

    # Undgå gentagelse af suffix
    suffixes = ["lower", "upper", "middle"]
    parts = base_name.split("_")

    if parts[-1] in suffixes:
        suffix = parts[-1]
        base_name = "_".join(parts[:-1])  # Fjern suffix midlertidigt for at undgå gentagelse
    else:
        suffix = ""

    # Crop left, middle, right delene
    left_part = img.crop((0, 0, split_width, height))
    middle_part = img.crop((split_width, 0, 2 * split_width, height))
    right_part = img.crop((2 * split_width, 0, width, height))

    # Flip right billedet
    right_part = right_part.transpose(Image.FLIP_LEFT_RIGHT)

    # Konstruer de rigtige filnavne uden at gentage suffix
    left_filename = f"{base_name}_{suffix}_left.png" if suffix else f"{base_name}_left.png"
    middle_filename = f"{base_name}_{suffix}_middle.png" if suffix else f"{base_name}_middle.png"
    right_filename = f"{base_name}_{suffix}_right.png" if suffix else f"{base_name}_right.png"

    # Gem filerne i de rigtige mapper
    left_part.save(os.path.join(overbite_folder, left_filename))
    middle_part.save(os.path.join(bolton_folder, middle_filename))
    right_part.save(os.path.join(overbite_folder, right_filename))

print(f"✅ Processed {len(image_files)} images and saved to {clean_data_folder}")