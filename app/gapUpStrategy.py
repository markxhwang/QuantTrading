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
from pandas import HDFStore


from matplotlib.backends.backend_pdf import PdfPages
from lib.util.plot import plot2multipagePdf

from pandas import DataFrame

sys.path.append("../..")

from config import GlobalConfig
import lib.market.quandl
from lib.util.GapStrats import Strats as GapStrats

from optparse import OptionParser

if __name__ == '__main__':
    config = GlobalConfig.Config()
    quandlobj = lib.market.quandl.Api()


    #quandlobj.downloadDatabase("WIKI", config.quandlStockDir)
    #with zipfile.ZipFile(config.quandlStockDir + "/WIKI.zip", "r") as zip_ref:
    #    zip_ref.extractall(config.quandlStockDir)

    #df_wikidb = pandas.read_csv(config.quandlStockDir + "/WIKI_20161014.csv",names=['Ticker', 'Open.unadj', 'High.unadj','Low.unadj','Close.unadj','Vol.unadj','Open','High','Low','Close','Vol'] , low_memory=False, nrows= 5000000)


    filename = config.quandlStockDir + "/WIKI_20161014.csv"
    #num_lines = sum(1 for line in open(filename))
    #print("Total number of lines in file %s is %s:" %(filename, num_lines))


    #store = pandas.HDFStore('pandas.HDFstore.h5', mode='w')

    mTrainedModel = {}            # Stores the trained model with stock ticker as key

    #for i in range(0,1):
        #df_wikidb_chunk = pandas.read_csv(filename, header = None, usecols=[0,1,9,12],names=['Ticker','Date', 'Open','Close'], index_col = [1], low_memory=False, nrows= 18035)         #2000000
    #    df_wikidb_chunk = pandas.read_csv(filename, header=None, usecols=[0, 1, 9, 12],
        #                                  names=['Ticker', 'Date', 'Open', 'Close'], index_col=[1], low_memory=False,
         #                                 nrows=2000000)  # 2000000
    for df_wikidb_chunk in pandas.read_csv(filename, header=None, usecols=[0, 1, 9, 12], names=['Ticker', 'Date', 'Open', 'Close'], index_col=[1], low_memory=False, chunksize=5000000) : # 2000000

        for stock in df_wikidb_chunk.loc[:,'Ticker'].unique():
            print("\n=======================%s========================== \n" %(stock))
            #print("Stock ",stock, df_wikidb.loc[df_wikidb.Ticker == stock, 'Close'])
            quotes = df_wikidb_chunk.loc[df_wikidb_chunk.Ticker == stock, :].dropna()

            insample = quotes[:'2015-01-01']          # Define in sample fitting period
            if (insample.empty): break

            insample["Open-PrevCloseChangePCT"] = (insample["Open"] - insample["Close"].shift(1))/insample["Close"].shift(1)
            insample["Close-OpenChangePCT"] = (insample["Close"] - insample["Open"])/insample["Open"]

            GapStratsObj = GapStrats(stock, insample.dropna() , thresthold = 0.01)

            try:
                flag = GapStratsObj.fit()            # If return = True, means beta < -0.5 and in sample R^2 > 0.2, select the model for out of sample test
            except:
                pass

            if (flag):
                mTrainedModel[stock] = GapStratsObj

        print("\n==============In sample fitting finished ============ \n" )
        print("All selected models are:")
    print(mTrainedModel.keys())

    exit()

    if (1 ==1):
        for stock in mTrainedModel.keys():
             mTrainedModel[stock].toReport()

        # ============ Out of sample period ===========
        for stock in df_wikidb_chunk.loc[:, 'Ticker'].unique():
             print("\n=======================%s========================== \n" % (stock))
             # print("Stock ",stock, df_wikidb.loc[df_wikidb.Ticker == stock, 'Close'])
             quotes = df_wikidb_chunk.loc[df_wikidb_chunk.Ticker == stock, :].dropna()

             insample = quotes['2015-01-02':]  # Define in sample fitting period

             if (stock in mTrainedModel.keys()):
                 for index, row in insample.iterrows():
                    xhat = GapStratsObj.predict(row['Close'].shift(1),row['Open'])
                    xtrue = insample['Close'] - insample['Open']
                    print("Prediction for stock  %s, xhat = %s, xtrue = %s" % (stock,xhat,xtrue))





    exit()

    print("===========Downloand GOOG/NYSE_SPY stock historical EOD prices ==============")
    pd = quandlobj.getSingleNameHistoricalEod("SPY")
    pd = lib.util.quant.computeReturns("SPY",pd)

    pd = lib.util.quant.computeEMAs("SPY", pd)
    pd = lib.util.quant.computeBollingerBands("SPY", pd)

    pd = lib.util.quant.computeRSI("SPY", pd, 5)
    pd = lib.util.quant.computeRSI("SPY", pd, 12)
    pd = lib.util.quant.computeRSI("SPY", pd, 30)
    pd = lib.util.quant.computeRSI("SPY", pd, 60)

    pd,outfields = lib.util.quant.computeMACDs("SPY", pd)
    print(pd.tail(10))
