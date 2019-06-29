
# coding: utf-8

# In[1]:


from CryptoCompareAPI import CryptoCompareAPI
from utils import COIN_LIST, myconcat
import cufflinks as cf
import pandas as pd


# In[2]:


# Get trading data from CryptoCompareAPI
api = CryptoCompareAPI()

param_list = []
for coin in COIN_LIST:
    param_list.append(
        {'fsym':coin, 'tsym':'USD', 'limit':24*3}
    )

df_list = []
for param in param_list:
    df = api.getCandle('h', param)
    df_list.append(df)

df = myconcat(df_list, ['time', 'close'])
df.columns = ['time'] + COIN_LIST
df.time = pd.to_datetime(df.time, unit='s')


# In[3]:


df.info()


# In[14]:


cf.set_config_file(offline=False, world_readable=True, theme='henanigans')
df.iplot(x='time', kind='scatter', xTitle='Date', yTitle='Price', title='Liquidity Profile of Stablecoins')

