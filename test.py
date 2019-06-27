from CryptoCompareAPI import CryptoCompareAPI
from utils import myfilter

api = CryptoCompareAPI()
top_cap = api.getTopCap()
stable_coins = ['USDT', 'DAI', 'TUSD', 'GUSD', 'USDC', 'PAX', 'USDS']

df = myfilter(top_cap, {'Name': stable_coins})
print(df)
