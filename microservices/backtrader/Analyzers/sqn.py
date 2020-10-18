# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Datetime : 2020/10/12 0:47
# @Author   : Fangyang
# @Software : PyCharm


import backtrader as bt


# 来源
# https://backtest-rookies.com/2017/06/11/using-analyzers-backtrader/

def printTradeAnalysis(analyzer):
    '''
    Function to print the Technical Analysis results in a nice format.
    '''
    # Get the results we are interested in
    total_open = analyzer.total.open
    total_closed = analyzer.total.closed
    total_won = analyzer.won.total
    total_lost = analyzer.lost.total
    win_streak = analyzer.streak.won.longest
    lose_streak = analyzer.streak.lost.longest
    pnl_net = round(analyzer.pnl.net.total, 2)
    strike_rate = round((total_won / total_closed) * 100, 2)

    # Designate the rows
    h1 = ['Total Open', 'Total Closed', 'Total Won', 'Total Lost']
    h2 = ['Strike Rate', 'Win Streak', 'Losing Streak', 'PnL Net']
    r1 = [total_open, total_closed, total_won, total_lost]
    r2 = [strike_rate, win_streak, lose_streak, pnl_net]

    # Check which set of headers is the longest.
    if len(h1) > len(h2):
        header_length = len(h1)
    else:
        header_length = len(h2)
    # Print the rows
    print_list = [h1, r1, h2, r2]
    row_format = "{:<15}" * (header_length + 1)
    print("Trade Analysis Results:")
    for row in print_list:
        print(row_format.format('', *row))


def printSQN(analyzer):
    sqn = round(analyzer.sqn, 2)
    print('SQN: {}'.format(sqn))


if __name__ == '__main__':
    from microservices.backtrader.Test.data import gen_test_data_df

    df = gen_test_data_df()
    print(f"数据长度为:{len(df)}")
    data = bt.feeds.PandasData(dataname=df, datetime="datetime")

    # Create a cerebro entity
    cerebro = bt.Cerebro()
    cerebro.adddata(data, "rb")
    cerebro.broker.setcash(100000.0)

    from microservices.backtrader.Strategy.rsi_strategy import RsiStrategy

    cerebro.addstrategy(RsiStrategy)
    # cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='mySharpeRatio', timeframe=bt.TimeFrame.Minutes)
    # cerebro.addanalyzer(bt.analyzers.DrawDown, _name='DW')
    # Add the analyzers we are interested in
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="ta")
    cerebro.addanalyzer(bt.analyzers.SQN, _name="sqn")

    r = cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    # print('SR:', r[0].analyzers.mySharpeRatio.get_analysis())
    # print('DW:', r[0].analyzers.DW.get_analysis())

    from microservices.backtrader.Strategy.rsi_strategy import RsiStrategy

    printTradeAnalysis(r[0].analyzers.ta.get_analysis())
    printSQN(r[0].analyzers.sqn.get_analysis())

    for x in r[0].analyzers:
        x.print()

    # cerebro.plot(style="bar")
    cerebro.plot(style="candlestick")
