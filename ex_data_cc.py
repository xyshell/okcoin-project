from APIs.CryptoCompareAPI import CryptoCompareAPI
from utils import CC_DATA_PATH, cc2bt
import os

api = CryptoCompareAPI()

# df = api.getCandle('d', param)
# df['datetime'] = df['time'].apply(unix2date)
# df.to_csv(os.path.join(CC_DATA_PATH, "ex_candle_1D.csv"), index=False)

# df = api.getCandle('h', param)
# df['datetime'] = df['time'].apply(unix2date)
# df.to_csv(os.path.join(CC_DATA_PATH, "ex_candle_1H.csv"), index=False)

# df = api.getCandle('m', param)
# df['datetime'] = df['time'].apply(unix2date)
# df.to_csv(os.path.join(CC_DATA_PATH, "ex_candle_1M.csv"), index=False)

# IGNIS airdrop 
# df = api.getCandle('IGNIS', 'USDT', '1h', start_time="2019-06-01", end_time="2019-07-15")
# df = cc2bt(df)
# df.to_csv(os.path.join(CC_DATA_PATH, "IGNIS_airdrop_1h.csv"), index=False)

# df = api.getCandle('IGNIS', 'USDT', '4h', start_time="2019-06-01", end_time="2019-07-15")
# df = cc2bt(df)
# df.to_csv(os.path.join(CC_DATA_PATH, "IGNIS_airdrop_4h.csv"), index=False)

# df = api.getCandle('IGNIS', 'USDT', '1d', start_time="2019-06-01", end_time="2019-07-15")
# df = cc2bt(df)
# df.to_csv(os.path.join(CC_DATA_PATH, "IGNIS_airdrop_1d.csv"), index=False)

# ZCL fork
# df = api.getCandle('ZCL', 'BTC', '4h', start_time="2017-06-01", end_time="2018-06-01")
# df = cc2bt(df)
# df.to_csv(os.path.join(CC_DATA_PATH, "ZCL_fork_4h.csv"), index=False)

# GXC buyback
df = api.getCandle('GXS', 'USDT', '4h', start_time="2019-04-01", end_time="2019-07-22")
df = cc2bt(df)
df.to_csv(os.path.join(CC_DATA_PATH, "GXS_buyback_4h.csv"), index=False)

