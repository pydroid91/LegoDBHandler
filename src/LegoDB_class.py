import time
import pandas as pd
from IPython.display import display
from collect_csv import collect_csv
import setup_themes
import count_colors_by_theme

# TODO:
#  6.  clear inventory_parts from minifigs' parts
#  7.  2-3-4 themes comparison plot (first N colors)
#  8.  top N colors by year
#  9.  all colors of specific part (API)
#  10. minifigs


class LegoDB:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(LegoDB, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.theme_df = None
        self.year_df = None
        # collect_csv()

    def fill_theme_df(self):
        # 5m53s
        setup_themes.transform_theme_records()
        self.theme_df = count_colors_by_theme.get_theme_df()
        display(self.theme_df)

    def fill_year_df(self):
        pass

    def create_result_table(self, item, header, count, source_list, total_pcs):
        output_dict = {item: [], "quantity": [], "percentage": []}
        max_name_len = 0

        for i in range(count):
            quantity = source_list.iloc[i]
            if quantity == 0:
                break
            item_name = source_list.index[i]
            max_name_len = max(max_name_len, len(item_name))
            output_dict[item].append(item_name)
            output_dict["quantity"].append(quantity)
            output_dict["percentage"].append(f"{quantity / total_pcs * 100:.3f}")

        # length of the header depends on maximum size of color name
        header_len = 25 + max_name_len
        # displaying result
        print(f"{header:=^{header_len}s}")
        output_df = pd.DataFrame(output_dict)
        output_df.index += 1
        # return output_df
        display(output_df)

    def get_colors_list(self, count, theme_name):
        count = min(count, len(self.theme_df) - 1)
        color_list = self.theme_df.loc[theme_name, self.theme_df.columns != "total"]\
                         .sort_values(ascending=False).head(count)

        # changing color_id from theme_df to corresponding color names
        color_dict = pd.read_csv("../data/colors.csv", index_col=0).to_dict()["name"]
        new_index = []
        for color in color_list.index:
            new_index.append(color_dict[int(color)])
        color_list.index = new_index

        total_pcs = self.theme_df.loc[theme_name, "total"]
        self.create_result_table("color_name", theme_name, count, color_list, total_pcs)

    def get_themes_list(self, count, color_name):
        count = min(count, len(self.theme_df.columns) - 1)

        # getting color id if color name is given
        color_df = pd.read_csv("../data/colors.csv", index_col=0)
        if color_name.isnumeric() or color_name == "-1":
            color_id = color_name
            color_name = color_df.loc[int(color_id)].iloc[0]
        else:
            try:
                color_id = str(color_df.loc[color_df["name"] == color_name].index[0])
            except IndexError:
                print("Incorrect id")
                return

        theme_list = self.theme_df.loc[self.theme_df.index != "total_pcs", color_id]\
                         .sort_values(ascending=False).head(count)
        total_pcs = self.theme_df.loc["total_pcs", color_id]
        self.create_result_table("theme_name", color_name, count, theme_list, total_pcs)

    def get_total_count_list(self, count, ascending=True):
        theme_list = self.theme_df.loc[self.theme_df.index != "total_pcs", "total"]\
                         .sort_values(ascending=ascending).head(count)
        theme_list = theme_list[theme_list > 0]
        total = self.theme_df.loc["total_pcs", "total"]
        self.create_result_table("theme_name", "total", len(theme_list), theme_list, total)


x = LegoDB()
x.theme_df = pd.read_csv("../data/result.csv", index_col=0)
x.get_total_count_list(18, ascending=True)
st = time.time()

print(time.time() - st)
