# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Datetime : 2020/10/11 12:52
# @Author   : Fangyang
# @Software : PyCharm

import backtrader as bt


class RsiStrategy(bt.Strategy):

    def __init__(self):
        self.rsi = bt.indicators.RSI_SMA(self.data.close, period=21)

    def next(self):
        if not self.position:
            if self.rsi < 30:
                self.buy(size=10)
        else:
            if self.rsi > 70:
                self.sell(size=10)


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
