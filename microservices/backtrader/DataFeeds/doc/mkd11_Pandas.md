# Data Feeds - Panda
```
class PandasData(feed.DataBase):
    '''
    The ``dataname`` parameter inherited from ``feed.DataBase`` is the pandas
    DataFrame
    '''

    params = (
        # Possible values for datetime (must always be present)
        #  None : datetime is the "index" in the Pandas Dataframe
        #  -1 : autodetect position or case-wise equal name
        #  >= 0 : numeric index to the colum in the pandas dataframe
        #  string : column name (as index) in the pandas dataframe
        ('datetime', None),

        # Possible values below:
        #  None : column not present
        #  -1 : autodetect position or case-wise equal name
        #  >= 0 : numeric index to the colum in the pandas dataframe
        #  string : column name (as index) in the pandas dataframe
        ('open', -1),
        ('high', -1),
        ('low', -1),
        ('close', -1),
        ('volume', -1),
        ('openinterest', -1),
    )
```
上面的摘录 `PandasData` 类显示了这些点：

* 实例化期间类的参数 `dataname` 保存 Pandas Dataframe 的名称    
  此参数是从基类 `feed.DataBase` 继承的 

*  DataSeries 中新参数在中具有常规字段的名称，并遵循以下约定:

    * `datetime` （默认值：`None`）     
      * `None` 表示 `datetime` 是pandasdataframe中的“索引”
      * -1：自动检测位置或大小写相等的名称
      * =0：pandas dataframe 中列的数字索引
      * string：pandas dataframe中的列名（作为索引）

    * `open，high，low，high，close，volume， openinterest`（默认：-1）

      * None：不存在列
      * -1：自动检测位置或大小写相等的名称
      * =0：pandas dataframe 中列的数字索引
      * string：pandas dataframe中的列名（作为索引）

由 Pandas 而不是 backtrader 直接由解析的示例加载standar 2006样本

运行示例, 使用CSV数据中的现有“标题”：
```
$ ./panda-test.py
--------------------------------------------------
               Open     High      Low    Close  Volume  OpenInterest
Date
2006-01-02  3578.73  3605.95  3578.73  3604.33       0             0
2006-01-03  3604.08  3638.42  3601.84  3614.34       0             0
2006-01-04  3615.23  3652.46  3615.23  3652.46       0             0
```

同样的脚本, 跳过标题:
```
$ ./panda-test.py --noheaders
--------------------------------------------------
                  1        2        3        4  5  6
0
2006-01-02  3578.73  3605.95  3578.73  3604.33  0  0
2006-01-03  3604.08  3638.42  3601.84  3614.34  0  0
2006-01-04  3615.23  3652.46  3615.23  3652.46  0  0
```

第二次的脚本使用了 pandas.read_csv:
* 跳过首行(参数 `skiprows` 设置为 1)
* 不使用 header row (参数 `header` 设置为 None)

backtrader对Pandas的支持会尝试自动检测是否使用了列名或数字索引并采取相应的措施，以尝试提供最佳匹配。

测试代码如下:
```
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import argparse

import backtrader as bt
import backtrader.feeds as btfeeds

import pandas


def runstrat():
    args = parse_args()

    # Create a cerebro entity
    cerebro = bt.Cerebro(stdstats=False)

    # Add a strategy
    cerebro.addstrategy(bt.Strategy)

    # Get a pandas dataframe
    datapath = ('../../datas/2006-day-001.txt')

    # Simulate the header row isn't there if noheaders requested
    skiprows = 1 if args.noheaders else 0
    header = None if args.noheaders else 0

    dataframe = pandas.read_csv(datapath,
                                skiprows=skiprows,
                                header=header,
                                parse_dates=True,
                                index_col=0)

    if not args.noprint:
        print('--------------------------------------------------')
        print(dataframe)
        print('--------------------------------------------------')

    # Pass it to the backtrader datafeed and add it to the cerebro
    data = bt.feeds.PandasData(dataname=dataframe)

    cerebro.adddata(data)

    # Run over everything
    cerebro.run()

    # Plot the result
    cerebro.plot(style='bar')


def parse_args():
    parser = argparse.ArgumentParser(
        description='Pandas test script')

    parser.add_argument('--noheaders', action='store_true', default=False,
                        required=False,
                        help='Do not use header rows')

    parser.add_argument('--noprint', action='store_true', default=False,
                        help='Print the dataframe')

    return parser.parse_args()


if __name__ == '__main__':
    runstrat()
```