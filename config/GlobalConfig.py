import platform
import datetime
import os

from lib.util import csvutil

class Config(object):
    ''' Singleton Global Config class'''
    _instance = None

    def __init__(self):
        self.debugLevel = 0  # (Level 0 is print Nothing, 10 Prints everything)

        self.projectRoot = 'E:\Quant\QuantTrading\development\python'
        self.configDir = self.projectRoot + '\config'
        self.dataDir = self.projectRoot + '\..\..\data'
        self.quandlDir = self.dataDir + '\quandl\db'
        self.quandlStockDir = self.quandlDir + '\stocksWiki'
        self.quandlStockAllData = self.quandlStockDir + '\WIKI_20161007.csv'

        # self.dump()
        self.quandlwikiEquityList = ['WIKI/AAPL','WIKI/JNJ']

        self.ticker2QuandlPathMap = {"SPY":"GOOG/NYSE_SPY",
                                     "AAPL": "WIKI/AAPL",
                                     "VIX": "CBOE/VIX",
                                     "VVIX": "CBOE/VVIX",
                                     "VX1": "CHRIS/CBOE_VX1",
                                     "VX2": "CHRIS/CBOE_VX2",
                                     "FutS30": "CHRIS/CME_I31",
                                     "FutS10": "CHRIS/CME_N1U1",
                                     "T2y": "CHRIS/CME_TU1",
                                     "T10y": "CHRIS/CME_N1U1"
                                     }

        self.QuandlPath2tickerMap = {v: k for k, v in self.ticker2QuandlPathMap.items()}

        self.ticker2ReturnFieldMap = {"SPY": "Close",
                                      "AAPL": "Close",
                                      "VIX": "VIX Close",
                                      "VVIX": "VVIX",
                                      "VX1": "Settle",
                                      "VX2": "Settle",
                                      "FutS30": "Settle",
                                      "FutS10": "Settle",
                                      "T2y": "Last",
                                      "T10y": "Last"
                                     }

    def __new__(cls, *args, **kwargs):  # Override new method to define Config as singleton
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls, *args, **kwargs)
            cls._instance.__init__()
        return cls._instance






