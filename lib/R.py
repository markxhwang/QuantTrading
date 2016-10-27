import rpy2
print("rpy2 version:"+rpy2.__version__)
#from rpy2.rinterface import R_VERSION_BUILD
import rpy2.robjects as robjects
#print(R_VERSION_BUILD)

from rpy2.robjects.packages import importr
# import R's "base" package
base = importr('base')

# import R's "utils" package
utils = importr('utils')

# R package names
packnames = ('ggplot2', 'hexbin')

# R vector of strings
from rpy2.robjects.vectors import StrVector

# Selectively install what needs to be install.
# We are fancy, just because we can.

#names_to_install = [x for packnames if not rpackages.isinstalled(x)]
#if len(names_to_install) > 0:
#    utils.install_packages(StrVector(names_to_install))

pi = robjects.r['pi']
pi[0]