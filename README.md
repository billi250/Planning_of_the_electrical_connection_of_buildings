# 📌 Planification du raccordement électrique de bâtiments


---

## 🏙️ Contexte du projet

Une petite ville a été fortement impactée par des intempéries, provoquant la destruction d’une partie des infrastructures nécessaires au raccordement électrique des bâtiments.  
La mairie nous a missionnés pour proposer un **plan de reconstruction du réseau électrique**, avec les objectifs suivants :

- Raccorder le plus grand nombre de citoyens le plus rapidement possible  
- Minimiser les coûts de reconstruction  
- Prioriser les bâtiments critiques, en particulier **l’hôpital**

Toutes les informations nécessaires à la planification sont contenues dans le fichier  
**`reseau_en_arbre.csv / xlsx`**, complété par des données bâtiments et infrastructures.

---

## 🎯 Objectifs du cas d’usage

- Modéliser un réseau électrique sous forme de graphe  
- Évaluer les coûts et les durées de reconstruction  
- Prioriser les bâtiments selon une métrique **coût / nombre de logements**  
- Tirer parti de la mutualisation des infrastructures  
- Garantir la sécurité énergétique de l’hôpital  

---

## 🗂️ Données fournies

### 1. Shapefile des bâtiments
- Localisation géographique  
- Type de bâtiment (hôpital, habitation, etc.)  
- Nombre de maisons raccordées  

### 2. Shapefile des infrastructures électriques
- Type d’infrastructure (aérien, semi-aérien, fourreau)  
- Longueur des lignes  
- État des infrastructures  

### 3. Fichier réseau en arbre (`reseau_en_arbre`)
- Connexions entre bâtiments et infrastructures  
- Informations de coût et de dépendances  

---

## 💰 Hypothèses de coûts

### Coût du matériel (€/m)

| Type d’infrastructure | Coût |
|----------------------|------|
| Aérien | 500 € |
| Semi-aérien | 750 € |
| Fourreau | 900 € |

### Durée de construction (heures / m)

| Type d’infrastructure | Durée |
|----------------------|-------|
| Aérien | 2 h |
| Semi-aérien | 4 h |
| Fourreau | 5 h |

### Main-d’œuvre
- 1 ouvrier = **300 € / jour (8h)**  
- Coût horaire : **37,5 €**  
- Maximum **4 ouvriers par infrastructure**  
- Les ouvriers peuvent se téléporter (pas de temps de déplacement)

---

## 🚑 Contrainte critique : hôpital

- Le générateur de l’hôpital dispose de **44 heures d’autonomie**  
- Une **marge de sécurité de 20 %** est imposée  
- Le temps maximum acceptable est donc **≈ 35 heures**  
- L’hôpital est traité en **priorité absolue (phase 0)**  

---

## 🏗️ Phases de construction

- **Phase 0** : Hôpital  
- **Phase 1** : ~40 % du budget total  
- **Phase 2, 3, 4** : ~20 % du budget chacune  

---

## 🧠 Méthodologie

### 1️⃣ Préparation des données
- Filtrage des infrastructures à remplacer  
- Jointure entre réseau, bâtiments et infrastructures  
- Nettoyage des colonnes inutiles  

### 2️⃣ Modélisation du réseau
- Les bâtiments sont considérés comme des **nœuds**  
- Les infrastructures comme des **arêtes**  
- Chaque arête possède un **coût** et une **durée**  

### 3️⃣ Calcul des coûts globaux
- Coût = matériel + main-d’œuvre  
- Agrégation par infrastructure unique (pas de surcomptage)  

### 4️⃣ Priorisation des bâtiments

Métrique utilisée :

```text
score = nombre_de_maisons / coût_total
➡️ **Plus le score est élevé, plus le bâtiment est prioritaire**  
➡️ **L’hôpital est toujours placé en premier**

---

## 5️⃣ Planification finale

### Classement des bâtiments par priorité
- Estimation du coût et du temps par bâtiment
- Export des résultats en CSV

---

## 🗺️ Intégration SIG et visualisation

- Les shapefiles sont intégrés dans **QGIS**
- Une visualisation cartographique des phases de construction a été réalisée

### Des captures d’écran illustrent :
- Les infrastructures à reconstruire
- Les priorités de raccordement
- Les différentes phases du projet

---

## 📁 Structure du projet

```text
Planning_of_the_electrical_connection_of_buildings
├── main.py
├── config.py
├── infra.py
├── building.py
├── data/
│   └── reseau_en_arbre.xlsx
├── new_data/
│   ├── batiments.csv
│   └── infra.csv
└── README.md
# 🧩 Description du code

## `main.py`
Point d’entrée du programme :

- Préparation des données  
- Calcul des coûts et durées  
- Priorisation des bâtiments  
- Export des résultats  

## `config.py`
Centralise tous les paramètres :

- Coûts  
- Durées  
- Contraintes de main-d’œuvre  

## `infra.py`
**Classe `Infra`** :  
Calcule automatiquement :  

- Le coût d’une infrastructure  
- La durée de reconstruction  

## `building.py`
**Classe `Building`** :  
Agrège les infrastructures et calcule :  

- Le coût total  
- La durée totale  
- La métrique de priorité  

---

# 📤 Fichiers de sortie

