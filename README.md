optimization-studies
====================

Trading system optimization algorithm studies.

There is a good brute force multiprocessing enabled optimizer built into pybacktest. Anything north of two
input parameters takes a very long time to optimize on large historical data sets.

Looking to the usual suspects, SciPy has general purpose optimization functionality but no simple multiprocessing
support like pybacktest and DEAP.

DEAP offers a variety of evolutionary algorithms, which may not always find global maxima, but can handle a large
number of parameters efficiently. Multiprocessing and grid capabilities also speed the process up.

* [Pybacktest](http://github.com/ematvey/pybacktest/) - Simple backtesting and optimization framework
* [SciPi Optimization](http://docs.scipy.org/doc/scipy/reference/tutorial/optimize.html) - Optimization algorithms
* [DEAP](https://code.google.com/p/deap/) - Distributed evolutionary algorithms