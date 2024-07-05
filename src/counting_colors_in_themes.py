import time
import numpy as np
import pandas as pd
from IPython.display import display

# TODO:
#  1. remove (719, "Bricklink Designer Program") from themes +
#  2. top 10 themes by every color
#  3. top 10 colors by every theme
#  4. top 10 themes by total pieces count
#  5. total number of pieces of each color +
#  6. clear inventory_parts from minifigs' parts


def create_result_dataframe():
    color_ids = pd.read_csv("../data/colors.csv")["id"]
    color_ids = pd.concat((pd.Series(["theme_id"]), color_ids))
    color_ids.loc[len(color_ids)] = "total"

    themes = pd.read_csv("../data/themes.csv")
    theme_names = pd.Index(themes[themes["theme_id"] == themes["parent_id"]]["name"])
    theme_names = theme_names.append(pd.Index(["total_pcs"]))

    df = pd.DataFrame(np.zeros((len(theme_names), len(color_ids))), index=theme_names, columns=color_ids).astype("int")
    # display(df)
    return df


def fill_result_dataframe():
    # 119.95s
    parts_df = pd.read_csv("../data/inventory_parts.csv")
    inventory_df = pd.read_csv("../data/inventories.csv", index_col=0)

    for part in parts_df.values:
        inventory_id = part[0]
        color_id = part[1]
        quantity = part[2]

        try:
            theme_name = inventory_df.loc[inventory_id, "theme_name"]
        except Exception as e:
            print(e, theme_name)

        result_df.loc[theme_name, color_id] += quantity
        # result_df.loc[theme_name, "total"] += quantity
        # result_df.loc["total_pcs", color_id] += quantity

start_time = time.time()
result_df = create_result_dataframe()
fill_result_dataframe()
result_df = result_df.drop(index="BrickLink Designer Program")

display(result_df)
result_df.to_csv("../data/result.csv")
print(time.time() - start_time)
