import pandas as pd
from IPython.display import display

df = pd.Series([1, 1, 2, 3, 4, 4, 2])
df = df.drop_duplicates()
display(df)