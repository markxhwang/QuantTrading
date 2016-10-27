import pandas
import numpy
import talib
import matplotlib.pyplot as plt

import statsmodels.api as statsmodel

import config.GlobalConfig
config = config.GlobalConfig.Config()

class Strats(object):
    def __init__(self, name, pd , thresthold):
        print("Constructing GapStrats Model ...")
        self.name = name  # Model or Ticker Name
        self.pd = pd   # Independent variable, pandas dataframe, normally should be [Open(t) - Close(t-1)]/Close(t-1)         in % format
                       # Dependent vairable,, pandas dataframe, should be (Close(t) - Open(t))/Open(t) for in sample fitting   in % format  all in pd dataframe
        self.thresthold = thresthold   #in % format
        self.intercept = None
        self.beta = None
        self.rsquared = None
        self.good = False
        self.model = None
        self.fittingSummary = None
        return

    def filterbyThreshold(self, pd):
        xx = pd.query("Open-PrevClose > self.thresthold or Open-PrevClose < -1*self.thresthold ")
        return xx


    def fit(self):
        print("Fitting GapStrats Model ...")
        # Create linear regression object

        mask = (self.pd['Open-PrevCloseChangePCT'] > self.thresthold) | (self.pd['Open-PrevCloseChangePCT'] < -1* self.thresthold)
        pd1 = self.pd.loc[mask]

        X = numpy.array(pd1["Open-PrevCloseChangePCT"])
        Y = numpy.array(pd1["Close-OpenChangePCT"])

        X = statsmodel.add_constant(X)
        model = statsmodel.OLS(Y,X).fit()

        self.intercept = model.params[0]
        self.beta = model.params[1]
        self.rsquared = model.rsquared
        self.model = model
        self.fittingSummary = model.summary()


        if ( self.beta < -0.2 ) and (self.rsquared > 0.2):
            self.good = True
            self.toReport()

            return True
        return False

    def predict(self, prevClose, currOpen):
        print("Running prediction using GapStrats Model ...")
        pct_change = (currOpen - prevClose) / prevClose
        if ( pct_change > self.thresthold) or ( pct_change < -1 * self.thresthold):
            return self.model.predict(pct_change)
        else:
            return 0
        return

    def toReport(self):
        print('---------------')
        print("Ticker:", self.name)

        print("Intercept:",self.intercept)
        print("Beta:",self.beta)
        print("R^2:",self.rsquared)
        print("Fitting Summary:",self.fittingSummary)
        print('---------------')
        return


