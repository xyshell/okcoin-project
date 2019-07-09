import os
import time

ROOT = os.path.abspath('.')
CAW_DATA_PATH = os.path.join(ROOT, 'data_caw')
CC_DATA_PATH = os.path.join(ROOT, 'data_cryptocompare')

# sample data
CC_DATA_PATH_1D = os.path.join(CC_DATA_PATH, 'ex_candle_1D.csv')
CC_DATA_PATH_1H = os.path.join(CC_DATA_PATH, 'ex_candle_1H.csv')
CC_DATA_PATH_4H = os.path.join(CC_DATA_PATH, 'ex_candle_4H.csv')
CC_DATA_PATH_5M = os.path.join(CC_DATA_PATH, 'ex_candle_5M.csv')
CC_DATA_PATH_15M = os.path.join(CC_DATA_PATH, 'ex_candle_15M.csv')

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
