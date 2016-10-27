import sys
import os
import pprint
import datetime
import pandas
import numpy
import logging
from lib.util import quant
import matplotlib.pyplot as plt

from matplotlib.backends.backend_pdf import PdfPages
from lib.util.plot import plot2multipagePdf

from pandas import DataFrame

sys.path.append("../..")

from config import GlobalConfig
import lib.market.quandl
import zipfile

from optparse import OptionParser

if __name__ == '__main__':
    config = GlobalConfig.Config()
    quandlobj = lib.market.quandl.Api()

    #quandlobj.downloadDatabase("WIKI", config.quandlStockDir)
    #with zipfile.ZipFile(config.quandlStockDir + "/WIKI.zip", "r") as zip_ref:
    #    zip_ref.extractall(config.quandlStockDir)

    #df_wikidb = pandas.read_csv(config.quandlStockDir + "/WIKI_20161014.csv",names=['Ticker', 'Open.unadj', 'High.unadj','Low.unadj','Close.unadj','Vol.unadj','Open','High','Low','Close','Vol'] , low_memory=False, nrows= 5000000)

    '''df_wikidb = pandas.read_csv(config.quandlStockDir + "/WIKI_20161014.csv",header = None, usecols=[0,1],
                                names=['Ticker','Date', 'Open.unadj', 'High.unadj', 'Low.unadj', 'Close.unadj', 'Vol.unadj',
                                       'Open', 'High', 'Low', 'Close', 'Vol'], low_memory=False, nrows= 10000)'''

    filename = config.quandlStockDir + "/WIKI_20161014.csv"
    #num_lines = sum(1 for line in open(filename))
    #print("Total number of lines in file %s is %s:" %(filename, num_lines))

    df_wikidb = pandas.read_csv(filename, header = None, usecols=[0,1,9,12],names=['Ticker','Date', 'Open','Close'], index_col = [1,0], low_memory=False, nrows= 18035)         #2000000


    print(df_wikidb.tail(10))
    print(df_wikidb.columns)
    print(df_wikidb.index.names)
    exit()

    #del df_wikidb['Open.unadj']
    #del df_wikidb['High.unadj']
    #del df_wikidb['Low.unadj']
    #del df_wikidb['Close.unadj']
    #del df_wikidb['Vol.unadj']
    print(df_wikidb.tail(1))
    print("==============")
    print(df_wikidb['Open'].tail(1))




    exit()
    # ====================== Get each stock from configuration one by one =======
    pd_wiki = pandas.read_csv(config.configDir + '\Quandl.WIKI.def.csv')
    quandlwikiEquityList = numpy.array(pd_wiki["QuandlKey"])
    for stockPath in quandlwikiEquityList:
        print("Reading quandl stocks:" + stockPath)
        pdstock = quandlobj.getSingleQuandlTsByKey(stockPath)
        print(pdstock.tail(5))

