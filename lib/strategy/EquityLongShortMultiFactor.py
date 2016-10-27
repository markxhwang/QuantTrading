from quantopian.algorithm import attach_pipeline, pipeline_output
from quantopian.pipeline import Pipeline
from quantopian.pipeline.data.builtin import USEquityPricing
from quantopian.pipeline.factors import CustomFactor, AverageDollarVolume
from quantopian.pipeline.data import morningstar

import zipline
import pandas as pd
import numpy as np


class Value(CustomFactor):
    inputs = [morningstar.valuation_ratios.book_value_yield,
              morningstar.valuation_ratios.sales_yield,
              morningstar.valuation_ratios.fcf_yield]

    window_length = 1

    def compute(self, today, assets, out, book_value, sales, fcf):
        value_table = pd.DataFrame(index=assets)
        value_table["book_value"] = book_value[-1]
        value_table["sales"] = sales[-1]
        value_table["fcf"] = fcf[-1]
        out[:] = value_table.rank().mean(axis=1)


class Momentum(CustomFactor):
    inputs = [USEquityPricing.close]
    window_length = 252

    def compute(self, today, assets, out, close):
        out[:] = close[-20] / close[0]


class Quality(CustomFactor):
    inputs = [morningstar.operation_ratios.roe]
    window_length = 1

    def compute(self, today, assets, out, roe):
        out[:] = roe[-1]


class Volatility(CustomFactor):
    inputs = [USEquityPricing.close]
    window_length = 252

    def compute(self, today, assets, out, close):
        close = pd.DataFrame(data=close, columns=assets)
        # Since we are going to rank largest is best we need to invert the sdev.
        out[:] = 1 / np.log(close).diff().std()

class PercentChange(CustomFactor):
        """
        Calculates the percent change of input over the given window_length.
        """

    def compute(self, today, assets, out, data):
            out[:] = (data[-1] - data[0]) / data[0]

class SimpleMovingAveragePercentChange(SimpleMovingAverage):
                """
                Average Value of an arbitrary column
                **Default Inputs**: None
                **Default Window Length**: None
                """

                def compute(self, today, assets, out, data):
                    prct_change = np.diff(data, axis=0)  # absolute change
                    prct_change /= data[:-1]  # percentage change
                    SimpleMovingAverage.compute(self, today, assets, out, prct_change)

                    # Compute final rank and assign long and short baskets.


class OBV_(CustomFactor):
    inputs = [USEquityPricing.close, USEquityPricing.volume]
    window_length = 2

    def compute(self, today, assets, out, close, vol):
        diff = close[-1] - close[-2]
        diff_abs = np.absolute(diff)
        price_dir = diff / diff_abs
        obv = pd.Series((price_dir * vol)[-1], index=assets)
        if (context.obv is None):
            context.obv = obv
            context.running_obv = obv
        else:
            context.obv = context.obv.add(obv, fill_value=0)
            context.running_obv.append(obv)
        out[:] = context.obv[assets]
    return OBV_()


def before_trading_start(context, data):
    results = pipeline_output('factors').dropna()
    ranks = results.rank().mean(axis=1).order()

    context.shorts = 1 / ranks[results["momentum"] < 1].head(200)
    context.shorts /= context.shorts.sum()

    context.longs = ranks[results["momentum"] > 1].tail(200)
    context.longs /= context.longs.sum()

    context.security_list = context.longs.index.union(context.shorts.index).tolist()


# Put any initialization logic here. The context object will be passed to
# the other methods in your algorithm.
def initialize(context):
    pipe = Pipeline()
    pipe = attach_pipeline(pipe, name='factors')

    value = Value()
    momentum = Momentum()
    quality = Quality()
    volatility = Volatility()

    pipe.add(value, "value")
    pipe.add(momentum, "momentum")
    pipe.add(quality, "quality")
    pipe.add(volatility, "volatility")

    dollar_volume = AverageDollarVolume(window_length=20)

    # Screen out low liquidity securities.
    pipe.set_screen(dollar_volume > 10 ** 7)

    context.spy = sid(8554)
    context.shorts = None
    context.longs = None

    schedule_function(rebalance, date_rules.month_start())
    schedule_function(cancel_open_orders, date_rules.every_day(),
                      time_rules.market_close())
    schedule_function(record_vars, date_rules.every_day(), time_rules.market_close())


# Will be called on every trade event for the securities you specify.
def record_vars(context, data):
    record(lever=context.account.leverage,
           exposure=context.account.net_leverage,
           num_pos=len(context.portfolio.positions),
           oo=len(get_open_orders()))


def cancel_open_orders(context, data):
    open_orders = get_open_orders()
    for security in open_orders:
        for order in open_orders[security]:
            cancel_order(order)


def rebalance(context, data):
    for security in context.shorts.index:
        if get_open_orders(security):
            continue
        if data.can_trade(security):
            order_target_percent(security, -context.shorts[security])

    for security in context.longs.index:
        if get_open_orders(security):
            continue
        if data.can_trade(security):
            order_target_percent(security, context.longs[security])

    for security in context.portfolio.positions:
        if get_open_orders(security):
            continue
        if data.can_trade(security) and security not in context.security_list:
            order_target_percent(security, 0)


def handle_data(context, data):
    pass