import datetime
import numpy as np
import pandas as pd
from IPython.display import display


def create_result_dataframe():
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


def count_colors(result_df, item):
    parts_df = pd.read_csv("../data/inventory_parts.csv")
    inventory_df = pd.read_csv("../data/inventories.csv", index_col=0)

    for part in parts_df.values:
        inventory_id = part[0]
        color_id = part[1]
        quantity = part[2]

        try:
            item_name = inventory_df.loc[inventory_id, item]
        except:
            continue

        result_df.loc[item_name, color_id] += quantity

    result_df.loc["total_pcs"] = result_df.sum(axis="index")
    result_df["total"] = result_df.sum(axis="columns")


def get_theme_df():
    df = create_result_dataframe()
    count_colors(df, "theme_name")
    df.index.name = "theme_name"
    df = df.drop(index="BrickLink Designer Program")
    df.to_csv("../data/result.csv")
    return df


def get_year_df():
    df = create_year_dataframe()
    count_colors(df, "year")
    df.index.name = "year"
    df.to_csv("../data/year_result.csv")
    return df

# result_df = pd.read_csv("../data/result.csv", index_col=0)
