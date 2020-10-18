# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Datetime : 2020/10/15 14:52
# @Author   : Fangyang
# @Software : PyCharm


import backtrader as bt


class GridBreakoutStrategy(bt.Strategy):
    params = dict(
        one_sigma_target_pos=0.5,
        two_sigma_target_pos=0.8,
        three_sigma_target_pos=0.9,
        average_period=300
    )

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.datetime(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.bband_dev1 = bt.ind.BollingerBands(period=self.p.average_period, devfactor=2.0)  # fast moving average
        self.bband_dev2 = bt.ind.BollingerBands(period=self.p.average_period, devfactor=3.0)  # fast moving average
        self.bband_dev3 = bt.ind.BollingerBands(period=self.p.average_period, devfactor=4.0)  # fast moving average
        self.bband_dev4 = bt.ind.BollingerBands(period=self.p.average_period, devfactor=5.0)  # fast moving average

    def next(self):

        if self.bband_dev1.bot < self.dataclose < self.bband_dev1.top:
            self.order_target_percent(data=self.datas[0], target=0.0)

        elif self.bband_dev2.bot < self.dataclose < self.bband_dev1.bot:
            self.order_target_percent(data=self.datas[0], target=self.p.one_sigma_target_pos)
        elif self.bband_dev3.bot < self.dataclose < self.bband_dev2.bot:
            self.order_target_percent(data=self.datas[0], target=self.p.two_sigma_target_pos)
        elif self.bband_dev4.bot < self.dataclose < self.bband_dev3.bot:
            self.order_target_percent(data=self.datas[0], target=self.p.three_sigma_target_pos)

        elif self.bband_dev1.top < self.dataclose < self.bband_dev2.top:
            self.order_target_percent(data=self.datas[0], target=-self.p.one_sigma_target_pos)
        elif self.bband_dev2.top < self.dataclose < self.bband_dev3.top:
            self.order_target_percent(data=self.datas[0], target=-self.p.two_sigma_target_pos)
        elif self.bband_dev3.top < self.dataclose < self.bband_dev4.top:
            self.order_target_percent(data=self.datas[0], target=-self.p.three_sigma_target_pos)


if __name__ == '__main__':
    import time

    start_time = time.time()
    from microservices.backtrader.Test.data import gen_test_data_df

    df = gen_test_data_df()

    # import matplotlib.pyplot as plt
    # from scipy.stats import probplot
    # fig = plt.figure()
    # res = probplot(df['close'], plot=plt)  # 默认检测是正态分布
    # plt.show()

    print(f"数据长度为:{len(df)}")
    data = bt.feeds.PandasData(dataname=df, datetime="datetime")

    # Create a cerebro entity
    cerebro = bt.Cerebro()
    cerebro.adddata(data, "rb")
    cerebro.broker.setcash(100000.0)
    cerebro.broker.setcommission(commission=0.6/10000)

    cerebro.addstrategy(GridBreakoutStrategy)

    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="ta")
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='mySharpeRatio', timeframe=bt.TimeFrame.Minutes)
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='DW')
    cerebro.addanalyzer(bt.analyzers.SQN, _name="sqn")

    cerebro.addobserver(bt.observers.Value)
    r = cerebro.run(stdstats=False)
    # r = cerebro.run()

    final_portfolio_value = cerebro.broker.getvalue()
    print('Final Portfolio Value: %.2f' % final_portfolio_value)
    print(f'Total pct : {(final_portfolio_value / 1e5 - 1) * 100:.2f}%')

    print('SR:', r[0].analyzers.mySharpeRatio.get_analysis())
    print('DW:', r[0].analyzers.DW.get_analysis())
    print('SQN: {}'.format(round(r[0].analyzers.sqn.get_analysis().sqn, 2)))
    from microservices.backtrader.Analyzers.sqn import printTradeAnalysis
    printTradeAnalysis(r[0].analyzers.ta.get_analysis())

    time_cost = time.time() - start_time
    print(f"Time cost:{time_cost:.2f}s, average speed:{len(df) / time_cost:.2f}条/s")
    cerebro.plot(style="bar")
