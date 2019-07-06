# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 00:27:10 2019

@author: Owner
"""

from data_retrival import data_retrieve 
from data_storage import data_storage

#增加获取类别， 修改 data_retrieve 的 load_data()
ret = data_retrieve()
stor = data_storage('crypto_base.sqlite')

coins = ['LTC']#['BTC', 'ETH']#,['LTC'] #1483232400 2017/01/01 #1561694400 min
stables = ['DAI','USDT', 'GUSD'] #14910084002017/04/01
exchanges = ['Coinbase', 'Binance']

for item in coins:
    data = ret.history_data('m',1561694400, {'fsym':item,'tsym':'USD','limit':2000,'e':'' ,'toTs':0})
    df, table_name = ret.output(data)
    stor.load_data(df, table_name, True)

#stor.drop_duplicates('table_titles')
#stor.commit()

#cur_df = stor.dump_data('price_BTC_USD_h')1483232400

