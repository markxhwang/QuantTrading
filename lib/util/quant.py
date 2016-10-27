import pandas
import numpy
import talib

import config.GlobalConfig
config = config.GlobalConfig.Config()

def computeReturns(ticker, pd):
    closeField = config.ticker2ReturnFieldMap[ticker]
    pd["r1d"] = pd[closeField].pct_change(1)
    pd["r1w"] = pd[closeField].pct_change(5)
    pd["r1m"] = pd[closeField].pct_change(22)
    pd["r1q"] = pd[closeField].pct_change(63)
    pd["r2q"] = pd[closeField].pct_change(126)
    pd["r1y"] = pd[closeField].pct_change(255)
    return pd

def computeReturn(ticker, pd, period):
    closeField = config.ticker2ReturnFieldMap[ticker]
    pd["r." + period + '.days'] = pd[closeField].pct_change(period)
    return pd

def computeEMAs(ticker, pd):
    closeField = config.ticker2ReturnFieldMap[ticker]
    pd['ema5'] = talib.EMA(numpy.array(pd[closeField]), timeperiod=5)
    pd['ema12'] = talib.EMA(numpy.array(pd[closeField]), timeperiod=12)
    pd['ema30'] = talib.EMA(numpy.array(pd[closeField]), timeperiod=30)
    pd['ema60'] = talib.EMA(numpy.array(pd[closeField]), timeperiod=60)
    pd['ema120'] = talib.EMA(numpy.array(pd[closeField]), timeperiod=120)
    return pd

def computeEMA(ticker, pd, period):
    closeField = config.ticker2ReturnFieldMap[ticker]
    pd['ema' + period] = talib.EMA(numpy.array(pd[closeField]), timeperiod=period)
    return pd

def computeBollingerBands(ticker, pd):
    closeField = config.ticker2ReturnFieldMap[ticker]
    BBupperband, BBmiddleband, BBlowerband = talib.BBANDS(numpy.array(pd[closeField]), timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)
    pd['BB.5d.upper'] = BBupperband
    pd['BB.5d.mid'] = BBmiddleband
    pd['BB.5d.lower'] = BBlowerband
    return pd

def computeMACDs(ticker, pd):
    closeField = config.ticker2ReturnFieldMap[ticker]
    close = numpy.array(pd[closeField])
    macd, macdsignal, macdhist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    pd['MACD.12.26.9.macd'] = macd
    pd['MACD.12.26.9.macdsignal'] = macdsignal
    pd['MACD.12.26.9.macdhist'] = macdhist
    fields = ['MACD.12.26.9.macd','MACD.12.26.9.macdsignal','MACD.12.26.9.macdhist']
    return pd,fields

def computeRSI(ticker, pd, period):
    closeField = config.ticker2ReturnFieldMap[ticker]
    close = numpy.array(pd[closeField])
    pd['RSI.' + str(period)] = talib.RSI(close, timeperiod=period)
    return pd

def computeHilbertTransformSignals(ticker, pd):
    closeField = config.ticker2ReturnFieldMap[ticker]
    close = numpy.array(pd[closeField])
    pd['Hilbert.DCPeriod'] = talib.HT_DCPERIOD(close)
    pd['Hilbert.DCPhase']  = talib.HT_DCPHASE(close)
    pd['Hilbert.inphase'], pd['Hilbert.quadrature'] = talib.HT_PHASOR(close)
    pd['Hilbert.sine'], pd['Hilbert.leadsine'] = talib.HT_SINE(close)
    pd['Hilbert.TrendMode'] = talib.HT_TRENDMODE(close)
    fields = ['Hilbert.DCPeriod','Hilbert.DCPhase','Hilbert.inphase','Hilbert.quadrature','Hilbert.sine','Hilbert.leadsine','Hilbert.TrendMode']
    return pd,fields

def computeOpenToPreviousClose(ticker, pd):
    closeField = config.ticker2ReturnFieldMap[ticker]
    open  = pd['Open']
    pd['Open-PrevClose'] = open - pd[closeField].shift(1)
    return pd

def computeOpenToPreviousClosePercentage(ticker, pd):
    closeField = config.ticker2ReturnFieldMap[ticker]
    open  = pd['Open']
    pd['Open-PrevClose%'] = (open - pd[closeField].shift(1)) / pd[closeField].shift(1)
    return pd

def computeCloseToOpen(ticker, pd):
    closeField = config.ticker2ReturnFieldMap[ticker]
    open  = pd['Open']
    pd['Close-Open'] = pd[closeField] - open
    return pd
