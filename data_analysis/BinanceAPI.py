import pandas as pd
import requests

class BinanceAPI():

    def __init__(self):
        self.url = 'https://api.binance.com'

    def __safeRequest(self, url, params):
        try:
            response = requests.get(url, params=params)
        except Exception:
            print('Connection Failed. Reconnecting...')
            self.__safeRequest(url, params) 
        data = response.json()
        if response.status_code != 200:
            raise Exception(data, params)
        return data

    def getCandle(self, param, candles_url='/api/v1/klines'):
        data = self.__safeRequest(self.url + candles_url, params=param)
        df = pd.DataFrame(data).iloc[:,[0, 1, 2, 3, 4, 7]]
        column_name = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        df.columns = column_name
        return df

    # def getXxx(self, ...):
    #     return df  
