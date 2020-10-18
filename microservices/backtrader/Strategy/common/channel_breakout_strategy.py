# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Datetime : 2020/10/11 12:52
# @Author   : Fangyang
# @Software : PyCharm

import backtrader as bt


class ChannelBreakoutStrategy(bt.Strategy):
    params = dict(
        pfast=20,  # period for the fast moving average
        pslow=40  # period for the slow moving average
    )

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.datetime(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.slow_high = bt.ind.Highest(self.dataclose, period=self.p.pslow, plot=False)
        self.slow_low = bt.ind.Lowest(self.dataclose, period=self.p.pslow, plot=False)
        self.fast_high = bt.ind.Highest(self.dataclose, period=self.p.pfast,plot=False)
        self.fast_low = bt.ind.Lowest(self.dataclose, period=self.p.pfast,plot=False)

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS {0:8.2f}, NET {1:8.2f}'.format(
            trade.pnl, trade.pnlcomm))

    def next(self):
        # Simply log the closing price of the series from the reference
        # self.log('Close, %.2f' % self.dataclose[0])

        if not self.position:
            if self.dataclose > self.slow_high[-1]:
                self.buy(size=1000)
            elif self.dataclose < self.slow_low[-1]:
                self.sell(size=1000)

        if self.position.size > 0 and (self.dataclose < self.fast_low[-1]):
            self.close()
        elif self.position.size <0 and (self.dataclose > self.fast_high[-1]):
            self.close()


if __name__ == '__main__':
    from microservices.backtrader.Test.data import gen_test_data_df

    df = gen_test_data_df()
    print(f"数据长度为:{len(df)}")
    data = bt.feeds.PandasData(dataname=df, datetime="datetime")

    # Create a cerebro entity
    cerebro = bt.Cerebro()
    cerebro.adddata(data, "rb")
    cerebro.broker.setcash(100000.0)

    cerebro.broker.setcommission(commission=0.6 / 10000)

    cerebro.addstrategy(ChannelBreakoutStrategy)
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='mySharpeRatio')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='DW')
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="ta")
    cerebro.addanalyzer(bt.analyzers.SQN, _name="sqn")


    r = cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    print('SR:', r[0].analyzers.mySharpeRatio.get_analysis())
    print('DW:', r[0].analyzers.DW.get_analysis())

    from microservices.backtrader.Analyzers.sqn import printSQN,printTradeAnalysis

    printTradeAnalysis(r[0].analyzers.ta.get_analysis())
    printSQN(r[0].analyzers.sqn.get_analysis())

    cerebro.plot()
