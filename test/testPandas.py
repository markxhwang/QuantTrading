#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import pprint
import datetime
import pandas

sys.path.append("../..")

from config import GlobalConfig

from optparse import OptionParser

if __name__ == '__main__':
    print("Hello world")
    config = GlobalConfig.Config()

    iniHolding = {}
    w = {}
    i = 1.0
    for ticker in ['SPY', 'IBM', 'AAPL']:
        iniHolding[ticker] = i
        w[ticker] = i * 2
        i += 1

    Holding = pandas.DataFrame(iniHolding, index=[datetime.date(2015, 12, 11)])
    print(Holding[-1:])
    df = pandas.DataFrame(Holding[-1:], index=[datetime.date(2015, 12, 12)])
    print('df:', df, '\n')
    Holding = Holding.append(df)
    value = pandas.DataFrame(w, index=[datetime.date(2015, 12, 11)])

    print('Holding:', Holding, '\n')
    print('value:', value, '\n')

    print('Holding * value', Holding * value, '\n')
    vv = Holding * value
    print("Sum Value:", vv.sum(axis=1), '\n')

