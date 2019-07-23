import requests
import json
import time
import pandas as pd
import util

global low_freq_tran_addr
low_freq_tran_addr = 0
global low_freq_tran_addr_list
low_freq_tran_addr_list = []

class OmniLayerAPI():

    def __init__(self):
        # have the base URL created to each new objection
        self.baseURL = 'https://api.omniexplorer.info'

    def __safe_request(self, url, addr):
        # try to connect, if unsuccessful, try again
        try:
            response = requests.post(url, data=addr, timeout=20)
            time.sleep(8)
        except Exception:
            print('Connection Failed. Reconnecting...')
            time.sleep(8)
            self.__safe_request(url, addr)
        resp = json.loads(response.text)
        if response.status_code != 200:
            return Exception(resp)
        # Here used to see how many data we get
        print('Safe Request========================')
        print(resp)

        return resp

    def get_balance(self, addr):
        # return balance for a give address
        subURL = '/v1/address/addr'
        response = self.__safe_request(self.baseURL + subURL, addr)
        response = response['balance']
        df = pd.DataFrame(response)
        return df

    def get_pages(self, url, addr):
        # get pages
        resp = self.__safe_request(url, addr)
        pages = resp['pages']
        return pages

    def valid_trans(self, response):
        # to see weather data are valid data
        # import dictionary, output list
        valid_trans = []
        for line in response:
            flag = True
            # d_time = self.cur_time(line['blocktime'])
            if 'valid' not in line.keys():
                flag = False
            if line['valid'] == False:
                flag = False
            if 'amount' not in line.keys():
                flag = False
            if flag:
                valid_trans.append(line)
        return valid_trans

    def crawl_page(self, url, addr, i):
        # get each page's info
        # update url to each page
        url = url + '/' + str(i)
        response = self.__safe_request(url, addr)
        response = response['transactions']
        valid_trans = self.valid_trans(response)
        return valid_trans

    def get_transactions(self, addr, start_time='2016-01-01 00:00:00'):
        # get transaction for a given address after given time
        # 2016-01-01 set as default to return all transactions
        subURL = '/v1/transaction/address'
        url = self.baseURL + subURL
        # transfer string type time to timestamp
        timestamp = util.str_to_tstp(start_time)
        # get page numbers
        pages = self.get_pages(url, addr)
        trans = pd.DataFrame()
        if pages == 1:
            # If there are only 1 page, read all transactions of that address
            global low_freq_tran_addr
            low_freq_tran_addr += 1
            global low_freq_tran_addr_list
            low_freq_tran_addr_list += [addr['addr']]
            response = self.__safe_request(url, addr)
            response = response['transactions']
            page_info = self.valid_trans(response)
            trans = trans.append(page_info)
        else:
            for i in range(pages):
                # sleep 8 seconds after each call since there are 30s limit on each 5 calls
                page_info = self.crawl_page(url, addr, i)
                if page_info[1]['blocktime'] < timestamp:
                    break
                page_info = pd.DataFrame(page_info)
                trans = trans.append(page_info)
        return trans


if __name__ == '__main__':
    # test
    api = OmniLayerAPI()
    addr = {'addr': '1PWTgtguDTcEXUCAqF2BMgKypsyuEGGJai'}

    print('All transactions for a give address')
    df1 = api.get_transactions(addr)
    print(df1)
    print(low_freq_tran_addr_list)

    print('All transactions for a give address after a given time')
    df2 = api.get_transactions(addr, '2019-06-01 00:00:00')
    print(df2)
