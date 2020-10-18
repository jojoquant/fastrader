# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Datetime : 2020/10/10 12:32
# @Author   : Fangyang
# @Software : PyCharm

import backtrader as bt
from microservices.backtrader.Test.data import gen_test_data_df


if __name__ == '__main__':
    # settings = get_settings("database.")
    # dbo = DBOperation(settings)
    # dbo.get_start_date_from_db()
    # xx = dbo.get_groupby_data_from_sql_db()

    dbbardata_info_dict = {
        "symbol": "RBL8",
        "exchange": "SHFE",
        "interval": "1m",
        "end": "2015-11-26 23:58:02"
    }

    df0 = gen_test_data_df(dbbardata_info_dict)

    dbbardata_info_dict = {
        "symbol": "CSL8",
        "exchange": "DCE",
        "interval": "1m",
        "end": "2015-01-01 23:58:02"
    }

    df1 = gen_test_data_df(dbbardata_info_dict)

    # Pass it to the backtrader datafeed and add it to the cerebro
    data0 = bt.feeds.PandasData(dataname=df0, datetime="datetime")
    data1 = bt.feeds.PandasData(dataname=df1, datetime="datetime")

    # Create a cerebro entity
    cerebro = bt.Cerebro()
    cerebro.adddata(data0, "rb")
    cerebro.adddata(data1, "cs")
    cerebro.broker.setcash(100000.0)

    from microservices.backtrader.Strategy.moving_agverage_strategy import MovingAverageStrategy
    cerebro.addstrategy(MovingAverageStrategy)

    from microservices.backtrader.Analyzers.sharp_ratio_custom import SharpeRatio
    cerebro.addanalyzer(SharpeRatio, _name='mySharpRatio')
    # Run over everything
    r = cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    print('SR:', r[0].analyzers.mySharpRatio.get_analysis())

    # Plot the result
    cerebro.plot(style='bar')
