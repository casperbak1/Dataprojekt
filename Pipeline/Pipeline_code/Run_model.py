import csv
import math
import matplotlib.pyplot as plt

import torch, detectron2
TORCH_VERSION = ".".join(torch.__version__.split(".")[:2])
CUDA_VERSION = torch.__version__.split("+")[-1]
print("torch: ", TORCH_VERSION, "; cuda: ", CUDA_VERSION)
print("detectron2:", detectron2.__version__)

# Andre pakker

# Some basic setup:
# Setup detectron2 logger
from detectron2.utils.logger import setup_logger
setup_logger()

# import some common libraries
import numpy as np
import os, json, cv2, random
import pandas as pd

# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog
from detectron2.structures import BoxMode

import os
import cv2
from detectron2.data import DatasetCatalog, MetadataCatalog
from detectron2.engine import DefaultTrainer
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.evaluation import COCOEvaluator, inference_on_dataset
from detectron2.data import build_detection_test_loader
from detectron2.data.datasets import convert_to_coco_json
import shutil
from detectron2.engine import DefaultTrainer
from detectron2.config import get_cfg
from detectron2 import model_zoo

# Indlæs model:

# Reinitialize config
cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file("COCO-Keypoints/keypoint_rcnn_X_101_32x8d_FPN_3x.yaml"))
cfg.MODEL.WEIGHTS = os.path.join("Pipeline_data", "Model", "model_0054999.pth")  # Ændre sti til placering af modellen
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.9
cfg.MODEL.KEYPOINT_ON = True
cfg.MODEL.DEVICE = "cpu"
cfg.MODEL.ROI_KEYPOINT_HEAD.NUM_KEYPOINTS = 1 # Matcher træning

predictor = DefaultPredictor(cfg)

print("Model reloaded successfully!")



# Test
# Unregister dataset if already registered
if "my_test_dataset" in DatasetCatalog.list():
    DatasetCatalog.remove("my_test_dataset")

if "my_test_dataset" in MetadataCatalog.list():
    MetadataCatalog.remove("my_test_dataset")
    print("My Test dataset was removed")

test_folder = os.path.join("Pipeline_data", "Clean Data", "Overbite Data") # Change folder for other images

def test_dataset_function():
    dataset_dicts = []
    for idx, filename in enumerate(os.listdir(test_folder)):
        if filename.endswith((".jpg", ".png", ".jpeg")):
            record = {}
            file_path = os.path.join(test_folder, filename)

            height, width = cv2.imread(file_path).shape[:2]
            record["file_name"] = file_path
            record["image_id"] = idx
            record["height"] = height
            record["width"] = width
            record["annotations"] = []  # Ingen annotations (ren test data)

            dataset_dicts.append(record)
    return dataset_dicts

DatasetCatalog.register("my_test_dataset", test_dataset_function)
MetadataCatalog.get("my_test_dataset").set(thing_classes=["object"])




# File paths
image_folder = os.path.join("Pipeline_data", "Clean Data", "Overbite Data")
output_csv = "Pipeline_data/Predicted_keypoints.csv"

# Conversion
PIXEL_TO_MM = 0.08

# Load metadata and test dataset
dataset_dicts = DatasetCatalog.get("my_test_dataset")
metadata = MetadataCatalog.get("my_test_dataset")


# === MAIN LOOP: Predict, Save, Visualize ===
rows = [["Filename","X_Model", "Y_Model"]]

for sample in dataset_dicts:
    img_path = sample["file_name"]
    filename = os.path.splitext(os.path.basename(img_path))[0]

    # Read image and run prediction
    img = cv2.imread(img_path)
    outputs = predictor(img)

    instances = outputs["instances"].to("cpu")
    if not instances.has("pred_keypoints"):
        print(f"❌ No keypoints found in: {filename}")
        continue

    keypoints = instances.pred_keypoints
    if len(keypoints) == 0:
        print(f"⚠️ Empty keypoint list in: {filename}")
        continue

    # Assume first instance
    pred_x, pred_y, _ = keypoints[0][0].tolist()


    # Save to CSV row
    rows.append([filename, pred_x, pred_y])

# === SAVE FINAL CSV ===
with open(output_csv, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(rows)

print(f"✅ Final results saved to: {output_csv}")