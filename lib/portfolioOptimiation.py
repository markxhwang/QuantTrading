import cvxopt
import cvxopt.blas
import cvxopt.solvers
import cvxopt.lapack
import pylab

from src.config import GlobalConfig

config = GlobalConfig.Config()

class PortfolioOptimization(object):
    def __init__(self):
        pass

    @staticmethod
    def calcMVPort01(ER, VCV, wLB, wUB, wSum, n):  # Quandratic optimization
        expectedReturn = cvxopt.matrix(ER.as_matrix())
        if (config.debugLevel > 7):
            print("Expected Returned converted to cvxopt.matrix type:")
            print(expectedReturn)

        varianceCoVarianceMatrix = cvxopt.matrix(VCV.as_matrix())
        if (config.debugLevel > 7):
            print("Variance co-variance matrixed converted to cvxopt.matrix type:")
            print(varianceCoVarianceMatrix)

        A = cvxopt.matrix(1.0, (1, n))
        b = cvxopt.matrix(float(wSum))
        h = cvxopt.matrix(0.0, (2 * n, 1))
        G = cvxopt.matrix(0.0, (2 * n, n))
        for x in range(0, n):
            G[x, x] = -1
            h[x, 0] = -wLB
        for x in range(n, 2 * n):
            G[x, x - n] = 1
            h[x, 0] = wUB

        cvxopt.solvers.options['show_progress'] = False
        w = cvxopt.solvers.qp(varianceCoVarianceMatrix, -1 * expectedReturn, G, h, A, b)['x']
        #   Minimize (12)*x'*P*x + q' * x
        #      Subject to G*x <= h
        #                 A * x = b

        if (config.debugLevel > 5):
            print("Optimum portoflio weight =")
            print(w)
        return w

