import numpy as np
import os
import requests
import gzip
import pandas as pd
from IPython.display import display


"""
Downloads .csv.gz archives from https://rebrickable.com/downloads/ and unpacks them into ./data/ folder with required changes
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


def get_parent(df: pd.DataFrame, theme_id):
    parent = df.loc[df["id"] == theme_id, "parent_id"].iloc[0]
    if parent == theme_id:
        return theme_id
    df.loc[df["id"] == theme_id, "parent_id"] = get_parent(df, parent)
    return parent


def transform_csv():
    colors_df = pd.read_csv("../data/colors.csv", usecols=["id", "name"])
    colors_df.to_csv("../data/colors.csv", index=False)

    parts_df = pd.read_csv("../data/inventory_parts.csv", usecols=["inventory_id", "color_id", "quantity", "is_spare"])
    parts_df = parts_df.drop(index=parts_df[parts_df["is_spare"] == 't'].index)
    parts_df = parts_df.drop(columns=["is_spare"])
    parts_df.to_csv("../data/inventory_parts.csv", index=False)

    themes_df = pd.read_csv("../data/themes.csv")
    themes_df["parent_id"] = themes_df["parent_id"].fillna(themes_df["id"]).astype("int64")
    themes_df.to_csv("../data/themes.csv", index=False)

    for theme_id in themes_df["id"]:
        get_parent(themes_df, theme_id)

    themes_df = themes_df.rename(columns={"id": "theme_id"})
    themes_df.to_csv("../data/themes.csv", index=False)

    sets_df = pd.read_csv("../data/sets.csv", usecols=["set_num", "year", "theme_id"])
    sets_df = sets_df.merge(themes_df, how="left")
    sets_df = sets_df.drop(columns=["theme_id", "name"])
    sets_df = sets_df.rename(columns={"parent_id": "theme_id"})
    sets_df = sets_df.merge(themes_df, how="left")

    sets_df = sets_df.drop(columns=["parent_id", "theme_id"])
    sets_df = sets_df.rename(columns={"name": "theme_name"})

    inventories_df = pd.read_csv("../data/inventories.csv", usecols=["id", "set_num"])
    inventories_df = inventories_df.merge(sets_df, how="left").dropna(axis="index")
    inventories_df = inventories_df.drop(columns=["set_num"])
    inventories_df = inventories_df.set_index("id")
    inventories_df.to_csv("../data/inventories.csv")


collect_csv()
transform_csv()
