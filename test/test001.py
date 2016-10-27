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

    l = [i for i in range(0,50)]
    print(l)
    print(l[10:])
    print(l[-10:])
