import time
import os
import pandas as pd


"""
Modifies the source tables for further analysis.
"""


def get_parent(df: pd.DataFrame, theme_id):
    """Recursively finds the highest parent of theme."""
    parent = df.loc[df["id"] == theme_id, "parent_id"].iloc[0]
    if parent == theme_id:
        return theme_id
    df.loc[df["id"] == theme_id, "parent_id"] = get_parent(df, parent)
    return parent


def transform_theme_records():
    """Removes unnecessary columns from datasets, combines themes with sets and inventories."""
    colors_df = pd.read_csv("../data/colors.csv", usecols=["id", "name"])
    colors_df.to_csv("../data/colors.csv", index=False)

    # removing spare parts from dataset
    parts_df = pd.read_csv("../data/inventory_parts.csv", usecols=["inventory_id", "color_id", "quantity", "is_spare"])
    parts_df = parts_df.drop(index=parts_df[parts_df["is_spare"] == 't'].index)
    parts_df = parts_df.drop(columns=["is_spare"])
    parts_df.to_csv("../data/inventory_parts.csv", index=False)

    # replacing parental themes to their highest parents
    themes_df = pd.read_csv("../data/themes.csv")
    themes_df["parent_id"] = themes_df["parent_id"].fillna(themes_df["id"]).astype("int64")
    themes_df.to_csv("../data/themes.csv", index=False)

    for theme_id in themes_df["id"]:
        get_parent(themes_df, theme_id)

    themes_df = themes_df.rename(columns={"id": "theme_id"})
    themes_df.to_csv("../data/themes.csv", index=False)

    # attributing themes to sets (temporary dataframe)
    sets_df = pd.read_csv("../data/sets.csv", usecols=["set_num", "year", "theme_id"])
    sets_df = sets_df.merge(themes_df, how="left")
    sets_df = sets_df.drop(columns=["theme_id", "name"])
    sets_df = sets_df.rename(columns={"parent_id": "theme_id"})
    sets_df = sets_df.merge(themes_df, how="left")

    sets_df = sets_df.drop(columns=["parent_id", "theme_id"])
    sets_df = sets_df.rename(columns={"name": "theme_name"})

    # attributing themes to inventories
    inventories_df = pd.read_csv("../data/inventories.csv", usecols=["id", "set_num"])
    inventories_df = inventories_df.merge(sets_df, how="left").dropna(axis="index")
    inventories_df = inventories_df.drop(columns=["set_num"])
    inventories_df = inventories_df.set_index("id")
    inventories_df.to_csv("../data/inventories.csv")

    os.remove("../data/sets.csv")
