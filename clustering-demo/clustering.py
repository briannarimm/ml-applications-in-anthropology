"""Group societies with the K-Modes clustering algorithm, then chart and map the groups.

K-Modes is like K-Means, but it works on categorical data.
It uses the most frequent category (the mode) as the center of a cluster.

Input:  data/societies.csv and data/coordinates.csv (repository root)
Output: clustering-demo/output/
          elbow_curve.png         cost for each number of clusters
          clusters.csv            the cluster of each society
          clusters_mapdata.csv    same, with coordinates (societies with coordinates only)
          charts/*_chart.png        one count chart per variable
          cluster_map.html        interactive map of the clusters
"""
from pathlib import Path

import branca
import folium
import matplotlib

matplotlib.use("Agg")  # draw to files, not to a window
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from kmodes.kmodes import KModes

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "output"

FEATURES = ["roleofgods_label", "religion_label", "domesticated_label", "animalshunted_label"]
N_CLUSTERS = 3
MAX_K = 5  # the elbow curve tests 1 to MAX_K clusters
SEED = 42  # K-Modes starts at random. A fixed seed gives the same result each time.
COLORS = {0: "black", 1: "green", 2: "red"}  # map color of each cluster


def fit(data: pd.DataFrame, k: int) -> KModes:
    model = KModes(n_clusters=k, init="random", n_init=20, random_state=SEED)
    model.fit(data)
    return model


def plot_elbow(data: pd.DataFrame) -> None:
    ks = list(range(1, MAX_K + 1))
    costs = [fit(data, k).cost_ for k in ks]
    plt.figure(figsize=(6, 4))
    plt.plot(ks, costs, "bx-")
    plt.xlabel("Number of clusters")
    plt.ylabel("Cost")
    plt.title("Elbow method for the best number of clusters")
    plt.xticks(ks)
    plt.tight_layout()
    plt.savefig(OUTPUT / "elbow_curve.png", dpi=120)
    plt.close()
    print("Cost per number of clusters:", dict(zip(ks, (round(c) for c in costs))))


def cluster_societies(societies: pd.DataFrame) -> pd.DataFrame:
    data = societies.set_index("society_name")[FEATURES]
    model = fit(data, N_CLUSTERS)
    # K-Modes numbers the clusters at random. Number them by size, largest first.
    sizes = pd.Series(model.labels_).value_counts()
    renumber = {old: new for new, old in enumerate(sizes.index)}
    result = societies.copy()
    result["Cluster"] = [renumber[label] for label in model.labels_]
    print("Cluster sizes:", result["Cluster"].value_counts().sort_index().to_dict())
    return result


def make_charts(data: pd.DataFrame) -> None:
    charts = OUTPUT / "charts"
    charts.mkdir(exist_ok=True)
    for column in ["Cluster"] + FEATURES:
        plt.figure(figsize=(15, 5))
        sns.countplot(x="Cluster", hue=column, data=data)
        plt.tight_layout()
        name = "cluster_sizes" if column == "Cluster" else column.replace("_label", "")
        plt.savefig(charts / f"{name}_chart.png", dpi=100)
        plt.close()


def make_map(data: pd.DataFrame) -> None:
    world = folium.Map(location=[10, 0], tiles="OpenStreetMap", zoom_start=2)
    for row in data.itertuples():
        popup = (
            f"Cluster: {row.Cluster + 1}"
            f"<br />Religion: {row.religion_label}"
            f"<br />Primary Domesticated Animal: {row.domesticated_label}"
            f"<br />Role of God(s): {row.roleofgods_label}"
            f"<br />Animals Hunted: {row.animalshunted_label}"
        )
        color = COLORS[row.Cluster]
        folium.CircleMarker(
            (row.latitude, row.longitude),
            radius=6, weight=1, color=color, fill_color=color, fill_opacity=0.9,
            popup=folium.Popup(popup, min_width=250, max_width=250),
            tooltip=row.society_name,
        ).add_to(world)

    rows = "\n".join(
        f'    <p><span style="color:{color};font-size:30px">&#9679;</span>&emsp;Cluster {n + 1}</p>'
        for n, color in COLORS.items()
    )
    html = (
        "{% macro html(this, kwargs) %}\n"
        '<div style="position: fixed; bottom: 30px; left: 30px; z-index: 9999; font-size: 14px;'
        ' background-color: rgba(255,255,255,0.85); padding: 4px 14px; border-radius: 6px;">\n'
        f"{rows}\n</div>\n{{% endmacro %}}"
    )
    legend = branca.element.MacroElement()
    legend._template = branca.element.Template(html)
    world.get_root().add_child(legend)
    world.save(str(OUTPUT / "cluster_map.html"))


if __name__ == "__main__":
    OUTPUT.mkdir(exist_ok=True)
    societies = pd.read_csv(ROOT / "data" / "societies.csv")
    plot_elbow(societies.set_index("society_name")[FEATURES])
    clustered = cluster_societies(societies)
    clustered.to_csv(OUTPUT / "clusters.csv", index=False)

    mapped = clustered.merge(pd.read_csv(ROOT / "data" / "coordinates.csv"), on="society_id")
    mapped.to_csv(OUTPUT / "clusters_mapdata.csv", index=False)
    make_charts(clustered)
    make_map(mapped)
    print(f"Saved results in {OUTPUT}")
