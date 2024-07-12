import time
import pandas as pd
from IPython.display import display
from collect_csv import collect_csv
import setup_themes
import count_colors

# TODO:
#  7.  2-3-4 themes comparison plot (first N colors)
#  9.  all colors of specific part (API)
#  10. minifigs
#  11. top N colors by several years
#  12. optimization
#  13. descending order to colors/items list
#  14. saving results


class LegoDB:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(LegoDB, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.theme_df = None
        self.year_df = None
        collect_csv()
        setup_themes.transform_records()
        self.theme_df, self.year_df = count_colors.count_colors()

    def show_colors(self):
        df = pd.read_csv("../data/colors.csv", index_col=0)
        print(df.to_string())

    def show_themes(self):
        df = pd.read_csv("../data/result.csv", usecols=[0])
        print(df.to_string())

    def create_result_table(self, item, header, count, source_list, total_pcs):
        output_dict = {item: [], "quantity": [], "percentage": []}
        max_name_len = 4 * (item == "year")

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

    def get_popular_color_list(self, item, count):
        if int(count) < 0:
            print("Enter non-negative number")
            return

        if item.isnumeric():
            df = self.year_df
        else:
            df = self.theme_df

        count = min(int(count), len(df) - 1)
        try:
            color_list = df.loc[item, df.columns != "total"]\
                           .sort_values(ascending=False).head(count)
        except KeyError:
            print("Incorrect year number/theme name. "
                  "Parts are produced from 1949 to the current year, with the exception of 1951 and 1952. "
                  "To see all of theme names, use command `2`.")
            return

        # changing color_id from theme_df to corresponding color names
        color_dict = pd.read_csv("../data/colors.csv", index_col=0).to_dict()["name"]
        new_index = []
        for color in color_list.index:
            new_index.append(color_dict[int(color)])
        color_list.index = new_index

        total_pcs = df.loc[item, "total"]
        self.create_result_table("color_name", item, count, color_list, total_pcs)

    def get_list_by_color(self, item, color_name, count):
        if int(count) < 0:
            print("Enter non-negative number")
            return

        if item == "years":
            item = item[:-1]
            df = self.year_df
        elif item == "themes":
            item = "theme_name"
            df = self.theme_df
        else:
            print("Incorrect input (should be `years` or `themes`)")
            return

        count = min(int(count), len(df.columns) - 1)

        # getting color id if color name is given
        color_df = pd.read_csv("../data/colors.csv", index_col=0)
        if color_name.isnumeric() or color_name == "-1":
            color_id = color_name
            color_name = color_df.loc[int(color_id)].iloc[0]
        else:
            try:
                color_id = str(color_df.loc[color_df["name"] == color_name].index[0])
            except IndexError:
                print("Incorrect color name/id")
                return

        theme_list = df.loc[df.index != "total_pcs", color_id]\
                       .sort_values(ascending=False).head(count)

        total_pcs = df.loc["total_pcs", color_id]
        self.create_result_table(item, color_name, count, theme_list, total_pcs)

    def get_total_count_list(self, item, count, ascending="y"):
        if int(count) < 0:
            print("Enter non-negative number")
            return

        if item == "years":
            item = item[:-1]
            df = self.year_df
        elif item == "themes":
            item = "theme_name"
            df = self.theme_df
        else:
            print("Incorrect input (should be `years` or `themes`)")
            return

        ascending = ascending == "y"

        theme_list = df.loc[df.index != "total_pcs", "total"]\
                         .sort_values(ascending=ascending).head(int(count))
        theme_list = theme_list[theme_list > 0]
        total = self.theme_df.loc["total_pcs", "total"]
        self.create_result_table(item, "total", len(theme_list), theme_list, total)


# st = time.time()
# x = LegoDB()
# x.theme_df = pd.read_csv("../data/result.csv", index_col=0)
# x.year_df = pd.read_csv("../data/year_result.csv", index_col=0)

# x.get_total_count_list("year", 10, False)
# print(time.time() - st)
