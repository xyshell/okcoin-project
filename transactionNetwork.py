
# coding=UTF-8
#!/usr/bin/python

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


class Top100Trans():

    def __init__(self):
        # import address file for later research of address' id and exchange
        self.address = pd.read_csv('address.csv')

    def get_id(self, addr):
        result = self.address.loc[self.address['address'] == addr]
        addr_id = result['id']
        if len(addr_id) == 0:
            return addr
        else:
            addr_id.index = [0]
            return addr_id[0]

    def get_exchange(self, addr):
        result = self.address.loc[self.address['address'] == addr]
        exchange = result['exchange']
        if len(exchange) == 0:
            return addr
        else:
            exchange.index = [0]
            return exchange[0]

    def address_trans(self, trans):
        # only take the top 200 biggest transactions in amount
        topTrans = trans.sort_values(by='amount', ascending=False).iloc[:200, :]
        graph = nx.MultiDiGraph()
        for row in topTrans.iterrows():
            # row is tuple
            tran = row[1]
            sending = self.get_id(tran['sending_address'])
            receiver = self.get_id(tran['reference_address'])

            if sending not in graph.nodes():
                graph.add_node(sending)
            if receiver not in graph.nodes():
                graph.add_node(receiver)

            graph.add_edges_from([(sending, receiver)])

        nx.draw(graph, font_size=10, with_labels=True, size=10, pos=nx.circular_layout(graph))
        plt.show()

    def exchange_trans(self, trans):
        # only take the top 200 biggest transactions in amount
        topTrans = trans.sort_values(by='amount', ascending=False).iloc[:200, :]
        graph = nx.MultiDiGraph()
        for row in topTrans.iterrows():
            tran = row[1]
            sending = self.get_exchange(tran['sending_address'])
            receiver = self.get_exchange(tran['reference_address'])

            if sending not in graph.nodes():
                graph.add_node(sending)
            if receiver not in graph.nodes():
                graph.add_node(receiver)

            graph.add_edges_from([(sending, receiver)])

        nx.draw(graph, font_size=10, with_labels=True, size=10, pos=nx.shell_layout(graph))
        plt.show()


if __name__ == '__main__':

    transaction = pd.read_csv('tether_transactions_522647.csv')

    topTrans = Top100Trans()
    # test address transactions
    topTrans.address_trans(transaction)
    # test exchange transactions
    topTrans.exchange_trans(transaction)


