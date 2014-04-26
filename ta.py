import pandas as pd


def ma(s, n):
    """ Moving Average - N bar period """
    return pd.Series(pd.rolling_mean(s, n))


def crosses_over(a, b):
    return (a > b) & (a.shift() <= b.shift())


def crosses_under(a, b):
    return (a < b) & (a.shift() >= b.shift())


def mav_cross_double(ohlc, fast=50, slow=100):
    """ Simple stop and reverse double moving average crossover """
    ser = ohlc.C
    if fast > slow:
        raise ValueError('fast must be less than slow')
    mf, ms = ma(ser, fast), ma(ser, slow)
    buy, short = crosses_over(mf, ms), crosses_under(mf, ms)
    sell, cover = short, buy
    return dict(ohlc=ohlc, buy=buy, cover=cover, sell=sell, short=short)


def mav_cross_triple(ohlc, fast=50, medium=75, slow=100):
    """ Simple stop and reverse triple moving average crossover """
    ser = ohlc.C
    if not fast < medium < slow:
        raise ValueError('fast must be less than medium and medium must be less than slow')
    mf = ma(ser, fast)
    mm = ma(ser, medium)
    ms = ma(ser, slow)
    buy = crosses_over(mf, mm) & crosses_over(mf, ms)
    short = crosses_under(mf, mm) & crosses_under(mf, ms)
    sell, cover = short, buy
    return dict(ohlc=ohlc, buy=buy, cover=cover, sell=sell, short=short)


