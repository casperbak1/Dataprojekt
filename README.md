# Table of contents (GitHub)
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

# Dataprojekt
![Image](https://github.com/user-attachments/assets/b3db6e84-c1ee-460c-910b-0eceaa46817a)

## Indholsfortegnelse

##### Abstract
##### Introduktion
##### Data og databehandling
##### CNN-netværk
##### Resultater
##### Pipeline


## Abstract

## Introduction
Vi har fået til opgave at automatisere processen for overbidsklassificering.\
Som det er lige nu er der i tandlægepraksissen ikke en standardiseret metode, eller automatiseret metode for at undersøge en patients overbid. Nogle praksisser tager den på øjemål, nogle med en lineal, andre et røntenfotografi hvorfra det udregnes og nogle tager 3D scanninger af tænderne, og kan så udregne det derfra.\
Der er altså mange forskellige metoder, som alle har sine fordele og ulemper, nogle er mere præcise, men også mere tidskrævende og vice versa. Hvis man kan standardisere og automatisere denne process, er der altså potentiale for både mere præcise målinger, men også tidsbesparelser.

Vi har i dette projekt haft 2 primære fokusområder:
1. Trænet maskinlæringsmodeller på forskellige måder, for at opnå den mest præcise model.
2. Udarbejdet et "proof of concept" Hvor vi går fra 3D filer af tænderne, til at have markeret hvor man skal måle overbiddet. Dette kan der læses mere om under sektionen "Pipeline". Nedestående figur er en GIF af en 3D model af en overkæbe.
![3D GIF](Data/Brunatest_UpperJawScan.gif)