from pybacktest import Backtest, Optimizer, load_from_yahoo
from ta import *


if __name__ == "__main__":
    ohlc = load_from_yahoo('AAPL', start='2000')
    # fn, params = mav_cross_triple, {'fast': (50, 75, 5), 'medium': (80, 100, 5), 'slow': (100, 120, 5)}
    fn, params = mav_cross_double, {'fast': (5, 75, 5), 'slow': (25, 100, 10)}
    opt = Optimizer(fn, ohlc, params)
    best = opt.best_by('mpi')
    print best.head()
    ps = [best[p].values[0] for p in params.keys()]
    ps.reverse()
    print 'Solution (fast period, slow period): %s\n' % ps
    print Backtest(fn(ohlc, *tuple(ps))).summary()
