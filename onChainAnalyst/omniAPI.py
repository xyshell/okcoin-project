import requests
import json
import time
import pandas as pd


class OmniLayerAPI():

    def __init__(self):
        # have the base URL created to each new objection
        self.baseURL = 'https://api.omniexplorer.info'

    def __safe_request(self, url, addr):
        '''
        dictionary object contact all the info for a give address and url
        :param url: string
        :param addr: string
        :return: dictionary
        '''
        try:
            response = requests.post(url, data=addr, timeout=20)
        except Exception:
            print('Connection Failed. Reconnecting...')
            self.__safe_request(url)

        resp = json.loads(response.text)

        if response.status_code != 200:
            raise Exception(resp)

        return resp

    def cur_time(self, timestamp):
        '''
        :return: time
        '''
        now = time.localtime(timestamp)
        cur_time = time.strftime("%Y-%m-%d %H:%M:%S", now)
        return cur_time

    def get_balance(self, addr):
        '''
        :param addr: string
        :return: dataframe, balance info for a given address
        '''
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

    def crawl_page(self, url, addr, i):
        # get each page's info
        # update url to each page
        url = url + '/' + str(i)
        response = self.__safe_request(url, addr)
        response = response['transactions']
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

    def get_transactions(self, addr):
        # get transaction for a given address
        subURL = '/v1/transaction/address'
        url = self.baseURL + subURL
        # get page numbers
        pages = self.get_pages(url, addr)
        trans = pd.DataFrame()
        for i in range(pages):
            page_info = self.crawl_page(url, addr, i)
            page_info = pd.DataFrame(page_info)
            trans = trans.append(page_info)
        return trans

    def get_all_transactions(self):
        # return total transactions in the Tether network

        return None


if __name__ == '__main__':
    api = OmniLayerAPI()
    # addr = {'addr': '1EXoDusjGwvnjZUyKkxZ4UHEf77z6A5S4P'}
    # df = api.get_transactions(addr)
    addr = {'addr': '1NTMakcgVwQpMdGxRQnFKyb3G1FAJysSfz'}
    df = api.get_balance(addr)
    print(df)
