import pandas as pd
from IPython.display import display

df = pd.read_csv("../result.csv", index_col=0)


sorted_df = df.sort_values(by="75", ascending=False)
display(sorted_df.head(10).loc[:, "75"])
