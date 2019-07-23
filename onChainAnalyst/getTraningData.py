import pandas as pd
import requests
import omniAPI

# global variable
rich_list = pd.read_csv('data/richlist.csv')
address_info = pd.read_csv('data/address_info.csv')


def get_transactions(addr_list, start_time='2014-01-01 00:00:00'):
    # return all transactions for a given list after a given time
    df = pd.DataFrame()
    for addr in addr_list:
        api = omniAPI.OmniLayerAPI()
        transactions = api.get_transactions({'addr': addr}, start_time)
        df = pd.concat([df, transactions])
    # One transaction will appear in 2 addresses' transaction record， thus need to drop duplicated one
    df = df.drop_duplicates(['block', 'positioninblock'])
    df = df.sort_values(by='blocktime', ascending=True)
    return df


def save_trans(new_trans):
    exist_trans = pd.read_csv('data/transactions.csv')
    total_trans = exist_trans.append(new_trans, ignore_index=True)
    total_trans = total_trans.drop_duplicates()
    total_trans = total_trans.sort_values(by='blocktime', ascending=True)
    total_trans.to_csv('data/transactions.csv', index = None)
    pass


def get_single_price(timestamp):
    '''
    Return tether price for a single timestamp
    '''
    timestamp = str(timestamp)
    url = 'https://min-api.cryptocompare.com/data/pricehistorical?'
    sub_url = 'fsym=USDT&tsyms=USD&ts=%s' % timestamp
    fianl_url = url + sub_url
    response = requests.get(fianl_url)
    resp = response.json()
    price = resp['USDT']['USD']
    return price


def save_price(new_price_list):
    # get data by time is very slow, 
    # thus every time we get price data from API
    # we will sava price data by this function to avoid future waste of time and CPU
    exit_price = pd.read_csv('data/price.csv')
    final_price = exit_price.append(new_price_list, ignore_index=True)
    final_price = final_price.drop_duplicates()
    final_price = final_price.sort_values(by='blocktime', ascending=True)
    final_price.to_csv('data/price.csv', index=None)
    return None


def get_price(timestamp_list):
    '''
    :param timestamp_list: list of timestamp
    :return: return Dataframe data contain timestamp and tether price
    '''
    exit_price = pd.read_csv('data/price.csv')
    price_list = pd.DataFrame(columns=['blocktime', 'price'])
    ts_list = timestamp_list.tolist()
    for ts in ts_list:
        if ts in exit_price['blocktime'].tolist():
            price = exit_price[exit_price['blocktime'] == ts].iloc[0, 1]
            # print(price)
        else:
            price = get_single_price(ts)
            # print(price)
        temp_dict = {'blocktime': ts, 'price': price}
        price_list = price_list.append(temp_dict, ignore_index=True)
    save_price(price_list)
    return price_list


def exchange_tpye(tran):
    sending_addr = address_info.loc[address_info['address'] == tran['sendingaddress']]
    reference_addr = address_info.loc[address_info['address'] == tran['referenceaddress']]
    if len(sending_addr) == 0 and len(reference_addr) == 0:
        exchange_type = 0
        return exchange_type

    if len(sending_addr) != 0 and len(reference_addr) == 0:
        exchange1 = sending_addr['exchange']
        if exchange1.iloc[0] == 'Poloniex':
            exchange_type = 2
        else:
            exchange_type = 0
        return exchange_type

    if len(sending_addr) == 0 and len(reference_addr) != 0:
        exchange2 = reference_addr['exchange']
        if exchange2.iloc[0] == 'Poloniex':
            exchange_type = 2
        else:
            exchange_type = 0
        return exchange_type

    else:
        exchange1 = sending_addr['exchange']
        exchange2 = reference_addr['exchange']

        if exchange1.iloc[0] == exchange2.iloc[0]:
            exchange_type = 1
        elif exchange1.iloc[0] == 'Poloniex' or exchange2.iloc[0] == 'Poloniex':
            exchange_type = 2
        else:
            exchange_type = 0

        return exchange_type


def add_exchange_type(transactions):
    dataset = pd.DataFrame(columns=['time', 'amount', 'exchange_type'])
    dataset[['time', 'amount']] = transactions[['blocktime', 'amount']]
    for i in range(len(transactions)):
        tran = transactions.iloc[i]
        dataset.iloc[i, 2] = exchange_tpye(tran)
    return dataset


def combine_same_time(transactions):
    dataset = pd.DataFrame(columns=['time', 'amount', 'exchange_type', 'transaction_times'])
    time_list = transactions['time'].tolist()
    time_list = list(set(time_list))
    time_list = sorted(time_list)
    for ts in time_list:
        sub_trans = transactions[transactions['time'] == ts]
        exchange_type = sub_trans['exchange_type'].tolist()
        exchange_type = list(set(exchange_type))
        exchange_type = sorted(exchange_type)
        for ex in exchange_type:
            total_amount = sub_trans[sub_trans['exchange_type'] == ex].sum()['amount']
            times = sub_trans[sub_trans['exchange_type'] == ex].count()['time']
            record = {'time': ts, 'amount': total_amount, 'exchange_type': ex, 'transaction_times': times}
            dataset = dataset.append(record, ignore_index=True)
    return dataset


def cpt_price_change(transactions):
    
    pass


if __name__ == '__main__':
    rich_list = pd.read_csv('data/richlist.csv')
    rich_list = rich_list['Address'].tolist()
    rich_list = rich_list[0:5]
    transactions = get_transactions(rich_list, '2019-07-01 00:00:00')

    save_trans(transactions)
    # transactions = pd.read_csv('data/transactions.csv')

    transactions = add_exchange_type(transactions)
    transactions = combine_same_time(transactions)
    
    ts_list = transactions['time']
    tether_price = get_price(ts_list)

    # merge transactions and tether price together
    transactions['price'] = tether_price['price']

    transactions.to_csv('data/dataset.csv', index=None)
    






