import pandas as pd
import numpy as np
import requests
import re
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
    
    def getCandle(self, fsym, tsym, freq, start_time=None, end_time=None, limit=None):        
        """
            fsym: ticker
            tsym: base
            freq: '1m', '2h', '3d'
            start_time: string datetime format
            end_time: string datetime format
            limit: number of candles
        """
        fsym = fsym.upper()
        tsym = tsym.upper()
        agg = re.findall("\d+", freq)[0]
        freq = re.findall("[a-z]", freq)[0]
        if freq == 'd':
            base_url = "/histoday?fsym={}&tsym={}".format(fsym, tsym)
        elif freq == 'h':
            base_url = "/histohour?fsym={}&tsym={}".format(fsym, tsym)
        elif freq == 'm':
            base_url = "/histominute?fsym={}&tsym={}".format(fsym, tsym)
        else:
            raise ValueError('frequency', freq, 'not supported')
        base_url += f'&aggregate={agg}' # aggragate
        if start_time != None and end_time != None and limit == None:
            start_unix = int(pd.to_datetime(start_time).timestamp())
            end_unix = int(pd.to_datetime(end_time).timestamp())
            base_url += f'&limit={2000}' # limit
            query_url = base_url + f'&toTs={end_unix}' # until
            bottom_df = pd.DataFrame(self.__safeRequest(self.url + query_url)) 
            while True:
                old_unix = bottom_df.iloc[0]['time']
                if  old_unix <= start_unix:
                    bottom_df = bottom_df[bottom_df['time'] >= start_unix]
                    break
                else:
                    query_url = base_url + f'&toTs={old_unix}' 
                    query_df = pd.DataFrame(self.__safeRequest(self.url + query_url))
                    if len(query_df) == 0:
                        request_time = datetime.utcfromtimestamp(start_unix).strftime('%Y-%m-%d %H:%M:%S')
                        earlies_time = datetime.utcfromtimestamp(old_unix).strftime('%Y-%m-%d %H:%M:%S')
                        print(f"Request from {request_time}. But Available from {earlies_time}")
                        break
                    else:
                        bottom_df = query_df.append(bottom_df.iloc[1:], ignore_index=True)
            return bottom_df
        elif end_time != None and limit != None and start_time == None:
            end_unix = int(pd.to_datetime(end_time).timestamp())
            base_url += f'&limit={limit}' # limit
            query_url = base_url + f'&toTs={end_unix}' # until
            return pd.DataFrame(self.__safeRequest(self.url + query_url))
        elif end_time == None and start_time == None and limit != None:
            base_url += f'&limit={limit}' # limit
            return pd.DataFrame(self.__safeRequest(self.url + base_url))
        else:
            raise ValueError(f"Can't do start_time={start_time}, end_time={end_time}, limit={limit}")

        
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
    df = api.getCandle('BTC', 'USDT', '1m', "2019-01-01", "2019-07-15")
    print(df)

    