# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 00:27:10 2019

@author: Owner
"""

#connect with data_retrival.py and data_storage.py
#input ticker, retrieve data and store them

from data_retrival import data_retrieve 
from data_storage import data_storage

ret = data_retrieve()
stor = data_storage('crypto_base.sqlite')

coins = ['LTC']#1483232400 2017/01/01, 1561694400 2019-06-28 00:00
stables = ['DAI','USDT', 'GUSD', 'TUSD', 'USDC', 'PAX', 'USDS'] 
exchanges = ['Coinbase', 'Binance']

for item in stables:
    print('Start retrieve '+item+' data. \n')
    #                   ('freq', start_time,                       params                  stop_time)
    data = ret.history_data('m',1563336000, {'fsym':item,'tsym':'USD','limit':2000,'e':'' ,'toTs':0})
    df, table_name = ret.output(data)
    stor.load_data(df, table_name, True)


#stor.commit()


