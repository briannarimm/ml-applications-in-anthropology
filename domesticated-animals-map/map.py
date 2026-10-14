"""Make an interactive map of the primary domesticated animal of each society.

Input:  data/societies.csv and data/coordinates.csv (repository root)
Output: domesticated-animals-map/output/animal_map.html

Each society is one icon. Hover to see the society name.
Click to see the focal year, the role of gods, the animals hunted and the religion.
"""
from pathlib import Path

import branca
import folium
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "output" / "animal_map.html"

# Icon file for each animal category.
# The HTML file links to the icons with a relative path, so keep the folder layout.
ICON_DIR = ROOT / "assets" / "icons"
ICON_URL_DIR = "../../assets/icons"  # from output/animal_map.html to assets/icons
ICONS = {
    "Small Species": "chicken.png",
    "Pigs": "pig.png",
    "Ovides": "sheep.png",
    "Equines": "horse.png",
    "Reindeer": "reindeer.png",
    "Camels": "camel.png",
    "Bovines": "cow.png",
}
LEGEND_NAMES = {"Ovides": "Ovis"}  # label shown in the legend, if different
ICON_SIZE = (30, 30)


def load_data() -> pd.DataFrame:
    """Join the society data to the coordinates. Societies without coordinates are dropped."""
    societies = pd.read_csv(ROOT / "data" / "societies.csv")
    coordinates = pd.read_csv(ROOT / "data" / "coordinates.csv")
    data = societies.merge(coordinates, on="society_id", how="inner")
    print(f"{len(data)} of {len(societies)} societies have coordinates.")
    missing = data.isnull().sum()
    print("Missing values per column (only columns with gaps):")
    print(missing[missing > 0].to_string())
    return data


def make_icon(name: str) -> folium.features.CustomIcon:
    """Folium embeds a local image in the HTML (about 30 KB for each marker).
    Replace the embedded image with a link to keep the HTML file small."""
    icon = folium.features.CustomIcon(str(ICON_DIR / name), icon_size=ICON_SIZE)
    icon.options["icon_url"] = f"{ICON_URL_DIR}/{name}"
    return icon


def build_legend() -> branca.element.MacroElement:
    rows = "\n".join(
        f'    <p><img src="{ICON_URL_DIR}/{icon}" alt="{LEGEND_NAMES.get(name, name)} icon" '
        f'width="25" height="25">&emsp;{LEGEND_NAMES.get(name, name)}</p>'
        for name, icon in ICONS.items()
    )
    html = (
        "{% macro html(this, kwargs) %}\n"
        '<div style="position: fixed; bottom: 30px; left: 30px; z-index: 9999; font-size: 14px;'
        ' background-color: rgba(255,255,255,0.85); padding: 8px 14px; border-radius: 6px;">\n'
        f"{rows}\n</div>\n"
        "{% endmacro %}"
    )
    legend = branca.element.MacroElement()
    legend._template = branca.element.Template(html)
    return legend


def build_map(data: pd.DataFrame) -> folium.Map:
    world = folium.Map(location=[10, 0], tiles="OpenStreetMap", zoom_start=2)
    for row in data.itertuples():
        popup = (
            f"Focal Year: {row.focal_year}"
            f"<br>Role of Gods: {row.roleofgods_label}"
            f"<br>Animals Hunted: {row.animalshunted_label}"
            f"<br>Religion: {row.religion_label}"
        )
        folium.Marker(
            [row.latitude, row.longitude],
            icon=make_icon(ICONS[row.domesticated_label]),
            popup=folium.Popup(popup, min_width=150, max_width=150),
            tooltip=folium.Tooltip(row.society_name),
        ).add_to(world)
    world.get_root().add_child(build_legend())
    return world


if __name__ == "__main__":
    OUTPUT.parent.mkdir(exist_ok=True)
    build_map(load_data()).save(str(OUTPUT))
    print(f"Saved {OUTPUT}")