- **`reseau_priorise.csv`** → Réseau filtré et prêt à être reconstruit  
- **`batiments_priorises.csv`** → Classement final des bâtiments avec :  
  - Rang de priorité  
  - Coût total  
  - Durée totale  
  - Nombre de maisons  

---

# ✅ Résultats clés

- L’hôpital est traité en priorité et respecte la contrainte temporelle  
- Les bâtiments les plus rentables (coût faible / logements élevés) sont favorisés  
- La mutualisation des infrastructures permet une réduction globale des coûts  
- La planification respecte les phases budgétaires imposées



---

# 📌 Planning the Electrical Connection of Buildings

---

## 🏙️ Project Context

A small town was heavily impacted by severe weather, causing the destruction of part of the infrastructures necessary for connecting buildings to the electrical network.  
The city council commissioned us to propose a **reconstruction plan for the electrical network**, with the following objectives:

- Connect as many citizens as possible, as quickly as possible  
- Minimize reconstruction costs  
- Prioritize critical buildings, especially **the hospital**

All the information needed for planning is contained in the file  
**`reseau_en_arbre.csv / xlsx`**, complemented by building and infrastructure data.

---

## 🎯 Use Case Objectives

- Model an electrical network as a graph  
- Evaluate reconstruction costs and durations  
- Prioritize buildings using a **cost / number of housing units** metric  
- Leverage infrastructure sharing  
- Ensure energy security for the hospital  

---

## 🗂️ Provided Data

### 1. Buildings Shapefile
- Geographic location  
- Building type (hospital, residential, etc.)  
- Number of connected houses  

### 2. Electrical Infrastructure Shapefile
- Infrastructure type (overhead, semi-overhead, duct)  
- Line lengths  
- Infrastructure condition  

### 3. Tree Network File (`reseau_en_arbre`)
- Connections between buildings and infrastructures  
- Cost and dependency information  

---

## 💰 Cost Assumptions

### Material Cost (€/m)

| Infrastructure Type | Cost |
|--------------------|------|
| Overhead           | €500 |
| Semi-overhead      | €750 |
| Duct               | €900 |

### Construction Duration (hours / m)

| Infrastructure Type | Duration |
|--------------------|----------|
| Overhead           | 2 h      |
| Semi-overhead      | 4 h      |
| Duct               | 5 h      |

### Labor
- 1 worker = **€300 / day (8h)**  
- Hourly rate: **€37.5**  
- Maximum **4 workers per infrastructure**  
- Workers can teleport (no travel time)  

---

## 🚑 Critical Constraint: Hospital

- The hospital generator has **44 hours of autonomy**  
- A **20% safety margin** is imposed  
- Maximum acceptable time ≈ **35 hours**  
- The hospital is treated with **absolute priority (phase 0)**  

---

## 🏗️ Construction Phases

- **Phase 0**: Hospital  
- **Phase 1**: ~40% of total budget  
- **Phases 2, 3, 4**: ~20% of budget each  

---

## 🧠 Methodology

### 1️⃣ Data Preparation
- Filter infrastructures to be replaced  
- Join network, building, and infrastructure data  
- Clean unnecessary columns  

### 2️⃣ Network Modeling
- Buildings are considered **nodes**  
- Infrastructures are **edges**  
- Each edge has a **cost** and **duration**  

### 3️⃣ Global Cost Calculation
- Cost = material + labor  
- Aggregation by unique infrastructure (no double counting)  

### 4️⃣ Building Prioritization

Metric used:

```text
score = number_of_houses / total_cost
➡️ **The higher the score, the higher the building's priority**  
➡️ **The hospital is always placed first**
## 5️⃣ Final Planning

### Building Priority Ranking
- Estimate cost and time per building  
- Export results to CSV  

---

## 🗺️ GIS Integration and Visualization
- Shapefiles are integrated in **QGIS**  
- A cartographic visualization of construction phases has been created  

### Screenshots illustrate:
- Infrastructures to be rebuilt  
- Connection priorities  
- Different project phases  

---

## 📁 Project Structure

```text
Planning_of_the_electrical_connection_of_buildings
├── main.py
├── config.py
├── infra.py
├── building.py
├── data/
│   └── reseau_en_arbre.xlsx
├── new_data/
│   ├── buildings.csv
│   └── infra.csv
└── README.md
# 🧩 Code Description

## `main.py`
**Program entry point**:

- Data preparation  
- Cost and duration calculation  
- Building prioritization  
- Export of results  

## `config.py`
**Centralizes all parameters**:

- Costs  
- Durations  
- Labor constraints  

## `infra.py`
**Class `Infra`**:  
Automatically calculates:

- Infrastructure cost  
- Reconstruction duration  

## `building.py`
**Class `Building`**:  
Aggregates infrastructures and calculates:

- Total cost  
- Total duration  
- Priority metric  

---

# 📤 Output Files

- **`reseau_priorise.csv`** → Filtered network ready for reconstruction  
- **`batiments_priorises.csv`** → Final building ranking with:  
  - Priority rank  
  - Total cost  
  - Total duration  
  - Number of houses  

---

# ✅ Key Results

- The hospital is treated with priority and meets the time constraint  
- The most cost-effective buildings (low cost / high housing units) are favored  
- Infrastructure sharing allows overall cost reduction  
- Planning respects the imposed budget phases
