import time
import pandas as pd

COIN_LIST = ['USDT', 'DAI', 'TUSD', 'GUSD', 'USDC', 'PAX', 'USDS']

def unix2date(unix):
    """
        Convert unix epoch time 1562554800 to
        datetime with format '2019-07-07 23:00:00'
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(unix))


def date2unxi(date):
    """
        Convert datetime with format '2019-07-07 23:00:00' to 
        unix epoch time 1562554800
    """
    return int(time.mktime(time.strptime(date, "%Y-%m-%d %H:%M:%S")))

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



