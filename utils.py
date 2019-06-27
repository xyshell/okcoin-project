import pandas as pd

def myfilter(df, key_val):
    key = list(key_val.keys())[0]
    df = df.set_index(key)
    val = list(key_val.values())[0]
    return df.loc[val].reset_index()



