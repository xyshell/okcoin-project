import backtrader as bt
import pandas as pd
import datetime
from CandleFmt import CCCandleData
from utils import CC_DATA_PATH_1D

class SmaCross(bt.Strategy):
    params = (
        ('pfast', 10),  # period for the fast moving average
        ('pslow', 30),  # period for the slow moving average
        ('printlog', False),
    )

    def log(self, txt, dt=None, doprint=False):
        ''' Logging function fot this strategy'''
        if self.p.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        sma1 = bt.ind.SMA(period=self.p.pfast)  # fast moving average
        sma2 = bt.ind.SMA(period=self.p.pslow)  # slow moving average
        self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.datas[0].close[0])

        if not self.position:  # not in the market
            if self.crossover > 0:  # if fast crosses slow to the upside
                self.buy()  # enter long
                self.log('Buy, %.2f' % self.datas[0].close[0])
        
        elif self.crossover < 0:  # in the market & cross to the downside
            self.close()  # close long position
            self.log('Close, %.2f' % self.datas[0].close[0])    

    def stop(self):
        opt_result_dict['_'.join([str(self.p.pfast), str(self.p.pslow)])] = self.broker.getvalue()
        self.log('(MA_fast %2d, MA_slow %2d) Ending Value %.2f' %
                 (self.p.pfast, self.p.pslow, self.broker.getvalue()), doprint=True)


if __name__ == '__main__':

    # optimize param
    opt_result_dict = {}
    cerebro = bt.Cerebro()
    data = CCCandleData(
        dataname=CC_DATA_PATH_1D, 
        dtformat= '%Y-%m-%d %H:%M:%S',
    )
    cerebro.adddata(data)
    strats = cerebro.optstrategy(
        SmaCross,
        pfast=range(5, 30, 5),
    )
    cerebro.addsizer(bt.sizers.PercentSizer, percents=95)
    cerebro.broker.set_cash(1000000)
    cerebro.broker.setcommission(commission=0.0)
    cerebro.run(maxcpus=1)
    
    opt_result = pd.Series(opt_result_dict)
    pfast, pslow = [int(i) for i in opt_result.idxmax().split('_')]
    print(f"pfast:{pfast}, pslow:{pslow}")

    # backtest from the best result
    cerebro = bt.Cerebro()   
    data = CCCandleData(
        dataname=CC_DATA_PATH_1D, 
        dtformat= '%Y-%m-%d %H:%M:%S',
    )
    cerebro.adddata(data)
    cerebro.addstrategy(SmaCross, pfast=pfast, pslow=pslow)
    cerebro.addsizer(bt.sizers.PercentSizer, percents=95)
    cerebro.broker.set_cash(1000000)
    cerebro.broker.setcommission(commission=0.0)
    cerebro.run(maxcpus=1)

    cerebro.plot()
    
