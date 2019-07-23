import os
import time

ROOT = os.path.abspath('.')
CAW_DATA_PATH = os.path.join(ROOT, 'data_caw')
CC_DATA_PATH = os.path.join(ROOT, 'data_cryptocompare')

# sample data
CC_EXDATA_PATH_1D = os.path.join(CC_DATA_PATH, 'ex_candle_1D.csv')
CC_EXDATA_PATH_1H = os.path.join(CC_DATA_PATH, 'ex_candle_1H.csv')
CC_EXDATA_PATH_4H = os.path.join(CC_DATA_PATH, 'ex_candle_4H.csv')
CC_EXDATA_PATH_5M = os.path.join(CC_DATA_PATH, 'ex_candle_5M.csv')
CC_EXDATA_PATH_15M = os.path.join(CC_DATA_PATH, 'ex_candle_15M.csv')

# IGNIS airdrop data
CC_IGNIS_1H = os.path.join(CC_DATA_PATH, 'IGNIS_airdrop_1h.csv')
CC_IGNIS_4H = os.path.join(CC_DATA_PATH, 'IGNIS_airdrop_4h.csv')
CC_IGNIS_1D = os.path.join(CC_DATA_PATH, 'IGNIS_airdrop_1d.csv')

# ZCL fork data
CC_ZCL_4H = os.path.join(CC_DATA_PATH, 'ZCL_fork_4h.csv')

# GXS buyback data
CC_GXS_4H = os.path.join(CC_DATA_PATH, 'GXS_buyback_4h.csv')


def unix2date(unix, fmt="%Y-%m-%d %H:%M:%S"):
    """
        Convert unix epoch time 1562554800 to
        datetime with format
    """
    return time.strftime(fmt, time.localtime(unix))

def date2unxi(date, fmt="%Y-%m-%d %H:%M:%S"):
    """
        Convert datetime with format to 
        unix epoch time 1562554800
    """
    return int(time.mktime(time.strptime(date, fmt)))

def cc2bt(df):
    """Convert CryptoCompare data to Backtrader data
    """
    df['datetime'] = df['time'].apply(unix2date)
    df['time'] = df['datetime'].apply(lambda x: x.split(' ')[1])
    df['datetime'] = df['datetime'].apply(lambda x: x.split(' ')[0])
    return df
