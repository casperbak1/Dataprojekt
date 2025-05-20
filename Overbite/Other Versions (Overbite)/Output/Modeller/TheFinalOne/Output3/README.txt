Initialisations should be:

# Load the annotations from the CSV file
ANNOTATIONS_FILE = "Dataprojekt/Data/Clean Data/Overbite Data/Updated_Labels.csv"
annotations_df = pd.read_csv(ANNOTATIONS_FILE)

# Sti til dataen
DATASET_PATH = "Dataprojekt/Data/Clean Data/Overbite Data/Annotated Data Pairs"

def my_dataset_function():
    dataset_dicts = []

    grouped_annotations = annotations_df.groupby("Filename")

    for idx, filename in enumerate(os.listdir(DATASET_PATH)):
        if filename.endswith((".jpg", ".png", ".jpeg")):
            record = {}
            file_path = os.path.join(DATASET_PATH, filename)

            # Read image dimensions
            image = cv2.imread(file_path)
            height, width = image.shape[:2]

            record["file_name"] = file_path
            record["image_id"] = idx
            record["height"] = height
            record["width"] = width

            record["annotations"] = []

            if filename in grouped_annotations.groups:
                keypoints_list = []
                bboxes = []

                for _, row in grouped_annotations.get_group(filename).iterrows():
                    x, y = row["X"], row["Y"]
                    
                    # Add keypoint
                    keypoints_list.extend([x, y, 2])  # visible

                    # Create a bounding box around the keypoint
                    box_x = max(x - 50, 0)
                    box_y = max(y, 0)
                    box_w = min(100, width - box_x)
                    box_h = min(100, height - box_y)

                    bboxes.append([box_x, box_y, box_w, box_h])

                # One annotation per keypoint
                for i in range(len(keypoints_list) // 3):
                    x = keypoints_list[i * 3]
                    y = keypoints_list[i * 3 + 1]
                    annotation = {
                        "bbox": bboxes[i],
                        "bbox_mode": BoxMode.XYWH_ABS,
                        "category_id": 0,
                        "keypoints": keypoints_list[i*3:i*3+3],
                        "num_keypoints": 1
                    }
                    record["annotations"].append(annotation)

            dataset_dicts.append(record)

    return dataset_dicts

# Register the dataset
DatasetCatalog.register("Overbite_Data", my_dataset_function)
MetadataCatalog.get("Overbite_Data").set(
    thing_classes=["object"],  # Modify for actual class names (Mangler godt navn)
    keypoint_names=["keypoint"],  # Name of keypoints (Mangler endnu bedre navn)
    keypoint_flip_map=[]  # Add keypoint flip pairs if needed (Nope)
)

# Test if it works
dataset_dicts = DatasetCatalog.get("Overbite_Data")
print(f"Loaded {len(dataset_dicts)} images with keypoints.")


-----------------------------------------------------------------------------------------------------
AND
-----------------------------------------------------------------------------------------------------
# Funktion til at hente verifikationsdata
def my_validation_function():
    dataset_dicts = []
    DATASET_PATH = "Dataprojekt/Data/Clean Data/Overbite Data/Annotated Verication data"

    grouped_annotations = annotations_df.groupby("Filename")

    for idx, filename in enumerate(os.listdir(DATASET_PATH)):
        if filename.endswith((".jpg", ".png", ".jpeg")):
            record = {}
            file_path = os.path.join(DATASET_PATH, filename)
            image = cv2.imread(file_path)
            height, width = image.shape[:2]

            record["file_name"] = file_path
            record["image_id"] = idx
            record["height"] = height
            record["width"] = width
            record["annotations"] = []

            if filename in grouped_annotations.groups:
                keypoints_list = []
                bboxes = []

                for _, row in grouped_annotations.get_group(filename).iterrows():
                    x, y = row["X"], row["Y"]
                    keypoints_list.extend([x, y, 2])

                    # Updated 60x80 bbox centered horizontally on keypoint
                    box_x = max(x - 50, 0)
                    box_y = max(y, 0)
                    box_w = min(100, width - box_x)
                    box_h = min(100, height - box_y)

                    bboxes.append([box_x, box_y, box_w, box_h])

                # One keypoint = one annotation
                for i in range(len(keypoints_list) // 3):
                    annotation = {
                        "bbox": bboxes[i],
                        "bbox_mode": BoxMode.XYWH_ABS,
                        "category_id": 0,
                        "keypoints": keypoints_list[i*3:i*3+3],
                        "num_keypoints": 1
                    }
                    record["annotations"].append(annotation)

            dataset_dicts.append(record)

    return dataset_dicts

# Registrér valideringsdatasæt
DatasetCatalog.register("Overbite_Validation", my_validation_function)
MetadataCatalog.get("Overbite_Validation").set(
    thing_classes=["object"],
    keypoint_names=["keypoint"],
    keypoint_flip_map=[]
)

-----------------------------------------------------------------------------------------------------
AND
-----------------------------------------------------------------------------------------------------
# 🧼 Træls Warning
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

import os
import torch
from detectron2.engine import DefaultTrainer
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.evaluation import COCOEvaluator, inference_on_dataset
from detectron2.data import (
    build_detection_test_loader,
    build_detection_train_loader,
    detection_utils as utils,
    transforms as T,
)
from detectron2.structures import BoxMode
from detectron2.data.datasets import convert_to_coco_json

# ----------------------------------------
# ✅ Custom Augmentation Mapper (Fixed)
# ----------------------------------------
def custom_mapper(dataset_dict):
    dataset_dict = dataset_dict.copy()
    image = utils.read_image(dataset_dict["file_name"], format="BGR")

    aug = [
        T.ResizeShortestEdge(short_edge_length=(640, 720, 768), max_size=1024, sample_style='choice'),
        # This was in your original version and might be critical
        T.RandomFlip(prob=0.5, horizontal=True, vertical=False),
    ]
    image, transforms = T.apply_transform_gens(aug, image)
    image_tensor = torch.as_tensor(image.transpose(2, 0, 1).copy(), dtype=torch.float32)
    dataset_dict["image"] = image_tensor

    annos = [utils.transform_instance_annotations(
        obj, transforms, image.shape[:2],
        keypoint_hflip_indices=[0]  # even though it's sketchy, the original had it
    ) for obj in dataset_dict["annotations"]]

    instances = utils.annotations_to_instances(annos, image.shape[:2])
    dataset_dict["instances"] = instances
    return dataset_dict

# ----------------------------------------
# ✅ Custom Trainer
# ----------------------------------------
class CustomTrainer(DefaultTrainer):
    @classmethod
    def build_evaluator(cls, cfg, dataset_name):
        return COCOEvaluator(dataset_name, cfg, False, output_dir=cfg.OUTPUT_DIR)

    @classmethod
    def build_train_loader(cls, cfg):
        return build_detection_train_loader(cfg, mapper=custom_mapper)

# ----------------------------------------
# ✅ Config Setup
# ----------------------------------------
cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file("COCO-Keypoints/keypoint_rcnn_X_101_32x8d_FPN_3x.yaml"))
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Keypoints/keypoint_rcnn_X_101_32x8d_FPN_3x.yaml")

cfg.DATASETS.TRAIN = ("Overbite_Data",)
cfg.DATASETS.TEST = ("Overbite_Validation",)

cfg.DATALOADER.NUM_WORKERS = 8
cfg.SOLVER.IMS_PER_BATCH = 4  # safer batch size
cfg.SOLVER.BASE_LR = 0.002     # fine-tuning friendly
cfg.SOLVER.MAX_ITER = 100000
cfg.SOLVER.STEPS = (50000, 75000)
cfg.SOLVER.GAMMA = 0.1

# Warmup & Gradient Clipping
cfg.SOLVER.WARMUP_ITERS = 1000
cfg.SOLVER.WARMUP_METHOD = "linear"
cfg.SOLVER.WARMUP_FACTOR = 1.0 / 1000
cfg.SOLVER.WEIGHT_DECAY = 0.0001
cfg.SOLVER.CLIP_GRADIENTS.ENABLED = True
cfg.SOLVER.CLIP_GRADIENTS.CLIP_TYPE = "norm"
cfg.SOLVER.CLIP_GRADIENTS.CLIP_VALUE = 1.0
cfg.SOLVER.CLIP_GRADIENTS.NORM_TYPE = 2.0

# AMP on (now that training is stable)
cfg.SOLVER.AMP.ENABLED = True

# Model Head
cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 256
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1
cfg.MODEL.KEYPOINT_ON = True
cfg.MODEL.ROI_KEYPOINT_HEAD.NUM_KEYPOINTS = 1

# Tight OKS threshold for mm-level precision
cfg.TEST.KEYPOINT_OKS_SIGMAS = [0.01]
cfg.TEST.EVAL_PERIOD = 1000

cfg.OUTPUT_DIR = "./output3/Overbite_Model"
os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)

# ----------------------------------------
# ✅ COCO Conversion (for external validation)
# ----------------------------------------
coco_annotation_path = os.path.join(cfg.OUTPUT_DIR, "Overbite_Validation_coco_format.json")
convert_to_coco_json("Overbite_Validation", coco_annotation_path)
print(f"✅ Validation set converted to COCO format: {coco_annotation_path}")

# ----------------------------------------
# ✅ Train!
# ----------------------------------------
trainer = CustomTrainer(cfg)
trainer.resume_or_load(resume=False)
trainer.train()

# ----------------------------------------
# ✅ Evaluate
# ----------------------------------------
val_loader = build_detection_test_loader(cfg, "Overbite_Validation")
inference_on_dataset(
    trainer.model,
    val_loader,
    COCOEvaluator("Overbite_Validation", cfg, False, output_dir=cfg.OUTPUT_DIR)
)

print("✅ Training and validation completed successfully!")

-----------------------------------------------------------------------------------------------------
AND
-----------------------------------------------------------------------------------------------------

Jeg stopped træning tidligere da validation konvergerede
