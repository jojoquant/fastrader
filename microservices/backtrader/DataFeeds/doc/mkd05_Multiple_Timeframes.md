- [Data Feeds - Mutiple Timeframes](#data-feeds---mutiple-timeframes)
  - [Example 1 - Daily and Weekly](#example-1---daily-and-weekly)
  - [Example 2 - Daily and Daily Compression (2 bars to 1)](#example-2---daily-and-daily-compression-2-bars-to-1)
  - [Example 3 - Strategy with SMA](#example-3---strategy-with-sma)
    - [Invocation 1:](#invocation-1)
    - [Invocation 2:](#invocation-2)
  - [Conclusion](#conclusion)
----------------------------------------------
# Data Feeds - Mutiple Timeframes
有时，投资决策是在不同的时间范围内做出的：

* 每周评估趋势
* 每天执行输入, 还是5分钟和60分钟。

这意味着需要组合多个时间范围的数据, backtrader支持这种组合。

对此支持已经内置。最终用户必须遵循以下规则：

* `timeframe` 最小（因此条形数量更多）的数据必须是要添加到 Cerebro 实例的第一位数据

* 数据必须正确地与日期和时间保持一致，以使平台从中获取一些意义

除此之外，最终用户可以自由地在较短/较大的时间范围内应用指标。当然：

* 应用于较大时间范围的指标将产生较少的柱线

该平台还将考虑以下因素

* 较大 timeframes 的最小period

最短时间 period 可能会产生副作用，即必须在添加到 Cerebro 的策略开始实施之前，消耗较小数量级 timeframe bars 的几个数量级。

内置`cerebro.resample`函数将用于创建更大的 timeframe。

下面是一些示例，但首先是测试脚本的精髓。
```
    # Load the Data
    datapath = args.dataname or '../../datas/2006-day-001.txt'
    data = btfeeds.BacktraderCSVData(dataname=datapath)
    cerebro.adddata(data)  # First add the original data - smaller timeframe

    tframes = dict(daily=bt.TimeFrame.Days, weekly=bt.TimeFrame.Weeks,
                   monthly=bt.TimeFrame.Months)

    # Handy dictionary for the argument timeframe conversion
    # Resample the data
    if args.noresample:
        datapath = args.dataname2 or '../../datas/2006-week-001.txt'
        data2 = btfeeds.BacktraderCSVData(dataname=datapath)
        # And then the large timeframe
        cerebro.adddata(data2)
    else:
        cerebro.resampledata(data, timeframe=tframes[args.timeframe],
                             compression=args.compression)

    # Run over everything
    cerebro.run()
```

步骤：

* 载入数据

* 根据用户指定的参数对其重新采样    
  该脚本还允许加载第二个数据

* 将数据添加到 `cerebro`

* 将重新采样的数据（更大的 timeframe）添加到 `cerebro`

* run

## Example 1 - Daily and Weekly

```
$ ./multitimeframe-example.py --timeframe weekly --compression 1
```

## Example 2 - Daily and Daily Compression (2 bars to 1)
```
$ ./multitimeframe-example.py --timeframe daily --compression 2
```

## Example 3 - Strategy with SMA
尽管绘图很不错，但是这里的关键问题是显示更大的 timeframe 如何影响系统，尤其是当它下降到起点时

脚本可以采用 `--indicators` 来添加一个策略，该策略在较大的(weekly, 较小为 daily) timeframe 数据上创建 period 10 的简单移动平均值。

如果仅考虑较小的timeframe：

* next 将在10个 bars 之后第一次被调用，这是简单移动平均线需要产生一个值的时间

  注意：请记住，Strategy monitors 创建的指标，仅next在所有指标都产生值时调用 。理由是用户已添加指标以在逻辑中使用它们，因此，如果指标未产生任何值，则不应进行逻辑处理

但是在这种情况下，较长的 timeframe（weekly）会延迟调用，next 直到简单移动平均数在每周数据产生一个值后才需要…10周。

该脚本会覆盖 `nextstart` 这个仅被调用一次的方法，默认情况下调用 `next` 以显示, 当被首次调用时。

### Invocation 1:
只有 timeframe 为 daily, 获得一个移动平均线
命令行和输出如下:
```
$ ./multitimeframe-example.py --timeframe weekly --compression 1 --indicators --onlydaily
--------------------------------------------------
nextstart called with len 10
--------------------------------------------------
```

### Invocation 2:
两个timeframes获得一个简单移动平均线
```
$ ./multitimeframe-example.py --timeframe weekly --compression 1 --indicators
--------------------------------------------------
nextstart called with len 50
--------------------------------------------------
--------------------------------------------------
nextstart called with len 51
--------------------------------------------------
--------------------------------------------------
nextstart called with len 52
--------------------------------------------------
--------------------------------------------------
nextstart called with len 53
--------------------------------------------------
--------------------------------------------------
nextstart called with len 54
--------------------------------------------------
```

这里有两件事要注意：

* 该策略不是在10个周期后调用，而是在50个周期后第一个调用。
  
  之所以如此，是因为在较大的（weekly）时间范围内应用的简单移动平均线会在10周后产生一个值…… 10 weeks * 5 days / week … 50 days

* nextstart 被叫5次而不是被叫1次
  这是混合 timeframe 并将 indicators （在这种情况下只有一个）应用于较大 timeframe 的自然副作用。
  
  较大的 timeframe，简单移动平均线产生5倍相同值，而消耗5条每日柱线。
  
  而且由于周期的开始是由较大的时间范围控制的，因此nextstart被调用5次。

## Conclusion
backtrader 中可以使用多个 `timeframe` 数据，而无需特殊对象或进行调整：只需先添加较小的 timeframe 即可。

测试脚本:
```
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import argparse

import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.indicators as btind


class SMAStrategy(bt.Strategy):
    params = (
        ('period', 10),
        ('onlydaily', False),
    )

    def __init__(self):
        self.sma_small_tf = btind.SMA(self.data, period=self.p.period)
        if not self.p.onlydaily:
            self.sma_large_tf = btind.SMA(self.data1, period=self.p.period)

    def nextstart(self):
        print('--------------------------------------------------')
        print('nextstart called with len', len(self))
        print('--------------------------------------------------')

        super(SMAStrategy, self).nextstart()


def runstrat():
    args = parse_args()

    # Create a cerebro entity
    cerebro = bt.Cerebro(stdstats=False)

    # Add a strategy
    if not args.indicators:
        cerebro.addstrategy(bt.Strategy)
    else:
        cerebro.addstrategy(
            SMAStrategy,

            # args for the strategy
            period=args.period,
            onlydaily=args.onlydaily,
        )

    # Load the Data
    datapath = args.dataname or '../../datas/2006-day-001.txt'
    data = btfeeds.BacktraderCSVData(dataname=datapath)
    cerebro.adddata(data)  # First add the original data - smaller timeframe

    tframes = dict(daily=bt.TimeFrame.Days, weekly=bt.TimeFrame.Weeks,
                   monthly=bt.TimeFrame.Months)

    # Handy dictionary for the argument timeframe conversion
    # Resample the data
    if args.noresample:
        datapath = args.dataname2 or '../../datas/2006-week-001.txt'
        data2 = btfeeds.BacktraderCSVData(dataname=datapath)
        # And then the large timeframe
        cerebro.adddata(data2)
    else:
        cerebro.resampledata(data, timeframe=tframes[args.timeframe],
                             compression=args.compression)

    # Run over everything
    cerebro.run()

    # Plot the result
    cerebro.plot(style='bar')


def parse_args():
    parser = argparse.ArgumentParser(
        description='Multitimeframe test')

    parser.add_argument('--dataname', default='', required=False,
                        help='File Data to Load')

    parser.add_argument('--dataname2', default='', required=False,
                        help='Larger timeframe file to load')

    parser.add_argument('--noresample', action='store_true',
                        help='Do not resample, rather load larger timeframe')

    parser.add_argument('--timeframe', default='weekly', required=False,
                        choices=['daily', 'weekly', 'monhtly'],
                        help='Timeframe to resample to')

    parser.add_argument('--compression', default=1, required=False, type=int,
                        help='Compress n bars into 1')

    parser.add_argument('--indicators', action='store_true',
                        help='Wether to apply Strategy with indicators')

    parser.add_argument('--onlydaily', action='store_true',
                        help='Indicator only to be applied to daily timeframe')

    parser.add_argument('--period', default=10, required=False, type=int,
                        help='Period to apply to indicator')

    return parser.parse_args()


if __name__ == '__main__':
    runstrat()
```