# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Datetime : 2020/10/11 12:52
# @Author   : Fangyang
# @Software : PyCharm
import time

import backtrader as bt


class EmvStrategy(bt.Strategy):
    params = dict(
        emvn=260,
    )

    def __init__(self):
        self.high = self.data.high
        self.low = self.data.low
        self.movmid = ((self.high - self.low) / 2 - (self.high(-1) - self.low(-1)) / 2)
        self.volume = self.data.volume
        self.ratio = (self.high - self.low) / self.volume
        self.emv = bt.ind.SMA(self.movmid * self.ratio, period=self.p.emvn)

    def next(self):
        if not self.position:
            if self.emv[0] > 0:
                self.buy(size=10)
            elif self.emv[0] < 0:
                self.sell(size=10)
        else:
            if self.emv[0] < 0 < float(self.position.size):
                self.close()
                self.sell(size=10)
            elif self.emv[0] > 0 > float(self.position.size):
                self.close()
                self.buy(size=10)

    def stop(self):
        pnl = round(self.broker.getvalue() - self.broker.startingcash, 2)
        print('emvn Period: {} Final PnL: {}, return:{:.2f}%'.format(
            self.params.emvn, pnl, pnl*100/self.broker.startingcash))


if __name__ == '__main__':
    from microservices.backtrader.Test.data import gen_test_data_df

    df = gen_test_data_df()
    print(f"数据长度为:{len(df)}")
    df = df[df['volume'] != 0.0]
    print(f"volume!=0.0 过滤后数据长度为:{len(df)}")
    data = bt.feeds.PandasData(dataname=df, datetime="datetime")

    # Create a cerebro entity
    cerebro = bt.Cerebro()

    cerebro.adddata(data, "rb")
    startcash = 100000.0
    cerebro.broker.setcash(startcash)

    # cerebro.optstrategy(EmvStrategy, emvn=range(300, 400, 5))
    cerebro.addstrategy(EmvStrategy)
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='mySharpeRatio', timeframe=bt.TimeFrame.Minutes)
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='DW')
    cerebro.addanalyzer(bt.analyzers.SQN, _name="sqn")

    # clock the start of the process
    tstart = time.perf_counter()

    cerebro.addobserver(bt.observers.Value)
    r = cerebro.run(stdstats=False)
    # r = cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    print('SR:', r[0].analyzers.mySharpeRatio.get_analysis())
    print('DW:', r[0].analyzers.DW.get_analysis())
    print('SQN: {}'.format(round(r[0].analyzers.sqn.get_analysis().sqn, 2)))
    # clock the end of the process

    # print out the result
    tend = time.perf_counter()
    print(f'Time used: {(tend - tstart):.2f}s')

    # Generate results list
    # final_results_list = []
    # for run in r:
    #     for strategy in run:
    #         # print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    #         # print('SR:', strategy.analyzers.mySharpeRatio.get_analysis())
    #         # print('DW:', strategy.analyzers.DW.get_analysis())
    #         # print('SQN: {}'.format(round(strategy.analyzers.sqn.get_analysis().sqn, 2)))
    #         value = round(strategy.broker.get_value(), 2)
    #         PnL = round(value - startcash, 2)
    #         period = strategy.params.period
    #         final_results_list.append([period, PnL])

    # Sort Results List
    # by_period = sorted(final_results_list, key=lambda x: x[0])
    # by_PnL = sorted(final_results_list, key=lambda x: x[1], reverse=True)

    # Print results
    # print('Results: Ordered by period:')
    # for result in by_period:
    #     print('Period: {}, PnL: {}'.format(result[0], result[1]))
    # print('Results: Ordered by Profit:')
    # for result in by_PnL:
    #     print('Period: {}, PnL: {}'.format(result[0], result[1]))


    cerebro.plot(style="bar")
