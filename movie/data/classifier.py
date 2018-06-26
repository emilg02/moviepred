import os
import pandas as pd
def classifier(row):
    if row["revenue"] <= 500000:
         return 1
    elif row["revenue"] > 500000 and row["revenue"] <= 1000000:
        return 2
    elif row["revenue"] > 1000000 and row["revenue"] <= 40000000:
        return 3
    elif row["revenue"] > 40000000 and row["revenue"] <= 150000000:
        return 4
    else:
        return 5
def apply_class_to_dataset():
    cwd = os.getcwd()
    df = pd.read_csv("movies_new.csv")
    df = df.dropna()

    #classify movies into 5 categories
    df["revenue_class"] = df.apply(classifier, axis=1)
    df.to_csv("test.csv")