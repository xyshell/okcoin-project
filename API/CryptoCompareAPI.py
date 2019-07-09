import pandas as pd
import numpy as np
import requests
from datetime import datetime

class CryptoCompareAPI():

    def __init__(self):
        self.url = 'https://min-api.cryptocompare.com/data'

    def __safeRequest(self, url):
        try:
            response = requests.get(url)
        except Exception:
            print('Connection Failed. Reconnecting...')
            self.__safeRequest(url)
        resp = response.json()
        if response.status_code != 200:
            raise Exception(resp)
        data = resp['Data']
        return data
    
    def getCandle(self, start_time, end_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), freq='d',
                  param={'fsym':'BTC', 'tsym':'USD'}):        
        try:
            start_tstmp = pd.to_datetime(start_time)
        except TypeError as error:
            print(error)
        try:
            end_tstmp = pd.to_datetime(end_time)
        except TypeError as error:
            print(error)
        
        start_stmp = int(pd.to_datetime(start_time).timestamp())
        end_stmp = int(pd.to_datetime(end_time).timestamp())
        
        if freq == 'd':
            ind = 60*60*24
            suburl = "/histoday?fsym={}&tsym={}".format(param['fsym'], param['tsym'])
        elif freq == 'h':
            ind = 60*60
            suburl = "/histohour?fsym={}&tsym={}".format(param['fsym'], param['tsym'])
        elif freq == 'm':
            ind = 60
            suburl = "/histominute?fsym={}&tsym={}".format(param['fsym'], param['tsym'])
        else:
            raise ValueError('frequency', freq, 'not supported')
        
        record_num = int((end_stmp-start_stmp)/ind)
        full_fetch_time = record_num//2000
        record_left = record_num-2000*full_fetch_time
        limit_list = [2000]*full_fetch_time + [record_left]*int(record_left>0)
        count_stmp = end_stmp
        df = pd.DataFrame()
        
        for limit in limit_list:
            full_suburl = suburl + "&limit={}&toTs={}".format(limit, count_stmp)
            data = self.__safeRequest(self.url + full_suburl)
            df1 = pd.DataFrame(data)
            df1 = df1.iloc[::-1]
            df = df.append(df1, ignore_index=True)
            count_stmp -= limit*ind
            
        df = df.drop_duplicates()
        
        return df
    
    def getTopCap(self, param={'tsym':'USD', 'limit':100}):
        suburl = "/top/mktcapfull?limit={}&tsym={}".format(
            param['limit'], param['tsym']
        )
        data = self.__safeRequest(self.url + suburl)
        name = [i['CoinInfo']['Name'] for i in data]
        mktcap = [i['RAW'][param['tsym']]['MKTCAP'] for i in data]
        supply = [i['RAW'][param['tsym']]['SUPPLY'] for i in data]
        vol_from_24h = [i['RAW'][param['tsym']]['VOLUME24HOURTO'] for i in data]
        vol_to_24h = [i['RAW'][param['tsym']]['VOLUME24HOURTO'] for i in data]
        df = pd.DataFrame({
            'Name':name, 'MarketCap':mktcap, 'Supply':supply,
            '24HVol':vol_from_24h, '24HBaseVol':vol_to_24h
        })
        return df

if __name__ == '__main__':
    api = CryptoCompareAPI()
    param = {'fsym':'USDT', 'tsym':'USD', 'limit':168}
    df = api.getCandle('h', param)
    print(df)

    