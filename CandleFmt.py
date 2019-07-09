import backtrader as bt

class CAWCandleData(bt.feeds.GenericCSVData):
  params = (
    ('datetime', 0),
    ('open', 1),
    ('high', 2),
    ('low', 3),
    ('close', 4),
    ('volume', 5),
    ('openinterest', -1)
)

class CCCandleData(bt.feeds.GenericCSVData):
  params = (
    ('datetime', 7),
    ('open', 3),
    ('high', 1),
    ('low', 2),
    ('close', 0),
    ('volume', 6),
    ('openinterest', -1)
)
