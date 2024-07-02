import os
import requests
import gzip
import pandas as pd
from IPython.display import display


"""
Downloads .csv.gz archives and unpacks them into ./data/ folder with required changes
"""


def download(item):
    url = f"https://cdn.rebrickable.com/media/downloads/{item}.csv.gz"
    response = requests.get(url)
    path = "../data/" + url.split('/')[-1]
    with open(path, mode="wb") as file:
        file.write(response.content)
    file.close()


def unpack(item):
    filename = f"../data/{item}.csv.gz"
    with gzip.open(filename, mode="rb") as archive,\
         open(filename[:-3], mode="wb") as csv:
        csv.write(archive.read())
    archive.close()
    csv.close()
    os.remove(filename)


def collect_csv():
    for db_item in ["themes", "colors", "inventories", "sets", "inventory_parts"]:
        download(db_item)
        unpack(db_item)


def transform_csv():
    sets_df = pd.read_csv("../data/sets.csv")
    sets_df = sets_df.drop(columns=["name", "num_parts", "img_url"])
    sets_df.to_csv("../data/sets.csv", index=False)

    inventories_df = pd.read_csv("../data/inventories.csv")
    inventories_df = inventories_df.drop(columns=["version"])
    inventories_df.to_csv("../data/inventories.csv", index=False)

    colors_df = pd.read_csv("../data/colors.csv")
    colors_df = colors_df.drop(columns=["rgb", "is_trans"])
    colors_df.to_csv("../data/colors.csv", index=False)

    parts_df = pd.read_csv("../data/inventory_parts.csv")
    parts_df = parts_df.drop(index=parts_df[parts_df["is_spare"] == 't'].index)
    parts_df = parts_df.drop(columns=["part_num", "img_url", "is_spare"])
    parts_df.to_csv("../data/inventory_parts.csv", index=False)

    themes_df = pd.read_csv("../data/themes.csv")
    themes_df["parent_id"] = themes_df["parent_id"].fillna(themes_df["id"]).astype("int64")
    themes_df.to_csv("../data/themes.csv", index=False)

collect_csv()
transform_csv()
