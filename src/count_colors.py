import datetime
import time

import numpy as np
import pandas as pd
from IPython.display import display


def create_theme_dataframe():
    color_ids = pd.read_csv("../data/colors.csv")["id"]
    # color_ids = pd.concat((pd.Series(["theme_id"]), color_ids))
    color_ids.loc[len(color_ids)] = "total"

    themes = pd.read_csv("../data/themes.csv")
    theme_names = pd.Index(themes[themes["theme_id"] == themes["parent_id"]]["name"])
    theme_names = theme_names.append(pd.Index(["total_pcs"]))

    df = pd.DataFrame(np.zeros((len(theme_names), len(color_ids))), index=theme_names, columns=color_ids).astype("int")
    return df


def create_year_dataframe():
    color_ids = pd.read_csv("../data/colors.csv")["id"]
    color_ids.loc[len(color_ids)] = "total"

    current_year = datetime.datetime.today().year
    years = np.arange(1949, current_year + 1)
    years = np.setdiff1d(years, np.array([1951, 1952]))
    years = pd.Index(years).append(pd.Index(["total_pcs"]))

    df = pd.DataFrame(np.zeros((len(years), len(color_ids))), index=years, columns=color_ids).astype("int")
    return df


def count_colors():
    theme_df = create_theme_dataframe()
    year_df = create_year_dataframe()
    parts_df = pd.read_csv("../data/inventory_parts.csv")
    inventory_df = pd.read_csv("../data/inventories.csv", index_col=0)

    for part in parts_df.values:
        inventory_id, color_id, quantity = part

        try:
            theme_name = inventory_df.loc[inventory_id, "theme_name"]
            year = inventory_df.loc[inventory_id, "year"]
        except:
            continue

        theme_df.loc[theme_name, color_id] += quantity
        year_df.loc[year, color_id] += quantity

    theme_df.index.name = "theme_name"
    theme_df = theme_df.drop(index="BrickLink Designer Program")
    theme_df.loc["total_pcs"] = theme_df.sum(axis="index")
    theme_df["total"] = theme_df.sum(axis="columns")
    theme_df.to_csv("../data/theme_result.csv")

    theme_df.index.name = "year"
    year_df.loc["total_pcs"] = year_df.sum(axis="index")
    year_df["total"] = year_df.sum(axis="columns")
    year_df.to_csv("../data/year_result.csv")

    return theme_df, year_df
