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
  - [Pixel-matrix](#pixel-matrix)
  - [Evalueringsmetoder](#evalueringsmetoder)
  - [Resultater](#resultater)
  - [Pipeline](#pipeline)
- [Folder Structure](#folder-structure)
---

## Hurtigt Overblik over filstruktur

- **Data:** Indeholder alle rå og forarbejdede CSV- og PNG-filer, primært brugt til træning og test.
- **Overbite:** Indeholder kode, scripts, outputs og forskellige versioner brugt til overbite-klassificering.
- **Pipeline:** Viser hele workflowet fra 3D .PLY-fil til keypoint-placering.

---

## Mappe struktur
<details open>
  <summary>📁 Dataprojekt/</summary>
  <ul>
    <li>📄 .gitignore</li>
    <li>📄 Model.txt</li>
    <li>📄 README.md</li>
    <li>
      <details>
        <summary>📁 Data/</summary>
        <ul>
          <li>📄 pixel_flip_formula.png</li>
          <li>📄 Splitting_and_flipping_of_images.ipynb</li>
        </ul>
      </details>
    </li>
    <li>
      <details>
        <summary>📁 Overbite/</summary>
        <ul>
          <li>
            <details>
              <summary>📁 Kode/</summary>
              <ul>
                <li>📄 Overbite.ipynb</li>
                <li>📄 Pixel_Matrix_Optimizer.ipynb</li>
                <li>📄 Test_Model.ipynb</li>
                <li>📄 Train_Model.ipynb</li>
              </ul>
            </details>
          </li>
        </ul>
      </details>
    </li>
  </ul>
</details>


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

Projektet bygger på et offentligt datasæt bestående af 1.351 tredimensionelle intraorale scanninger. Til dette projekt er 3D-scanningerne konverteret til todimensionelle billeder, hvilket gør det muligt at anvende gængse deep-learning-metoder til billedanalyse. 

Som model anvender vi Keypoint R-CNN, en videreudvikling af Mask R-CNN, der er designet til at finde præcise keypoints i billeder. Ved at kombinere regions­forslag med punktdetektion gør modellen det muligt at identificere nøjagtige punkter på tænder, hvilket er afgørende for vores opgave, da overbid måles som den vertikale afstand mellem to præcise punkter på fortænderne.

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

Oversigt over fordelingen af billeder:

| Folder                               | Image count | Patient count | Annotated |
|---------------------------------------|-------------|-------------|-------------|
| Bolton Data                          | 1351        | 675 | No |
| Overbite Data                        | 2702        | 675 | NaN |
| Overbite Data/Annotated Data Pairs   | 1580        | 395 | Yes |
| Overbite Data/Annotated Verication data | 100      | 25 | Yes |
| Overbite Data/Annotated Test data    | 300         | 75 | Yes |
| Overbite Data/Unannotated Data Pairs | 722         | 180 | NaN|

Efter dataen er opdelt i mapper mangler vi kun 2 ting inden træningen kan påbegynde:

1. Opsætte en bounding boks
2. Konvertere annoteringer til "COCO JSON" format

Vi opsætter en bounding boks for at hjælpe med at lokalisere objektet af interesse. Det hjælper modellen med at finde det område den skal fokusere på, for at lave forudsigelser. Dette gør modellen mere præcis og effektiv.

Annoteringerne skal til sidst konverteres til et format som kan læses af modellen.

Modellen modtager altså som input til træning 1580 billeder af følgende format:

<img src="Data/Figurer/Data_For_Training.png" width="600" height="600"/>

> *Keypoint markeret med rød, og bounding box markeret med grå*

Og annoteringen:

```json
{
  "images": [
    {
      "file_name": "Dataprojekt/Data/Clean Data/Overbite Data/Annotated Data Pairs/00OMSZGW_lower_left.png",
      "height": 1024,
      "width": 1024,
      "id": 0
    }
  ],
  "annotations": [
    {
      "bbox": [740, 492, 62, 125],
      "bbox_mode": 1,
      "category_id": 0,
      "keypoints": [777, 492, 2],
      "num_keypoints": 1,
      "image_id": 0,
      "id": 0
    }
  ],
  "categories": [
    {
      "id": 0,
      "name": "tooth",
      "keypoints": ["apex"],
      "skeleton": []
    }
  ]
}
```

Modellen er altså nu klar til at blive trænet.


---

## Keypoints R-CNN-netværk

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

## Pixel-matrix

Efter modellen har placeret keypoints på billederne, finjusteres disse positioner ved hjælp af pixelsøgning. Dette sker ved at definere en matrix (af forudbestemt størrelse) omkring det keypoint, som modellen har forudsagt. Inden for denne matrix identificeres den pixel, der ligger højest og er lysest, og denne pixel vælges herefter som det nye, justerede keypoint. Hvis der findes to pixels med samme værdi, bliver den pixel, der ligger længst til venstre, valgt. Dette valg bygger på hvordan det sande keypoint bliver annoteret. 
Formålet med denne proces er at sikre, at keypointet placeres så præcist som muligt ud fra det forudsagte keypoint fra modellen, hvilket forbedrer den samlede nøjagtighed og robusthed af keypoint placeringen.

Figuren viser fordelingen af fejl for placeringen af keypoints efter pixelsøgningen er implementeret.

<img src="Data/Figurer/Histogram_efter_pixelmatrix.png" width="900" height="400"/> 

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
### Detection Metrics (gælder for alle tests)

| SDR (≤ 0.5 mm) | SDR (≤ 1 mm) | SDR (≤ 2 mm) | Mean Radial Error (MRE) |
|----------------|--------------|--------------|--------------------------|
| 89.33 %        | 96.00 %      | 99.00 %      | 0.22 mm                  |

### Test Results

| Summary Name                | Classification Accuracy | Weighted Cohen's Kappa | Patients Total | Patients Excluded |
|----------------------------|--------------------------|------------------------|----------------|-------------------|
| Overbite_Classification1.csv | 97.22 %                 | 0.9927                 | 75             | 3                 |
| Overbite_Classification2.csv | 94.44 %                 | 0.9841                 | 75             | 3                 |
| Overbite_Classification3.csv | 95.89 %                 | 0.9906                 | 75             | 2                 |
| Overbite_Classification4.csv | 95.83 %                 | 0.9906                 | 75             | 3                 |
| Overbite_Classification5.csv | 94.59 %                 | 0.9860                 | 75             | 1                 |
| Overbite_Classification6.csv | 94.59 %                 | 0.9875                 | 75             | 1                 |
| Overbite_Classification7.csv | 95.89 %                 | 0.9894                 | 75             | 2                 |
| Overbite_Classification8.csv | 94.52 %                 | 0.9882                 | 75             | 2                 |
| Overbite_Classification9.csv | 97.30 %                 | 0.9935                 | 75             | 1                 |
| Overbite_Classification10.csv| 93.15 %                 | 0.9836                 | 75             | 2                 |


## Pipeline
Som den sidste del af projektet har vi udviklet en pipeline, der tager to PLY-filer — én for overkæben og én for underkæben — som input. Pipelinen giver som output en visuel forudsigelse af det samlede tandsæt samt en klassifikation af overbid.

Den første version af pipelinen byggede på kode, som vores vejleder havde stillet til rådighed, oprindeligt udviklet af en postdoc. Denne kode accepterede én enkelt PLY-fil og genererede to billeder: ét, der viste tænderne fra venstre side, og ét fra højre side.

Vi udvidede og ændrede koden, så den nu tager to PLY-filer (over- og underkæbe) som input. Vores tilføjelser omfatter:

• Justering og ensretning af billederne

• Kørsel af modellen til overbidsklassifikation

• Fremstilling af et endeligt output, der viser både de forudsagte keypoints og klassifikationsresultatet

På nuværende tidspunkt kan vi ikke evaluere pipelinens ydeevne på virkelige eksempler. For at pipelinen kan give nøjagtige forudsigelser, skal både over- og underkæbemodellerne være i samme koordinatsystem. Denne justering findes dog ikke i de PLY-filer, vi har til rådighed.


## Referencer 

Ben-Hamadou, Achraf, Neifar, Nour, Rekik, Ahmed, Smaoui, Oussama, Bouzguenda, Firas, Pujades, Sergi, Boyer, Edmond, and Ladroit, Edouard. "Teeth3Ds+: An Extended Benchmark for Intra-oral 3D Scans Analysis." arXiv preprint arXiv:2210.06094 (2022). https://arxiv.org/abs/2210.06094

