import sys
import os
import pprint
import datetime
import pandas
import numpy
import logging
import talib
from lib.util import quant
import matplotlib.pyplot as plt

from matplotlib.backends.backend_pdf import PdfPages
from lib.util.plot import plot2multipagePdf

from pandas import DataFrame

sys.path.append("../..")

from config import GlobalConfig
import lib.market.quandl

from optparse import OptionParser

if __name__ == '__main__':
    config = GlobalConfig.Config()
    quandlobj = lib.market.quandl.Api()

    print("===========Downloand GOOG/NYSE_SPY stock historical EOD prices ==============")
    pd = quandlobj.getSingleNameHistoricalEod("SPY")
    pd = lib.util.quant.computeReturns("SPY",pd)

    pd = lib.util.quant.computeEMAs("SPY", pd)
    pp = PdfPages('Quandl.DataDownLoad.plots.pdf')
    fig = plt.figure()
    plotfields = ['Close', 'ema5', 'ema12', 'ema30', 'ema60', 'ema120']
    title = 'SPY and EMA series (5d, 12d, 30d, 60d, 120d)'
    plot2multipagePdf(pd , plotfields, title, fig, pp)

    fig = plt.figure()
    pd = lib.util.quant.computeBollingerBands("SPY", pd)
    plotfields = ['Close', 'BB.5d.upper', 'BB.5d.mid', 'BB.5d.lower']
    title = str(' ').join(['SPY: '] + ['Close', 'BB.5d.upper', 'BB.5d.mid', 'BB.5d.lower'])
    plot2multipagePdf(pd , plotfields, title, fig, pp)

    fig = plt.figure()
    pd = lib.util.quant.computeRSI("SPY", pd, 5)
    pd = lib.util.quant.computeRSI("SPY", pd, 12)
    pd = lib.util.quant.computeRSI("SPY", pd, 30)
    pd = lib.util.quant.computeRSI("SPY", pd, 60)
    plotfields = ['Close', 'RSI.5', 'RSI.12', 'RSI.30', 'RSI.60']
    title = str(' ').join(['SPY: '] + ['Close', 'RSI.5', 'RSI.12', 'RSI.30', 'RSI.60'])
    plot2multipagePdf(pd , plotfields, title, fig, pp)

    fig = plt.figure()
    pd,outfields = lib.util.quant.computeMACDs("SPY", pd)
    plotfields = ['Close'] + outfields
    title = str(' ').join(['SPY: '] + plotfields)
    plot2multipagePdf(pd , plotfields, title, fig, pp)

    fig = plt.figure()
    pd,outfields = lib.util.quant.computeHilbertTransformSignals("SPY", pd)
    plotfields = ['Close'] + outfields
    title = str(' ').join(['SPY: '] + plotfields)
    plot2multipagePdf(pd , plotfields, title, fig, pp)
    pp.close()


    print("===========Downloand CBOE / VIX ==============")
    pd = quandlobj.getSingleNameHistoricalEod("VIX")
    pd = quandlobj.computeReturns("VIX", pd)
    print(pd)

    exit()
    print("===========Downloand CHRIS/CBOE_VX1 stock historical EOD prices ==============")
    pd = quandlobj.getSingleNameHistoricalEod("VX1")
    print(pd)

    print("===========Downloand CHRIS/CBOE_VX2 stock historical EOD prices ==============")
    pd = quandlobj.getSingleNameHistoricalEod("VX2")
    print(pd)

    print("===========Downloand CBOE / VVIX ==============")
    pd = quandlobj.getSingleNameHistoricalEod("VVIX")
    print(pd)


    print("===========Downloand CHRIS/CME_I3 30Y IR Swap ==============")
    pd = quandlobj.getSingleNameHistoricalEod("FutS30")
    print(pd)


    print("===========Downloand CHRIS/CME_N1U 10Y IR Swap ==============")
    pd = quandlobj.getSingleNameHistoricalEod("FutS10")
    print(pd)


    print("===========Downloand CHRIS/CME_TU 2Y IR Swap ==============")
    pd = quandlobj.getSingleNameHistoricalEod("T2y")
    print(pd)


    print("===========Downloand CHRIS/CME_TY 10Y IR Swap ==============")
    pd = quandlobj.getSingleNameHistoricalEod("T10y")
    print(pd)

    print("===========Downloand WIKI/AAPL stock historical EOD prices ==============")
    pd = quandlobj.getSingleNameHistoricalEod("AAPL")





    exit()
    print("===========Downloand Entire YC Database from Quandl ==============")
    # quandlobj.downloadDatabase("YC",config.quandlStockDir)             # Needs premium subscription

    pd = pandas.DataFrame()
    for stock in config.quandlwikiEquityList:
        print("Reading quandl stocks:"+stock)
        pdstock = quandlobj.getSingleNameHistoricalEod(stock)
        print(pdstock)

