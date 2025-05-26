# Dataprojekt
![Image](https://github.com/user-attachments/assets/b3db6e84-c1ee-460c-910b-0eceaa46817a)

# Table of contents
## Quick overview:
* "Data" contains the data we initially started out with, CSV files and png files. - Folder primarily used for training and testing models
* "Overbite" This folder contains the code used for training, testing, search refinement and overbite classification along with the outputs
* "Pipeline" This folder "showcases" the workflow, so going from .PLY file to a keypoint placement

## 1. Data - Folder - Contains our data (CSV + PNG)

#### 1.1 Clean Data - Folder - Contains the formatted data
##### 1.1.1 Bolton Data - Folder - Contains images for bolton analysis
##### 1.1.2 Overbite Data - Folder - Contains images for Overbite detection
###### 1.1.2.1 Annotated Data Pairs - Folder - Contains images for training the model
###### 1.1.2.2 Annotated Data Verication Pairs - Folder - Contains images for verification during training
###### 1.1.2.3 Unannotated Data Pairs - Folder - Contains the images without annotations
###### 1.1.2.4 Annotated Data Verication Pairs - Folder - Contains images for testing after training

#### 1.2 Raw Data - Folder - Contains the raw data we started out with
###### 1.2.1 Sample images - Folder - Contains the original images

#### 1.3 Splitting_and_flipping_of_images.ipynb - Jupyter notebook file - This file does our dataprocessing

## 2. Overbite
#### 2.1 Kode - Folder - Contains the code used for training and testing
#### 2.2 Output - Folder - Different outputs from the model (Images, csv files plots)
#### 2.3 Other Versions (Overbite) - Folder - Contains "kode" and "Output" folders, but for different models

## 3. Pipeline
#### 3.1 Pipeline_code - Folder - Contains the .py files used in the pipeline.ipynb file
#### 3.2 Pipeline_data - Folder - Contains the "data" so .PLY files, PNG files and the outputs
#### 3.3 dock - Folder - Contains the "data" so .PLY files, PNG files and the outputs