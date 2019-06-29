import pandas as pd

COIN_LIST = ['USDT', 'DAI', 'TUSD', 'GUSD', 'USDC', 'PAX', 'USDS']

def myfilter(df, key_val):
    key = list(key_val.keys())[0]
    df = df.set_index(key)
    val = list(key_val.values())[0]
    return df.loc[val].reset_index()

def myconcat(df_list, cols):
    """concat dataframes by cols[0] as index, and cols[1] as data
    """
    for i in range(len(df_list)):
        if i == 0:
            df = df_list[i].filter(items=cols).set_index(cols[0])
        else:
            temp_df = df_list[i].filter(items=cols).set_index(cols[0])
            df = pd.concat([df, temp_df], axis=1)
    return df.dropna(how='any', axis=0).reset_index()



