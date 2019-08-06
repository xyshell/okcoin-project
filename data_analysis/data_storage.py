# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 00:25:18 2019

@author: Owner
"""
import sqlite3
import pandas as pd

class data_storage():
    
    def __init__(self, db_name):
        
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()
        
    def load_data(self, df, table_name='', drop_duplicate = True):
        #load df into sqlite db
        
        if len(table_name)<1:
            raise Exception('unsupport load table_name ! \n')
        
        try:
            df.to_sql(table_name, self.con, if_exists = 'append')
            table = pd.Series(table_name)
            table = table.to_frame('titles')
            table.to_sql('table_titles', self.con, if_exists = 'append')       
            del table
        
        except Exception:
            print('Error in load_data')
        
        #modify database to drop duplicates
        if drop_duplicate:
            self.drop_duplicates(table_name)
            
        
            
    def dump_data(self, table_name):
        #dump table back to df
        #del all zero slides
        
        if len(table_name)<1:
            raise Exception('unsupport dump table_name ! \n')
            
        df = pd.read_sql_query('''SELECT * FROM {}'''.format(table_name), self.con) #提取db
        
        temp = df['time']
        del df['time'] 
        df = df.ix[~(df==0).all(axis=1), :]  # del all 0 roll
        df['time'] = temp

        return df
    
        
    def drop_duplicates(self, table_name):
        
        temp_df = pd.read_sql_query('''SELECT * FROM {}'''.format(table_name), self.con) #提取db
        temp_df = temp_df.drop_duplicates()
        temp_df.to_sql(table_name, self.con, if_exists = 'replace', index = False)
        
        del temp_df        
                
    def commit(self):
        self.con.commit()
        self.con.close()
    
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
    
    
if False:#__name__ == '__main__':
    from data_retrival import data_retrieve
    
    obj = data_storage("crypto_base.sqlite")
    obj.load_data(df, 'test_table2')
    obj.drop_duplicates('test_table')
    
    #sample process:
    #create obj data_storage('.sqlite')
    #.load_data(df, 'table_name', drop_duplicate = True)
    #.dump_data('table_name')
   