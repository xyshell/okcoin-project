# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 15:22:29 2019

@author: chang
"""

from data_storage import data_storage
import datetime
import pytz
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa import stattools
from statsmodels.stats.diagnostic import unitroot_adf
from statsmodels.tsa.seasonal import seasonal_decompose




class data_analyze():
    
    def __init__(self):#initial a df_list to contain dfs
        
        self.df_list = []
        self.test_df_list = []
    
    def adding_df(self, obj): #add new df to df_list 
        if type(obj) == pd.DataFrame:
            self.df_list.append(obj)
            
        elif type(obj) == list:
            self.df_list = self.df_list + obj
        else:
            raise ValueError('unsupport adding obj!! \n')
    
    def time_convert(self,time_in):#convert timestamp to US/EST and vice versa 
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
            if time_in[4] == '/':
                date = datetime.datetime.strptime(time_in,"%Y/%m/%d")
            elif time_in[4] == '-':
                date = datetime.datetime.strptime(time_in,"%Y-%m-%d")
            else:
                raise ValueError('\n unsupport time format! \n')
            est = pytz.timezone('US/Eastern')
            utc=pytz.utc
            
            date_est=est.localize(date,is_dst=None)
            date_utc=date_est.astimezone(utc)
            return int(date_utc.timestamp())
        
    def covert_to_test_df(self): #create&update 'test_df_list' and transfer each df in df_list to analysiable df
                                 #test_df_list contain df as US_eastern_time index, timestamp and returns
        new_list = []
        for df in self.df_list:
            returns = df['close'].pct_change()
            #create datetime index
            index = pd.to_datetime( df['time'].apply(self.time_convert) )
            new_df = pd.DataFrame({'index':index,'close':df['close'], 'timestamp':df['time'], 'return':returns})
            new_df = new_df.set_index('index')
            new_list.append(new_df)
        self.test_df_list = new_list
    
    def rolling_mean_std(self, test_df, plot=False):

        if (test_df['timestamp'][1] - test_df['timestamp'][0]) == 60:
            rolmean = pd.rolling_mean(test_df['return'], window=60)
            rolstd = pd.rolling_std(test_df['return'], window=60)

        elif (test_df['timestamp'][1] - test_df['timestamp'][0]) == 3600:
            rolmean = pd.rolling_mean(test_df['return'], window=24)
            rolstd = pd.rolling_std(test_df['return'], window=24)
        else:
            raise ValueError('\n unsupport data freq ! \n')
            
        if plot:
            #Plot rolling statistics:
            plt.figure(figsize=(10,5))
            plt.grid()
            orig = plt.plot(test_df['return'], color='blue',label='Obv', alpha=0.5, lw=0.7)
            mean = plt.plot(rolmean, color='red', label='Rolling Mean',lw=0.7)
            std  = plt.plot(rolstd, color='orange', label = 'Rolling Std',lw=0.7)
            plt.legend(loc='best')
            plt.title('Rolling Mean & Standard Deviation')
            plt.xticks(rotation=50)
            plt.show(block=False)
            
            plt.figure(figsize=(10,5))
            plt.grid()
            mean = plt.plot(rolmean, color='red', label='Rolling Mean',lw=0.7)
            std  = plt.plot(rolstd, color='orange', label = 'Rolling Std',lw=0.7)
            plt.legend(loc='best')
            plt.title('Rolling Mean & Standard Deviation')
            plt.xticks(rotation=50)
            plt.show(block=False)

        return {'rolling_mean': rolmean, 'rolling_std': rolstd}
    
    def stationary_test(self, test_df, plot = False):
        
        acf = stattools.acf(test_df['return'][1::], nlags=10)
        pacf = stattools.pacf(test_df['return'][1::], nlags=10)
        ADF = unitroot_adf(test_df['return'][1::])
    
        if plot:
            #plt.figure(figsize = (10,10))
            plt.stem(acf)
            plt.title('ACF')
            plt.show()
            #plt.figure(figsize = (10,10))
            plt.stem(pacf)
            plt.title('PACF')
            plt.show()
        
        return {'acf':acf, 'pacf': pacf, 'adf': ADF}
    
    def seasonality_return_decomp(self, test_df, f = 0, plot = False):
        if f == 0:
            raise ValueError('\nError freqency input!! \n')
            
        obv = test_df['return'][1::]
        
        if test_df['timestamp'][1] - test_df['timestamp'][0] == 60:
            
            raise ValueError('\n Wrong using minute data! \n')
            
        #since 'return[0]' is nan     
        decomposition = seasonal_decompose(obv, freq=f, model='additive')
        trend = decomposition.trend
        seasonal = decomposition.seasonal
        residual = decomposition.resid
        ADF = unitroot_adf(test_df['return'][1::])
        
        if plot:
            plt.figure(figsize=(15,10)) 
            plt.subplot(411)
            plt.plot(obv,label = 'obv', lw = 0.7)
            plt.legend(loc='best')
            plt.subplot(412)
            plt.plot(trend,label = 'trend', lw = 0.7)
            plt.legend(loc='best')
            plt.subplot(413)
            plt.plot(seasonal,label = 'seasonal', lw = 0.7)
            plt.legend(loc='best')
            plt.subplot(414)
            plt.plot(residual,label = 'residual', lw = 0.7)
            plt.legend(loc='best')
            plt.show()
            
            print('stats =',ADF[0], 'Alpha =',ADF[4])
            if ADF[0] < ADF[4]['1%']:
                print('\nResidual is stable in 99% confid. interval')
            
        return {'trend':trend, 'seasonal':seasonal, 'residual': residual, 'adf':ADF}
        
        
    def seasonality_price_decomp(self, test_df, f = 0, plot = False):
        if f == 0:
            raise ValueError('\nError freqency input!! \n')
            
        obv = test_df['close']
        
        if test_df['timestamp'][1] - test_df['timestamp'][0] == 60:
            
            raise ValueError('\n Wrong using minute data! \n')
            
        #since 'return[0]' is nan     
        decomposition = seasonal_decompose(obv, freq=f, model='additive')
        trend = decomposition.trend
        seasonal = decomposition.seasonal
        residual = decomposition.resid
        ADF = unitroot_adf(test_df['return'][1::])
        
        if plot:
            plt.figure(figsize=(15,10)) 
            plt.subplot(411)
            plt.plot(obv,label = 'obv', lw = 0.7)
            plt.legend(loc='best')
            plt.subplot(412)
            plt.plot(trend,label = 'trend', lw = 0.7)
            plt.legend(loc='best')
            plt.subplot(413)
            plt.plot(seasonal,label = 'seasonal', lw = 0.7)
            plt.legend(loc='best')
            plt.subplot(414)
            plt.plot(residual,label = 'residual', lw = 0.7)
            plt.legend(loc='best')
            plt.show()
            
            print('stats =',ADF[0], 'Alpha =',ADF[4])
            if ADF[0] < ADF[4]['1%']:
                print('\nResidual is stable in 99% confid. interval')
            
        return {'trend':trend, 'seasonal':seasonal, 'residual': residual, 'adf':ADF}
            



if False: #__name__ == '__main__':
    
    stor = data_storage('crypto_base.sqlite')
    GUSD_USD_m = stor.dump_data('price_GUSD_USD_m')
    GUSD_USD_h = stor.dump_data('price_GUSD_USD_h')
    ETH_USD_d = stor.dump_data('price_ETH_USD_d')
    DAI_USD_h = stor.dump_data('price_DAI_USD_h')
    
    
    obj = data_analyze()
    obj.adding_df( [GUSD_USD_m, GUSD_USD_h, ETH_USD_d, DAI_USD_h])
    obj.covert_to_test_df()
    
    temp_test_df_list = obj.test_df_list
    
    test_df_gusd_m = temp_test_df_list[0]
    test_df_gusd_h = temp_test_df_list[1]
    test_df_eth_d = temp_test_df_list[2]
    test_df_dai_h = temp_test_df_list[3]
    

    #plt.figure()
    #plt.plot(BTC_min.index, BTC_min_r)
    #plt.show()