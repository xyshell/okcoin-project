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

class CCCandle1H(bt.feeds.GenericCSVData):
  params = (
    ('timeframe', bt.TimeFrame.Minutes),
    ('compression', 60),

    ('datetime', 7),
    ('time', 4),
    ('open', 3),
    ('high', 1),
    ('low', 2),
    ('close', 0),
    ('volume', 6),
    ('openinterest', -1)
)

class CCCandle4H(bt.feeds.GenericCSVData):
  params = (
    ('timeframe', bt.TimeFrame.Minutes),
    ('compression', 60*4),

    ('datetime', 7),
    ('time', 4),
    ('open', 3),
    ('high', 1),
    ('low', 2),
    ('close', 0),
    ('volume', 6),
    ('openinterest', -1)
)

class CCCandle1D(bt.feeds.GenericCSVData):
  params = (
    ('timeframe', bt.TimeFrame.Days),

    ('datetime', 7),
    ('time', 4),
    ('open', 3),
    ('high', 1),
    ('low', 2),
    ('close', 0),
    ('volume', 6),
    ('openinterest', -1)
)
