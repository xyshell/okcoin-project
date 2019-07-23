import requests
import numpy as np
import pandas as pd
import sqlite3
import datetime
import pytz



#api_key: 6d7259f0240106c89188aa493f3937dc3d15ec7576e4c6706342edf82c2c12d3

class data_retrieve():
    
    def __init__(self):
        
        self.base_url = 'https://min-api.cryptocompare.com/data/'
        self.api_key = '6d7259f0240106c89188aa493f3937dc3d15ec7576e4c6706342edf82c2c12d3'
        
    def retrieve(self, url):
        try:
            handle = requests.get(url)
        except Exception:
            print('Reconnect')
            self.retrieve(url)
        
        resp = handle.json()
        
        if 'Response' in resp.keys():
            if resp['Response'] == 'Error':
                #print(resp)
                raise Exception('\nResponse error! \n' + resp['Message'])
                
            
        return resp
    
    
    
    def history_data(self, style = 'h', fromTs = 0, param = {'fsym':'','tsym':'USD','limit':10, 'e':'','toTs':0} ):
        
        if len(param['fsym']+param['e']) < 1:
            raise ValueError('Unsupport Parameter! /n')
        
        self.fromTs = fromTs
        self.style = style
        self.param = param
        #&limit=2000&toTs={the earliest timestamp received}
        #cal float window length for retrieval limits
        if fromTs != 0 and param['toTs'] != 0:
            window = self.window_length(style, fromTs, param['toTs'], param['limit'])
            print('window_length: '+ str(window))
            param['limit']=window

        
        if style == 'd':
            extension = "histoday?fsym={}&tsym={}&limit={}".format(param['fsym'],param['tsym'],param['limit'])
            
        elif style == 'h':
            extension = "histohour?fsym={}&tsym={}&limit={}".format(param['fsym'],param['tsym'],param['limit'])
            
        elif style == 'm':
            extension = "histominute?fsym={}&tsym={}&limit={}".format(param['fsym'],param['tsym'],param['limit'])
            
        elif style == 'ed':
            extension = "exchange/histoday?e={}&tsym={}&limit={}".format(param['e'],param['tsym'],param['limit'])
            
        elif style == 'eh':
            extension = "exchange/histohour?e={}&tsym={}&limit={}".format(param['e'],param['tsym'],param['limit'])
            
        else:
            raise ValueError('Wrong freq input')
            return 0
        
        if param['toTs'] != 0: #toTS=0: retrieve data until today, toTs !=0 retrieve data until that time
            extension+="&toTs={}".format(param['toTs'])
        extension = extension + '&api_key=' + self.api_key
            
        url = self.base_url + extension
        resp = self.retrieve(url)
        data = resp['Data']
        
        if fromTs < resp['TimeFrom']: #or timefrom
            param['toTs']=resp['TimeFrom']
            data = self.history_data(style, fromTs, param) + data #'+' order does matter here
            return data
        else:
            return data #not df
        
        
    def output(self, data):
        
        df = pd.DataFrame(data)
        df = df.drop_duplicates() #drop same line
        df.index = df['time'] #assign time to index
        df = df.drop(df.index[len(df)-1], axis=0) #drop last row since its contain variance
        
        #print('from_time: '+ self.time_convert(df.time[0]))
        #print('to_time: '+self.time_convert(df.time[len(df)-1]))
        
        if self.style == 'd' or self.style =='h' or self.style =='m':
                #df['return'] = df['close'].pct_change()
            df = df[['open','close','high','low']] #only reserve o c h l part for price data
            return df, 'price_'+self.param['fsym']+'_'+self.param['tsym']+'_'+self.style
        
        elif self.style == 'ed' or self.style =='eh':
            df = df['volume']
            return df, 'vol_'+self.param['fsym']+'_'+self.param['e']+'_'+self.style[1]
            
        
        
    def window_length(self, style, fromTs, toTs, w_limit):
        #compute window length associate with data frequency
        
        diff = toTs - fromTs
        if style == 'h' or style == 'eh':#h=3600s
            window_len = min(w_limit, int(np.ceil(diff/3600)))
        elif style == 'd' or style == 'ed':#d=86400s
            window_len = min(w_limit, int(np.ceil(diff/86400)))
        elif style == 'm':#m=60s
            window_len = min(w_limit, int(np.ceil(diff/60)))
            
        return window_len
    
    
    
    def _time_to(self,resp):
        time_to = resp['TimeTo']
        return time_to
    
    def time_convert(self,time_in):
        #convert timestamp to US/EST and viceversa
        if type(time_in) != str:
            time_in = int(time_in)
            #timestampe to US/EST
            date = datetime.datetime.utcfromtimestamp(time_in)
            utc = pytz.timezone('UTC')
            est = pytz.timezone('US/Eastern')
            fmt = '%Y-%m-%d %H:%M' 
            time_out = utc.localize(date,is_dst=None)
            time_out = time_out.astimezone(est).strftime(fmt)
            return time_out
        
        else:
            #US/EST to timestamp, input 'yyyy/mm/dd'
            date = datetime.datetime.strptime(time_in,"%Y/%m/%d")
            est = pytz.timezone('US/Eastern')
            utc=pytz.utc
            
            date_est=est.localize(date,is_dst=None)
            date_utc=date_est.astimezone(utc)
            return int(date_utc.timestamp())
            
         
        
        
        
#test      
if False: #__name__ == "__main__":
    obj = data_retrieve()
    data = obj.history_data('h',1559174400, {'fsym':'BTC','tsym':'USD','limit':200,'e':'Coinbase','toTs':1561852800})
    df, title = obj.output(data)
    
    #sample process
    #.history_data(freq style, fromTime, parameter{fsym: crypt, tsym: fiat, limit:<2000, e: exchang, toTs: until time}
    #.output(data) to load in Sqlite
    

