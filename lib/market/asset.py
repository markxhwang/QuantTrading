import pandas
import numpy

class Stock(object):
    def __init__(self, ticker, dataframe=None):
        self.ticker = ticker
        self.df = dataframe


