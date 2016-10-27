from quantopian.algorithm import attach_pipeline, pipeline_output
from quantopian.pipeline import Pipeline
from quantopian.pipeline import CustomFactor
from quantopian.pipeline.data.builtin import USEquityPricing
from quantopian.pipeline.data import morningstar
from quantopian.pipeline.factors import AverageDollarVolume
from quantopian.pipeline.factors import VWAP
import numpy as np
import scipy
import math


class ROE(CustomFactor):
    inputs = [morningstar.operation_ratios.roe]
    window_length = 1

    def compute(self, today, assets, out, close):
        out[:] = close[-1]


class Alpha41(CustomFactor):
    inputs = [USEquityPricing.low, USEquityPricing.high]
    window_length = 1

    def compute(self, today, assets, out, low, high):
        out[:] = high[0] * low[0]


def initialize(context):
    # set_commission(commission.PerShare(cost=0, min_trade_cost=None))
    # set_slippage(slippage.FixedSlippage(spread=0))

    pipe = Pipeline()
    attach_pipeline(pipe, 'ranked')
    dollar_volume = AverageDollarVolume(window_length=1)
    high_dollar_volume = dollar_volume.percentile_between(95, 100)
    alpha41 = Alpha41(mask=high_dollar_volume)
    vwap = VWAP(window_length=1)
    alpha41 = alpha41 ** .5 - vwap

    alpha41_rank = alpha41.rank(mask=high_dollar_volume)
    roe = ROE(mask=high_dollar_volume)

    combo_raw = (alpha41_rank)
    pipe.add(combo_raw, 'combo_raw')

    pipe.set_screen(roe > .005)

    schedule_function(func=rebalance,
                      date_rule=date_rules.every_day(),
                      time_rule=time_rules.market_open(hours=0, minutes=1))

    context.long_leverage = .5
    context.short_leverage = -.5
    context.short_num = 20
    context.long_num = 20


def before_trading_start(context, data):
    context.output = pipeline_output('ranked')
    context.long_list = context.output.sort_values(['combo_raw'], ascending=False).iloc[:context.long_num]
    context.short_list = context.output.sort_values(['combo_raw'], ascending=False).iloc[-context.short_num:]


def rebalance(context, data):
    if float(len(context.long_list)) <> 0:
        long_weight = context.long_leverage / float(len(context.long_list))
    else:
        long_weight = 0
    if float(len(context.short_list)) <> 0:
        short_weight = context.short_leverage / float(len(context.short_list))
    else:
        short_weight = 0
    for long_stock in context.long_list.index:
        if data.can_trade(long_stock):
            if long_stock not in security_lists.leveraged_etf_list:
                order_target_percent(long_stock, long_weight)
    for short_stock in context.short_list.index:
        if data.can_trade(short_stock):
            if short_stock not in security_lists.leveraged_etf_list:
                order_target_percent(short_stock, short_weight)
    for stock in context.portfolio.positions.iterkeys():
        if stock not in context.long_list.index and stock not in context.short_list.index:
            if data.can_trade(stock):
                order_target(stock, 0)

