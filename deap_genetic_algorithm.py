import random
import multiprocessing

from numpy import inf
from pybacktest import Backtest, load_from_yahoo
from deap import base, creator, tools, algorithms
from ta import *


def evaluate(params, ohlc=None, strategy=None, metric='mpi', mintrades=10):
    fitness = None
    try:
        bt = Backtest(strategy(ohlc, *params))
        fitness = getattr(bt.stats, metric)
        if not fitness or getattr(bt.stats, 'trades') < mintrades:
            fitness = -inf
    except Exception, e:
        fitness = -inf
    print params, fitness
    return fitness,


def optimize(ohlc=None, strategy=None, metric='mpi', params=None, population=25, generations=10):
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    toolbox.register("params", random.randint, min(params), max(params))
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.params, len(params))
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", evaluate, ohlc=ohlc, strategy=strategy, metric=metric)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutUniformInt, low=min(params), up=max(params), indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)

    pool = multiprocessing.Pool()
    toolbox.register("map", pool.map)

    pop = toolbox.population(n=population)
    algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=generations, verbose=False)
    best = tools.selBest(pop, 1)[0]

    pool.close()
    return best


if __name__ == "__main__":
    # params = [60, 90]
    # print evaluate(params, ohlc=load_from_yahoo('AAPL', start='2000'), strategy=mav_cross_double)

    ohlc = load_from_yahoo('AAPL', start='2000')
    # TODO: ranges and step size? these numbers really just indicate parameter count
    strategy, params, population = mav_cross_double, [5, 100], 25
    #strategy, params = mav_cross_triple, [5, 50, 100], 100
    best = optimize(ohlc=ohlc, strategy=strategy, params=params, population=population)
    print 'Solution (fast period, slow period): %s\n' % best
    print Backtest(strategy(ohlc, *tuple(best))).summary()



