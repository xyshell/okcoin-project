import backtrader as bt
import pandas as pd
import datetime
from CandleFmt import CCCandle1H, CCCandle4H, CCCandle1D
from utils import CC_IGNIS_1H, CC_IGNIS_4H, CC_IGNIS_1D

class TempStrat(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.datetime(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.sma1 = bt.ind.SMA(period=5)  # fast moving average
        self.sma2 = bt.ind.SMA(period=10)  # slow moving average
        self.sma3 = bt.ind.SMA(period=20)  # slow moving average
        # self.sma4 = bt.ind.SMA(period=30)  # slow moving average
        self.sma_cdl1 = bt.ind.CrossDown(self.sma1, self.sma2, plotname='sma_crossdown_level1')

        self.long_head0 = self.datas[0].close > self.sma1
        self.long_head1 = self.sma1 > self.sma2
        self.long_head2 = self.sma2 > self.sma3
        self.long_headl1 = bt.And(self.long_head0, self.long_head1)
        self.long_headl2 = bt.And(self.long_head0, self.long_head1, self.long_head2)
        bt.LinePlotterIndicator(self.long_headl2, name='long_head_level2')

        self.obv = bt.talib.OBV(self.datas[0].close, self.datas[0].volume)
        self.obv5 = bt.ind.SMA(self.obv, period=5)
        self.obv10 = bt.ind.SMA(self.obv, period=10)
        self.obv_cul1 = bt.ind.CrossOver(self.obv5, self.obv10, plotname='obv_crossup_level1')

        self.mom1= self.datas[0].close > self.datas[0].close (-1)
        self.mom2= self.datas[0].close (-1) > self.datas[0].close (-2)
        self.mom3= self.datas[0].close (-2) > self.datas[0].close (-3)
        # self.mom4= self.datas[0].close (-3) > self.datas[0].close (-4)
        # self.mom5= self.sma1(-4) > self.sma1(-5)

        self.moml1 = bt.And(self.mom1, self.mom2, self.mom3)
        # self.moml5 = bt.And(self.mom1, self.mom2, self.mom3, self.mom4, self.mom5)

    def prenext(self):
        if len(self) == 30:
            self.buy()
            self.log('Long Position, %.4f' % self.datas[0].close[0])
    
    def next(self):
        dt = self.datas[0].datetime.datetime(0)
        close = self.datas[0].close[0]
        self.log('Price, %.4f' % close)

        if self.obv_cul1 > 0 and self.long_headl2:
            self.buy()

        elif self.long_headl2 and self.obv5 > self.obv10:
            self.buy()
        
        if self.sma_cdl1:
            self.close()
        
        # target_percent = (int(self.sma1[0] > self.sma2[0]) + int(self.sma1[0] > self.sma2[0]) + int(self.sma1[0] > self.sma3[0]))/3
        # port_value = self.broker.get_value() - self.broker.get_cash()
        # total_value = self.broker.get_value()
        # now_percent = port_value / total_value
        # if abs(now_percent - target_percent) < 0.1:
        #     self.log(f'now_percent:{now_percent}, target_percent:{target_percent}')
        #     return
        # else:
        #     if now_percent < target_percent and close < self.maxn[0]:
        #         return
        #     self.order_target_percent(target=target_percent)
        #     self.log(f'Long to {target_percent} at {close}')

    

    # def next(self):
    #     # Simply log the closing price of the series from the reference
    #     if not self.position:  # not in the market
    #         if self.crossover > 0:  # if fast crosses slow to the upside
    #             self.buy()  # enter long
    #             self.log('Long Position, %.2f' % self.datas[0].close[0])
        
    #     elif self.crossover < 0:  # in the market & cross to the downside
    #         self.close()  # close long position
    #         self.log('Close Position, %.2f' % self.datas[0].close[0])   
    
    # def stop(self):
    #     self.log('(MA_fast %2d, MA_slow %2d) Ending Value %.2f' %
    #             (self.p.pfast, self.p.pslow, self.broker.getvalue()), doprint=True)

if __name__ == '__main__':

    # backtest from the best result
    cerebro = bt.Cerebro(stdstats=True)   
    data = CCCandle4H(
        dataname=CC_IGNIS_4H, 
        dtformat= "%Y-%m-%d",
        tmformat= "%H:%M:%S",
        fromdate= datetime.datetime(2019, 6, 1),
        todate= datetime.datetime(2019, 7, 14),
    )
    cerebro.adddata(data)
    cerebro.addstrategy(TempStrat)
    cerebro.addsizer(bt.sizers.PercentSizer, percents=95)
    cerebro.broker.set_cash(1000000)
    cerebro.broker.setcommission(commission=0.001)
    cerebro.run()

    cerebro.plot(style='candlestick', barup='green', bardown='red')
    
