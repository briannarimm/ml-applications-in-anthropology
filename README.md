# ML Applications in Anthropology

![A herd of cows](assets/images/cows.jpg)

**Online showcase:** <https://www.briannaimm.com/ml-applications-in-anthropology/>

This repository has two small Python projects. Both projects look for patterns in anthropology data. Each project makes an interactive map that you open in a web browser.

* **Domesticated animals map.** The map shows the main farm animal of 118 societies.
* **Clustering demo.** A machine learning method puts 141 societies into 3 groups. The groups are shown on a map and in charts.

You do not need to know machine learning or anthropology to use this repository.

## Contents

1. [Terms](#terms)
2. [Data](#data)
3. [Project 1: Domesticated animals map](#project-1-domesticated-animals-map)
4. [Project 2: Clustering demo](#project-2-clustering-demo)
5. [Install and run](#install-and-run)
6. [Use your own data](#use-your-own-data)
7. [Repository layout](#repository-layout)
8. [Troubleshooting](#troubleshooting)
9. [Credits and license](#credits-and-license)

## Terms

| Term | Meaning |
| --- | --- |
| Society | A group of people that share a culture. Each row in the data is one society |
| Domesticated animal | An animal that people keep and breed, for example a pig or a cow |
| Cluster | A group of societies that are similar to each other |
| Clustering | A machine learning method that finds clusters. It does not use a list of right answers |
| K-Modes | A clustering method for categories, such as "Pigs" or "Bovines" |
| Elbow curve | A chart that helps you choose the number of clusters |
| Otiose god | A god that exists, but does not take part in human affairs |
| Focal year | The year that the data describes |

## Data

Both projects use the same data. The data describes 141 societies from the Standard Cross-Cultural Sample (SCCS). It comes from [D-PLACE](https://d-place.org), a database of cultural data.

Each society has these variables:

| Column | Meaning | Example values |
| --- | --- | --- |
| `domesticated_label` | The main domesticated animal | Pigs, Bovines, Camels, Small Species |
| `roleofgods_label` | The role of the gods | Absent, Otiose, Active (supporting morality) |
| `animalshunted_label` | The animals that people hunt | Large Game, Small Mammals, Birds or Waterfowl |
| `religion_label` | The main religion | Indigenous religion, Islamization, Christianization |
| `focal_year` | The year that the data describes | 1880 |

The [data](data) folder has two files:

* `societies.csv` has the variables of all 141 societies.
* `coordinates.csv` has the latitude and longitude of 118 societies. The coordinates come from [Glottolog](https://glottolog.org).

23 societies have no coordinates. They are in the clustering. They are not on the maps.

## Project 1: Domesticated animals map

The script reads the data and makes one web page. The web page shows a world map. Each society has one animal icon on the map.

| Action | Result |
| --- | --- |
| Move the mouse over an icon | The name of the society shows |
| Click an icon | The focal year, role of the gods, animals hunted and religion show |
| Read the legend (bottom left) | You see which icon shows which animal |

**Script:** [domesticated-animals-map/map.py](domesticated-animals-map/map.py)
**Output:** `domesticated-animals-map/output/animal_map.html`

The script uses these libraries:

* **pandas** reads and joins the data.
* **Folium** draws the map.
* **Branca** draws the legend.

## Project 2: Clustering demo

Clustering puts similar items in the same group. In this project, the items are societies. The script finds groups of societies that have similar animals, gods and religion.

The script uses **K-Modes**. K-Modes is like K-Means, but it works with categories and not with numbers. The center of a group is the most common category of each variable.

**Script:** [clustering-demo/clustering.py](clustering-demo/clustering.py)
**Output:** `clustering-demo/output/`

The script does these steps:

1. It reads the data of 141 societies.
2. It calculates the cost of 1 to 5 groups and draws the elbow curve. A lower cost means a better fit.
3. It makes 3 groups.
4. It adds coordinates to the societies that have them.
5. It draws one count chart for each variable.
6. It makes a map. Each group has a different color.

> **Note:** The elbow curve has no sharp bend. The cost continues to decrease as the number of groups increases. The number 3 is easy to read. It is not a proof.

K-Modes starts at random. The script uses a fixed seed (`SEED = 42`). Each run gives the same result.

### Output files

| File | Content |
| --- | --- |
| `cluster_map.html` | Interactive map of the clusters |
| `elbow_curve.png` | Cost for each number of clusters |
| `clusters.csv` | The cluster of each of the 141 societies |
| `clusters_mapdata.csv` | The same data with coordinates (118 societies) |
| `charts/*_chart.png` | One count chart for each variable |

### Results

The numbers are counts of societies.

| Cluster | Map color | Size | What the cluster has in common |
| --- | --- | --- | --- |
| 1 | Black | 69 | Gods are absent (50). Pigs are the main animal (23 of the 24 pig societies) |
| 2 | Green | 47 | Gods are otiose (27). Small animals are the main animal (31). People hunt two or more kinds of animal (26) |
| 3 | Red | 25 | Gods are active and support morality (22). Deep Islamization is common (14). Bovines (17) and camels (3) are the main animals |

Almost all pig societies are in cluster 1, where the gods are absent. Pigs are a food taboo in Judaism and Islam. The result can support the idea that food taboos relate to the role of the gods.

> **Warning:** Correlation is not causation. Geography and indigenous religions also influence the clusters. Many societies do not follow the pattern of their cluster.

The folder [clustering-demo/published](clustering-demo/published) keeps the charts and the map from the 2021 analysis. That analysis used a different random start. The cluster sizes are a little different. The main pattern is the same.

## Install and run

You need Python 3.9 or later and an internet connection.

1. Clone the repository and go to the folder:

   ```bash
   git clone https://github.com/briannarimm/ml-applications-in-anthropology.git
   cd ml-applications-in-anthropology
   ```

2. Make a virtual environment and install the libraries:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. Run the domesticated animals map:

   ```bash
   python domesticated-animals-map/map.py
   ```

4. Run the clustering demo:

   ```bash
   python clustering-demo/clustering.py
   ```

5. Start a local web server:

   ```bash
   python -m http.server 8000
   ```

6. Open <http://localhost:8000> in a web browser. This page is the same as the online showcase.

> **Note:** The maps load map tiles from the internet. Without a connection, the base map does not show.

> **Note:** Do not move the HTML files. `animal_map.html` links to the icons in `assets/icons` with a relative path.

## Use your own data

1. Open the CSV files in the `data` folder.
2. Change the rows. Keep the column names.
3. Make sure that each society has the same `society_id` in both files.
4. Run the scripts again.

To add an animal, add a line to the `ICONS` dictionary in `map.py`. Put a PNG file in `assets/icons`.

To change the number of clusters, change `N_CLUSTERS` in `clustering.py`.

## Repository layout

```text
data/                       Data of the societies (CSV)
assets/icons/               Animal icons for the map
assets/images/              Header images
domesticated-animals-map/   Project 1: map.py and its output
clustering-demo/            Project 2: clustering.py and its output
  published/                Charts and map from the 2021 analysis
LICENSES/                   Full text of the Creative Commons licenses
index.html                  The online showcase page
requirements.txt            Python libraries
```

## Troubleshooting

| Problem | Cause | Solution |
| --- | --- | --- |
| `ModuleNotFoundError` | The libraries are not installed | Activate the virtual environment. Run `pip install -r requirements.txt` |
| The animal icons do not show | You opened the HTML file from a different folder | Keep the folder layout. Use the local web server |
| The base map is empty | There is no internet connection | Connect to the internet and reload the page |
| The cluster numbers are different | You changed `SEED` or the data | Set `SEED = 42` and use the original data |

## Credits and license

**Author:** Brianna R. Imm

This repository has more than one license:

| What | License |
| --- | --- |
| Source code | [MIT](LICENSE) |
| Text and page design | [CC BY 4.0](LICENSES/CC-BY-4.0.txt) |
| Data and results | [CC BY-NC 4.0](LICENSES/CC-BY-NC-4.0.txt) (non-commercial) |
| Icons and images | Their own licenses |

See [LICENSING.md](LICENSING.md) for details. See [CREDITS.md](CREDITS.md) for data sources, icon authors and software citations.
