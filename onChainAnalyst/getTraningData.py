#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 18:19:45 2019

@author: HeJiabao
"""

import pandas as pd
import numpy as np
import time
import requests

transaction = pd.read_csv('tether_transactions_522647.csv')
address = pd.read_csv('address.csv')

transaction.block_time = pd.to_datetime(transaction.block_time)

my_transaction = transaction[transaction.block_time > pd.Timestamp(2018, 5, 1, 0)]

dataset = pd.DataFrame(columns=['time', 'amount', 'sameExchange', 'price', 'vol', 'isIncreasing'])
dataset[['time','amount']] = my_transaction[['block_time','amount']]

# get data to see wheather they come from the same exchange
for i in range(len(my_transaction)):
    print(i)
    addr1 = address.loc[address['address'] == my_transaction.iloc[i]['sending_address']]
    addr2 = address.loc[address['address'] == my_transaction.iloc[i]['reference_address']]
    if len(addr1) == 0 or len(addr2) == 0:
        dataset.iloc[i, 2] = 0
    else:
        exchange1 = addr1['exchange']
        exchange2 = addr2['exchange']
        if exchange1.iloc[0] != exchange2.iloc[0]:
            dataset.iloc[i, 2] = 0
        else:
            dataset.iloc[i, 2] = 1

# Get trading data from CryptoCompareAPI
def get_Tether_price(my_time):
    ts = str(my_time)
    url = 'https://min-api.cryptocompare.com/data/pricehistorical?'
    sub_url = 'fsym=USDT&tsyms=USD&ts=%s' % ts
    fianl_url = url+sub_url
    response = requests.get(fianl_url)
    resp = response.json()
    return resp['USDT']['USD']

for dt64 in dataset['time'].unique():
    ts = (dt64 - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's')
    price = get_Tether_price(int(ts))

    dataset.loc[dataset['time'] == dt64, 'price'] = price



# dataset.to_csv('training_data.csv')


