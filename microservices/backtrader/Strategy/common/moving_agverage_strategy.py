# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Datetime : 2020/10/11 12:52
# @Author   : Fangyang
# @Software : PyCharm

import backtrader as bt


class MovingAverageStrategy(bt.Strategy):
    params = dict(
        pfast=10,  # period for the fast moving average
        pslow=40  # period for the slow moving average
    )

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.datetime(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        sma1 = bt.ind.SMA(period=self.p.pfast)  # fast moving average
        sma2 = bt.ind.SMA(period=self.p.pslow)  # slow moving average
        self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal

    def next(self):
        # Simply log the closing price of the series from the reference
        # self.log(f'Close,{self.dataclose[0]:.2f}.')

        # if self.position:
        #     self.log(f"Position:{self.position}")

        if not self.position:  # not in the market
            if self.crossover > 0:  # if fast crosses slow to the upside
                # self.order_target_size(target=1)  # enter long
                self.buy()
            elif self.crossover < 0:
                self.sell()

        elif self.position.size > 0 > self.crossover:
            self.close()
            self.sell()

        elif self.position.size < 0 and self.crossover > 0:
            self.close()
            self.buy()

if __name__ == '__main__':
    from microservices.backtrader.Test.data import gen_test_data_df

    df = gen_test_data_df()
    print(f"数据长度为:{len(df)}")
    data = bt.feeds.PandasData(dataname=df, datetime="datetime")

    # Create a cerebro entity
    cerebro = bt.Cerebro()
    cerebro.adddata(data, "rb")
    cerebro.broker.setcash(100000.0)

    cerebro.addstrategy(MovingAverageStrategy)
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='mySharpeRatio', timeframe=bt.TimeFrame.Minutes)
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='DW')

    r = cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    print('SR:', r[0].analyzers.mySharpeRatio.get_analysis())
    print('DW:', r[0].analyzers.DW.get_analysis())
    cerebro.plot(style="bar")
