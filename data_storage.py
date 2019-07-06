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
        
    def load_data(self, df, table_name='', drop_duplicate = False):
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
        
        if len(table_name)<1:
            raise Exception('unsupport dump table_name ! \n')
            
        df = pd.read_sql_query('''SELECT * FROM {}'''.format(table_name), self.con) #提取db
        return df
    
        
    def drop_duplicates(self, table_name):
        
        temp_df = pd.read_sql_query('''SELECT * FROM {}'''.format(table_name), self.con) #提取db
        temp_df = temp_df.drop_duplicates()
        temp_df.to_sql(table_name, self.con, if_exists = 'replace', index = False)
        
        del temp_df        
                
    def commit(self):
        self.con.commit()
        self.con.close()
    
    
    
if False:#__name__ == '__main__':
    from data_retrival import data_retrieve
    
    x = data_storage("crypto_base.sqlite")
   
    x.load_data(df, 'test_table2')
    
    x.drop_duplicates('test_table')
   