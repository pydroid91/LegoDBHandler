import time
import numpy as np
import pandas as pd


def create_result_dataframe():
    color_ids = pd.read_csv("../data/colors.csv")["id"]
    color_ids = pd.concat((pd.Series(["theme_id"]), color_ids))
    color_ids.loc[len(color_ids)] = "total"

    themes = pd.read_csv("../data/themes.csv")
    theme_names = pd.Index(themes[themes["theme_id"] == themes["parent_id"], "name"].iloc[0])
    theme_names = theme_names.append(pd.Index(["total_pcs"]))

    df = pd.DataFrame(np.zeros((len(theme_names), len(color_ids))), index=theme_names, columns=color_ids).astype("int")
    return df


def count_colors(result_df):
    parts_df = pd.read_csv("../data/inventory_parts.csv")
    inventory_df = pd.read_csv("../data/inventories.csv", index_col=0)

    for part in parts_df.values:
        inventory_id = part[0]
        color_id = part[1]
        quantity = part[2]

        try:
            theme_name = inventory_df.loc[inventory_id, "theme_name"]
        except:
            continue

        result_df.loc[theme_name, color_id] += quantity

    result_df.loc["total_pcs"] = result_df.sum(axis="index")
    result_df["total"] = result_df.sum(axis="columns")


def get_theme_df():
    df = create_result_dataframe()
    count_colors(df)
    df = df.drop(index="BrickLink Designer Program")
    df.to_csv("../data/result.csv")
    return df

# result_df = pd.read_csv("../data/result.csv", index_col=0)
