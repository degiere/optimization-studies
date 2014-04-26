from numpy import inf
from scipy.optimize import brute
from pybacktest import Backtest, load_from_yahoo
from ta import *


def cost(params, ohlc=None, fn=None):
    signals = fn(ohlc, *params)
    bt = Backtest(signals)
    try:
        sharpe = bt.report['risk/return profile']['sharpe']
        cost = 1.0 / sharpe
        print params, sharpe, cost
        return cost
    except Exception, e:
        cost = inf
        print params, None, cost
        return cost


if __name__ == "__main__":
    ohlc = load_from_yahoo('AAPL', start='2000')
    # TODO: multiprocessing?
    fn, params = mav_cross_double, [slice(5, 35, 5), slice(20, 110, 10)]
    res = brute(cost, params, args=(ohlc, fn), finish=None)
    print 'Solution (fast period, slow period): %s\n' % res
    print Backtest(fn(ohlc, *res)).summary()
