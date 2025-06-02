# Overbidsklassificering — Automatisering og standardisering  
*Et maskinlæringsprojekt til klassificering af overbid ud fra 3D-scanninger og billeder.*

---

## Table of Contents

- [Hurtigt Overblik](#hurtigt-overblik)
- [Projektbeskrivelse](#projektbeskrivelse)
  - [Abstract](#abstract)
  - [Introduktion](#introduktion)
  - [Data og Databehandling](#data-og-databehandling)
    - [Databehandling](#databehandling)
    - [Data](#data)
  - [CNN-netværk](#cnn-netværk)
  - [Evalueringsmetoder](#evalueringsmetoder)
  - [Resultater](#resultater)
  - [Pipeline](#pipeline)
- [Folder Structure](#folder-structure)
---

## Hurtigt Overblik Filstruktur

- **Data:** Indeholder alle rå og forarbejdede CSV- og PNG-filer, primært brugt til træning og test.
- **Overbite:** Indeholder kode, scripts, outputs og forskellige versioner brugt til overbite-klassificering.
- **Pipeline:** Viser hele workflowet fra 3D .PLY-fil til keypoint-placering.

---

## Mappe struktur

Dataprojekt/
├── .gitignore
├── Model.txt
├── README.md
│
├── Data/
│ ├── pixel_flip_formula.png
│ ├── Splitting_and_flipping_of_images.ipynb
│ ├── Clean Data/
│ │ ├── Bolton Data/
│ │ │ └── Example_lower_middle.png
│ │ └── Overbite Data/
│ │ ├── Updated_Labels.csv
│ │ ├── Annotated Data Pairs/
│ │ │ └── Example_lower_left.png
│ │ ├── Annotated Test data/
│ │ │ └── Example_lower_left.png
│ │ ├── Annotated Verication data/
│ │ │ └── Example_lower_left.png
│ │ └── Unannotated Data Pairs/
│ │ └── Example_lower_left.png
│ ├── Figurer/
│ └── Raw Data/
│ ├── 2024-04-08 Test data for overbite classification.xlsx
│ ├── 2025-05-08 TRANSLATE_KEY(1).xlsx
│ ├── Definitions of columns.docx
│ ├── Labels as of 19-02-2025 (Sample images).csv
│ ├── Labels as of 28-02-2025 (FINAL - for now).csv
│ └── Sample images/
│ └── Example_lower_combined.png
│
├── Overbite/
│ ├── Kode/
│ │ ├── Overbite.ipynb
│ │ ├── Pixel_Matrix_Optimizer.ipynb
│ │ ├── Test_Model.ipynb
│ │ └── Train_Model.ipynb
│ ├── Other Versions (Overbite)/
│ │ ├── Kode/
│ │ └── Output/
│ │ ├── Modeller/
│ │ ├── Overbite Detection/
│ │ └── Pixel Matrix/
│ └── Output/
│ ├── Keypoint Placement/
│ │ └── KP_Placement.csv
│ ├── Modeller/
│ │ └── Model.txt
│ ├── Overbite Detection/
│ │ ├── All_FALSE_Classification_Rows.csv
│ │ ├── Overbite_Classification9.csv
│ │ └── Results.ipynb
│ └── Pixel Matrix/
│ ├── KP_Refinement.csv
│ ├── KP_Refinement_Distance.csv
│ └── Image Output/
│ └── Example_lower_left.html
│
├── Pipeline/
│ ├── pipeline.ipynb
│ ├── README.txt
│ ├── docker_detectron2_env/
│ │ └── Dockerfile_pytorch3d_jupyter
│ ├── output/
│ │ └── Overbite_Model/
│ ├── Pipeline_code/
│ │ ├── Opdeling_og_flip_af_billeder.py
│ │ ├── Overbite.py
│ │ ├── Pixelmatrix.py
│ │ ├── Ply_To_Image.py
│ │ └── Run_model.py
│ └── Pipeline_data/
│ ├── patient_level_summary4.csv
│ ├── Predicted_keypoints.csv
│ ├── Clean Data/
│ │ └── Overbite Data/
│ │ └── Info.txt
│ ├── Model/
│ │ ├── Info.txt
│ │ └── Model.txt
│ ├── Output_after_pixel_matrix/
│ │ └── Info.txt
│ ├── Ply Files/
│ │ ├── Brunatest LowerJawScan.ply
│ │ ├── Brunatest_UpperJawScan.ply
│ │ └── Info.txt
│ └── Raw_data/
│ ├── Brunatest LowerJawScan_0.png
│ ├── Brunatest LowerJawScan_1.png
│ ├── Brunatest_UpperJawScan_0.png
│ ├── Brunatest_UpperJawScan_1.png
│ └── Info.txt
                    
---

# Projektbeskrivelse

## Indholdsfortegnelse

- Abstract
- Introduktion
- Data og databehandling
- CNN-netværk
- Resultater
- Pipeline

---

## Abstract

*Automatisering og standardisering af overbidsklassificering gennem maskinlæring og billedbehandling.*

---

## Introduktion

I tandlægepraksis findes der ikke én standardiseret metode til måling af overbid. Nogle anvender øjemål, andre lineal, røntgenbilleder eller 3D-scanninger. Alle metoder har fordele og ulemper, men ofte er der en afvejning mellem præcision og tidsforbrug.

**Dette projekt har to hovedfokusområder:**

1. Udvikling og træning af maskinlæringsmodeller til præcis overbidsklassificering.
2. Udarbejdelse af en pipeline, der går fra 3D-filer (.PLY) til keypoint-markering, der muliggør automatisk måling.

**Bemærk:** Resten af denne projektbeskrivelse omhandler kun punkt 1. Pipeline beskrives separat i sektionen "Pipeline".

---

## Data og Databehandling

### Databehandling

Projektet startede med **1351 kombinerede billeder** (3 vinkler pr. patient):

<img src="Data/Figurer/00OMSZGW_lower_combined.png" width="800" height="250"/>

> *Billede af underkæbe fra 3 vinkler*

Til billederne var der **1166 annoteringer**, eksempelvis:

| Filename                       | X1  | Y1  | X2   | Y2  |
|---------------------------------|-----|-----|------|-----|
| 00OMSZGW_lower_combined.png     | 777 | 492 | 2310 | 487 |

#### Mål for databehandling:

1. Split kombinerede billeder til tre separate billeder (left, middle, right)
2. Fordel billeder i mapper: **Bolton Data** og **Overbite Data**
3. Ensret orientering og koordinationer i "Overbite Data" (ved transponering)
4. Gruppér data som billed-par
5. Del data i træning, test, verifikation, og uannoteret data

#### Step 1: Opdeling af billeder

<table>
  <tr>
    <td><img src="Data/Figurer/Lower_Right.png" width="250" height="250"/></td>
    <td><img src="Data/Figurer/Lower_Middle.png" width="250" height="250"/></td>
    <td><img src="Data/Figurer/Lower_Left.png" width="250" height="250"/></td>
  </tr>
</table>


#### Step 2: Sortering

- **Left/Right** billeder → *Overbite Data*
- **Middle** billede → *Bolton Data*

#### Step 3: Ensretning

"Right" billedet transponeres (flippes), så orienteringen matcher "Left" billedet, og koordinater justeres:\

<table>
  <tr>
    <td><img src="Data/Figurer/Lower_Right.png" width="400" height="400"/></td>
    <td><img src="Data/Figurer/Lower_Left_Flipped.png" width="400" height="400"/></td>
  </tr>
</table>

> Keypoint/Annoteringen er markeret med rød på de 2 billeder

Koordinatet justeres så med følgende formel:
`x' = w - 1 - x`\
Her er `x = X2 = 2310` fra originalen, w = 3072 fra originalen, og derfor er det nye x beregnet til:\
`x' = 3072 - 1 - 2310 = 761`

Og den nye CSV vil derfor blive til:

| Filename                   | X1  | Y1  |
|----------------------------|-----|-----|
| 00OMSZGW_lower_left.png   | 777 | 492 |
| 00OMSZGW_lower_right.png    | 761 | 487 |


#### Step 4 + 5: Par og grupper

- Et *par* = 4 billeder med koordinater (left/right, upper/lower)
- Ufuldstændige par → *Unannotated Data Pairs*
- Resten inddeles i:
    - *Annotated Data Pairs* (træning)
    - *Annotated Verication data* (verifikation under træning)
    - *Annotated Test data* (test efter træning)

> Outliers og fejl rettes i CSV efter databehandling.  
> Alt databehandling findes i `Splitting_and_flipping_of_images.ipynb`.

---

### Data

Oversigt over fordelingen af billeder:

| Folder                               | Image count | Patient count | Annotated |
|---------------------------------------|-------------|-------------|-------------|
| Bolton Data                          | 1351        | 675 | No |
| Overbite Data                        | 2702        | 675 | NaN |
| Overbite Data/Annotated Data Pairs   | 1580        | 395 | Yes |
| Overbite Data/Annotated Verication data | 100      | 25 | Yes |
| Overbite Data/Annotated Test data    | 300         | 75 | Yes |
| Overbite Data/Unannotated Data Pairs | 722         | 180 | NaN|

Dataen er nu klargjort til at træne og teste en maskinlæringsmodel.

---

## CNN-netværk

Vi trænede vores model ved at benytte os af en forudtrænet model fra Detectron2.\
Den model vi har anvendt hedder "keypoint_rcnn_X_101_32x8d_FPN_3x".\
Modellen er altså en Keypoint R-CNN model hvor X_101_32x8d_FPN er selve backbone-arkitekturen:\
X_101_32x8d betyder ResNeXt-101 (101 lag) med 32 grupper og en bredde på 8 per gruppe\
FPN står for Feature Pyramid Network, hvilket betyder, at modellen bruger flere “feature-maps” på forskellige skalaer\

Den grundlæggende måde vores træning har kørt på er:

Vi starter med billeder af størrelsen 1024x1024 som hver har et ground truth keypoint.
Det næste der sker er at billederne bliver augmenteret på forskellige måder, f.eks. med andre billedstørrelser, spejlinger, lys- og kontrastjusteringer så modellen ikke kun lærer et specifikt udseende. Annoteringerne følger selvfølgelig med spejlinger osv.
Denne augmentering er med til at gøre modellen mere robust.

Det næste der sker er at vi indlæser billederne i batches.
Dette gør vi fordi at havde vi kun taget et billede af gangen, havde vi fået langsommere træning og en mere ustabil træning.
Når vi træner modellen med en batch str. på 16, så vil modellens vægte blive opdateret på gennemsnittet af fejlen for hele batchen. Havde vi nu kun brugt 1 billede af gangen, så ville modellens vægte blive opdateret på baggrund af fejlen for dette ene billede og havde billedet nu været en outlier, så ville modellens vægte altså blive opdateret i retning af en outlier.

Efter augmentering og batch indlæsning kommer vi til ResNeXt-101, dette er selve CNN delen.
Her har vi 101 lag, som hver laver en convulution.
Hver enkelt convulution bliver så indelt i 32 grupper.
De 32 grupper finder så mønstre.
Efter ResNeXt-101 ender vi op med en masse "Feature maps" hvor hver pixel svarer til styrken af et bestemt mønster i billedet.

Nu har vi en masse feature maps og det er her FPN kommer ind i billedet.
FPN samler feature maps fra alle de forskellige lag.
De tidligste lag finder de helt små mønstre, og de sene lag finder helhedderne.

Vi er nu ankommet til RPN (Region Proposal Network).
RPN foreslår tusindvis af små bokse med forskellige størrelser og former alle  de steder, hvor der kan være noget spændende.
For hver enkelt af disse bokse scorer RPN, hvor sandsynligt det er, at boksen indeholder et objekt. De bedste forslag går videre til næste skridt.

Vi er nu ved at være ved vejs ende.
For hver af de vidersendte forslag fra RPN skaber modellen et heatmap hvor hver pixel viser sandsynligheden for at vores keypoint ligger der.
Sandsynlighederne laves med en softmax-funktion, så de summer til 1.
Så tager modellen den pixel på heatmappet, hvor sandsynligheden er højest, da det er modellens bedste bud på keypointets placering.

Til sidst er der loss, backpropagation og optimering.
Efter modellen har givet sit bedste bud på hvor keypointet skal placeres, så beregnes det hvor galt den tog fejl, med en cross-entropy loss mellem predicted og ground truth.
Efter det sker der backpropagation;
Den starter med fejlen og regner, hvor meget hver vægt i netværket har påvirket fejlen, dette sker lag-for-lag bagud gennem hele netværket med kædereglen for differenciering.
Vægtene justeres en smule, så fejlen bliver mindre næste gang.
Det her gentager vi for hver batch indtil modellen er konvergeret.

---



## Evalueringsmetoder

Til evaluering af modellen har vi benyttet os af tre metoder:

1. **Mean radial error (MRE)**
2. **Succesful detection rate (SDR)**
3. **Weighted Cohen’s kappa**

De er defineret som følger:

**Mean radial error**:

$$
MRE = \frac{\sum_{i=1}^N R_i}{N}
$$

Her er \$N\$ antallet af predikterede punkter, og \$R\_i\$ er den euklidiske afstand mellem ground truth og modellens punkt.

MRE giver os indsigt i, hvor tæt modellens forudsigelser i gennemsnit ligger på det korrekte punkt (ground truth). Jo lavere MRE, desto mere præcis er modellens gennemsnitlige punktplacering.

**Succesful detection rate**:

$$
SDR = \frac{K}{N} \cdot 100
$$

Her er \$N\$ antallet af predikterede punkter, og \$K\$ er antallet af korrekt placerede punkter indenfor et tilladt "fejl"-interval. Vi har brugt intervaller, der tillader 0.5, 1 og 2 mm afstand i forhold til ground truth.

SDR viser, hvor stor en andel af modellens forudsigelser der ligger indenfor et givent toleranceniveau fra ground truth (fx 0.5, 1 eller 2 mm). Det er særligt nyttigt, hvis man vil vide, hvor ofte modellen rammer “tilstrækkeligt tæt” på det korrekte punkt, givet at man accepterer en vis fejlmargin.

**Weighted Cohen’s kappa** (\$\kappa\_w\$) bruges til at måle, hvor god overensstemmelse der er mellem modellens klassifikation og den sande (ekspert-annoterede) klasse, hvor tilfældig overensstemmelse er korrigeret for:

$$
\kappa_w = 1 - \frac{\sum_{i,j} w_{i,j} O_{i,j}}{\sum_{i,j} w_{i,j} E_{i,j}}
$$

Her er \$O\_{i,j}\$ andelen af tilfælde, hvor ground truth er klasse \$i\$ og modellen valgte klasse \$j\$, og \$E\_{i,j}\$ er den forventede andel af sådanne tilfælde, hvis annotatorerne var uafhængige.

Vægtene \$w\_{i,j}\$ bruges til at straffe større fejl hårdere. Ved **kvadratisk vægtning** (“quadratic weights”) beregnes vægten som:

$$
w_{i,j} = \left( \frac{i - j}{k - 1} \right)^2
$$

hvor \$k\$ er antallet af klasser (her 5 for “A”–“E”).

Det vil sige, at hvis modellen forveksler “A” og “E”, tæller det som en større fejl end hvis den forveksler “A” og “B”.

---

## Resultater 



## Pipeline
Som den sidste del af projektet har vi udviklet en pipeline, der tager to PLY-filer — én for overkæben og én for underkæben — som input. Pipelinen giver som output en visuel forudsigelse af det samlede tandsæt samt en klassifikation af overbid.

Den første version af pipelinen byggede på kode, som vores vejleder havde stillet til rådighed, oprindeligt udviklet af en postdoc. Denne kode accepterede én enkelt PLY-fil og genererede to billeder: ét, der viste tænderne fra venstre side, og ét fra højre side.

Vi udvidede og ændrede koden, så den nu tager to PLY-filer (over- og underkæbe) som input. Vores tilføjelser omfatter:

• Justering og ensretning af billederne

• Kørsel af modellen til overbidsklassifikation

• Fremstilling af et endeligt output, der viser både de forudsagte keypoints og klassifikationsresultatet

På nuværende tidspunkt kan vi ikke evaluere pipelinens ydeevne på virkelige eksempler. For at pipelinen kan give nøjagtige forudsigelser, skal både over- og underkæbemodellerne være i samme koordinatsystem. Denne justering findes dog ikke i de PLY-filer, vi har til rådighed.
