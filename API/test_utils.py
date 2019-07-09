from CryptoCompareAPI import CryptoCompareAPI
from utils import *

api = CryptoCompareAPI()

# Test myfilter
# top_cap = api.getTopCap()
# df = myfilter(top_cap, {'Name': COIN_LIST})
# print(df)

# Test myconcat
param_list = []
for coin in COIN_LIST:
    param_list.append(
        {'fsym':coin, 'tsym':'USD', 'limit':168}
    )
df_list = []
for param in param_list:
    df = api.getCandle('h', param)
    df_list.append(df)
df = myconcat(df_list, ['time', 'close'])
print(df)


