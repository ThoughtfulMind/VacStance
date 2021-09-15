import pickle as pkl
import pandas as pd

with open("output/dedup_combined_df_2020_1_1_to_2021_7_1.pkl", "rb") as f:
    object = pkl.load(f)

df = pd.DataFrame(object)

df.to_csv(r'output/unpickle.csv')