# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Datetime : 2020/10/11 12:52
# @Author   : Fangyang
# @Software : PyCharm

import backtrader as bt


class RsiStrategy(bt.Strategy):
    params = dict(
        period=10,
    )
    def __init__(self):
        # Let's create the moving averages as before
        self.data_co = (self.datas[0].close - self.data0.open) / self.data0.open
        self.data_hl = self.datas[0].high - self.data0.low
        ma1 = bt.ind.SMA(self.data_co, period=self.p.period)
        ma2 = bt.ind.SMA(self.data_hl, period=self.p.period)

        # Use line delay notation (-x) to get a ref to the -1 point
        ma1_pct = ma1 / ma1(-1) - 1.0  # The ma1 percentage part
        ma2_pct = ma2 / ma2(-1) - 1.0  # The ma2 percentage part

        self.buy_sig = ma1_pct > ma2_pct  # buy signal
        self.sell_sig = ma1_pct <= ma2_pct  # sell signal

    def next(self):
        # if not self.position:

        if self.buy_sig:
            self.buy(size=10)
        elif self.sell_sig:
            self.sell(size=10)

        # else:
        #     if self.rsi > 70:
        #         self.sell(size=10)


if __name__ == '__main__':
    from microservices.backtrader.Test.data import gen_test_data_df

    df = gen_test_data_df()
    print(f"数据长度为:{len(df)}")
    data = bt.feeds.PandasData(dataname=df, datetime="datetime")

    # Create a cerebro entity
    cerebro = bt.Cerebro()
    cerebro.adddata(data, "rb")
    cerebro.broker.setcash(100000.0)

    cerebro.addstrategy(RsiStrategy)
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='mySharpeRatio', timeframe=bt.TimeFrame.Minutes)
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='DW')

    r = cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    print('SR:', r[0].analyzers.mySharpeRatio.get_analysis())
    print('DW:', r[0].analyzers.DW.get_analysis())
    cerebro.plot(style="bar")
