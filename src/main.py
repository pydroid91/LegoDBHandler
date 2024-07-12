from LegoDB_class import LegoDB
import pandas as pd

def main():
    print("Collecting database...")
    db = LegoDB()
    print("Available commands:\n"
          "(1) Show all colors.\n"
          "(2) Show all themes.\n"
          "(3) Show ranked list of number of parts of specific colors for each year/theme.\n"
          "(4) Show ranked list of most popular colors for specific year/theme.\n"
          "(5) Show ranked list of total number of parts for all of the years/themes.\n"
          "(exit) End program.")

    # use 18-19 to speed up when result.csv and year_result.csv are in `../data/`
    # (comment 29-32 in LegoDB_class.LegoDB.__init__)

    # db.theme_df = pd.read_csv("../data/result.csv", index_col=0)
    # db.year_df = pd.read_csv("../data/year_result.csv", index_col=0)
    actions = {"1": db.show_colors,
               "2": db.show_themes,
               "3": db.get_list_by_color,
               "4": db.get_popular_color_list,
               "5": db.get_total_count_list,
               "exit": exit}
    response = {"1": [],
                "2": [],
                "3": ["Where to count (years/themes): ", "Color name/id: ", "How many to print: "],
                "4": ["Enter year number or theme name: ", "How many to print: "],
                "5": ["Where to count (years/themes): ", "How many to print: ", "Is ascending (y/n): "],
                "exit": []}
    while True:
        print("\nEnter command:")
        action = input()
        args = []
        for arg in response[action]:
            print(arg)
            args.append(input())
        actions[action](*args)


if __name__ == "__main__":
    main()
