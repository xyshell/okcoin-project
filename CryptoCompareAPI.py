import pandas as pd
import requests

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

    def getCandle(self, freq='d', param={'fsym':'BTC', 'tsym':'USD', 'limit':168}):
        if freq == 'd':
            suburl = "/histoday?fsym={}&tsym={}&limit={}".format(
                param['fsym'], param['tsym'], param['limit']
            )
        elif freq == 'h':
            suburl = "/histohour?fsym={}&tsym={}&limit={}".format(
                param['fsym'], param['tsym'], param['limit']
            )
        elif freq == 'm':
            suburl = "/histominute?fsym={}&tsym={}&limit={}".format(
                param['fsym'], param['tsym'], param['limit']
            )
        else:
            raise ValueError('frequency', freq, 'not supported')
        data = self.__safeRequest(self.url + suburl)
        df = pd.DataFrame(data)
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

    