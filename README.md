# Dataprojekt
This is our dataproject about detecting overbite and mapping the teeth
![Image](https://github.com/user-attachments/assets/b3db6e84-c1ee-460c-910b-0eceaa46817a)

# Table of contents
## Quick overview:
* "Data" contains the data we initially started out with - Folder primarily used for training and testing models
* "Overbite" This folder contains the code used for training, testing, search refinement and overbite classification
* "Pipeline" This folder "showcases" the workflow, so going from .PLY file to a keypoint placement

## 1. Data - Folder - Contains our data

#### 1.1 Clean Data - Folder - Contains the formatted data
##### 1.1.1 Bolton Data - Folder - Contains images for bolton analysis
##### 1.1.2 Overbite Data - Folder - Contains images for Overbite detection
###### 1.1.2.1 Annotated Data Pairs - Folder - Contains images for training the model
###### 1.1.2.2 Annotated Data Verification Pairs - Folder - Contains images for testing the model
###### 1.1.2.3 Unannotated Data Pairs - Folder - Contains the images without annotations
###### 1.1.2.4 Updated_Labels - CSV file - Contains annotations for the data (After the transformation)

#### 1.2 Raw Data - Folder - Contains the raw data we started out with
###### 1.2.1 Sample images - Folder - Contains the original images
###### 1.2.2 Labels as of 28-02-2025 (FINAL - for now) - CSV file - Contains the annotations for the original image

#### 1.3 Opdeling_og_flip_af_billeder.ipynb - Jupyter notebook file - This file does our datahandling
#### 1.4 Pixel_flip_formel - Image - Image used for visualisation in the Jupyter notebook

## 2. Overbite_Overjet
#### 2.1 Kode - Folder - Contains the code used for training and testing, as well as performance overview
#### 2.2 Pixel matrix - Folder - Contains the code used for fine tuning the model output