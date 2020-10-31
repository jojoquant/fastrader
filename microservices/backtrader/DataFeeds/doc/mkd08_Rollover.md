- [Data Feeds - Rollover](#data-feeds---rollover)
  - [The RollOver Data Feed](#the-rollover-data-feed)
    - [Options for the Roll-Over](#options-for-the-roll-over)
    - [Subclassing RollOver](#subclassing-rollover)
  - [Let’s Roll](#lets-roll)
    - [Futures concatenation](#futures-concatenation)
    - [Futures roll-over with no checks](#futures-roll-over-with-no-checks)
    - [Changing during the Week](#changing-during-the-week)
    - [Adding a volume condition](#adding-a-volume-condition)
  - [Concluding](#concluding)
  - [Sample Usage](#sample-usage)
  - [Sample Code](#sample-code)
-------------------------------------------------------------
# Data Feeds - Rollover
一份连续的期货合约数据并不是很好找到, 有时已经过了交割日, 但是数据依旧还有, 还可以继续交易.

当待回测数据分散在一些不同的合约, 而这些合约又时间上有重合, 在回测时会遇到一些问题

如何才能合理的拼接好这些合约数据, 过去的做法是拼成一个连续的流 stream 数据. 问题是:

* 没有规则写清如何才能将不同的过期日期拼接成一个连续的期货合约

[一些文献，由SierraChart提供](http://www.sierrachart.com/index.php?page=doc/ChangingFuturesContract.html)

## The RollOver Data Feed
`backtrader` 从 `1.8.10.99` 之后, 提供了将不同到期日期的期货数据合并为连续期货的可能：
```
import backtrader as bt

cerebro = bt.Cerebro()
data0 = bt.feeds.MyFeed(dataname='Expiry0')
data1 = bt.feeds.MyFeed(dataname='Expiry1')
...
dataN = bt.feeds.MyFeed(dataname='ExpiryN')

drollover = cerebro.rolloverdata(data0, data1, ..., dataN, name='MyRoll', **kwargs)

cerebro.run()
```

也可以通过直接访问 `RollOver` feed 来完成（如果用子类实现，这将很有帮助）：

```
import backtrader as bt

cerebro = bt.Cerebro()
data0 = bt.feeds.MyFeed(dataname='Expiry0')
data1 = bt.feeds.MyFeed(dataname='Expiry1')
...
dataN = bt.feeds.MyFeed(dataname='ExpiryN')

drollover = bt.feeds.RollOver(data0, data1, ..., dataN, dataname='MyRoll', **kwargs)
cerebro.adddata(drollover)

cerebro.run()
```

> 使用 `RollOver` 分配名称 `dataname` 。这是用于所有 data Feed 传递 `name/ticker` 的标准参数 。在这种情况下，它可以重复使用，为完整的期货套期分配一个通用名称。

在 `cerebro.rolloverdata` 的模式下，使用 `name` 给 Feed 命名，是该方法的一个命名参数。

底层实现如下：

* data feeds 创建像往常一样，但不加入 `cerebro`
* 这些 data feeds 作为输入提供给 `bt.feeds.RollOver`  
  参数 `dataname` 主要用于识别目的。
* 然后将此 roll over data feed 添加到 `cerebro`


### Options for the Roll-Over
提供了两个参数来控制 roll-over 过程

* `checkdate`（默认值：`None`）   
  这必须是具有以下签名的可调用项：
  
  > checkdate(dt, d):
  
  这里:
  * `dt` 是一个 `datetime.datetime` 对象
  * `d` 是当前活跃期货的 data feed
  
  期待的返回值:
  * `True` : 只要被调用对象返回 `True`，下一个期货就进行切换(switchover)  
  如果某商品期货在3月第三个周五过期，`checkdate` 将在其到期所发生的整个星期都返回 `True` 。
  
  * `False`：还没到期

* `checkcondition` (default: `None`)
    > 仅在 `checkdate` 返回 `True` 时才调用
    
    if 设置为 `None`, `checkdate` 返回 `True`, 执行 roll over
    
    else 这就是个可调用函数:
    > checkcondition(d0, d1)
    
    这里:
    * `d0` 是当前活跃期货的 data feed
    * `d1` 是下一个过期的 data feed

    期待的返回值:
    * `True`: roll-over 到下一个期货合约    
    遵循 `checkdate` 的示例，可以说只有在 `d0` 的 `volume` 已经小于 `d1` 时才可以进行翻转(roll-over)

    * False: 还没到期

### Subclassing RollOver
如果仅指定可调用对象(函数)还不够，那么还有继承 `RollOver` 子类化的模式,子类方法如下：

* `def _checkdate(self, dt, d):`  
  与上面同名参数的签名匹配。期望的返回值也是一样。

* `def _checkcondition(self, d0, d1):`     
  与上面同名参数的签名匹配。期望的返回值也是一样。

## Let’s Roll
> 注意  
> 示例中的默认行为是使用 `cerebro.rolloverdata`。可以通过传递`-no-cerebro` 标志来更改 。在这种情况下，其实是使用 `RollOver` 和 `cerebro.adddata`

该实现包括一个示例，该示例可在 backtrader 源码中获得。

### Futures concatenation
让我们从不带参数的示例开始看一个纯 concatenation。
```
$ ./rollover.py

Len, Name, RollName, Datetime, WeekDay, Open, High, Low, Close, Volume, OpenInterest
0001, FESX, 199FESXM4, 2013-09-26, Thu, 2829.0, 2843.0, 2829.0, 2843.0, 3.0, 1000.0
0002, FESX, 199FESXM4, 2013-09-27, Fri, 2842.0, 2842.0, 2832.0, 2841.0, 16.0, 1101.0
...
0176, FESX, 199FESXM4, 2014-06-20, Fri, 3315.0, 3324.0, 3307.0, 3322.0, 134777.0, 520978.0
0177, FESX, 199FESXU4, 2014-06-23, Mon, 3301.0, 3305.0, 3265.0, 3285.0, 730211.0, 3003692.0
...
0241, FESX, 199FESXU4, 2014-09-19, Fri, 3287.0, 3308.0, 3286.0, 3294.0, 144692.0, 566249.0
0242, FESX, 199FESXZ4, 2014-09-22, Mon, 3248.0, 3263.0, 3231.0, 3240.0, 582077.0, 2976624.0
...
0306, FESX, 199FESXZ4, 2014-12-19, Fri, 3196.0, 3202.0, 3131.0, 3132.0, 226415.0, 677924.0
0307, FESX, 199FESXH5, 2014-12-22, Mon, 3151.0, 3177.0, 3139.0, 3168.0, 547095.0, 2952769.0
...
0366, FESX, 199FESXH5, 2015-03-20, Fri, 3680.0, 3698.0, 3672.0, 3695.0, 147632.0, 887205.0
0367, FESX, 199FESXM5, 2015-03-23, Mon, 3654.0, 3655.0, 3608.0, 3618.0, 802344.0, 3521988.0
...
0426, FESX, 199FESXM5, 2015-06-18, Thu, 3398.0, 3540.0, 3373.0, 3465.0, 1173246.0, 811805.0
0427, FESX, 199FESXM5, 2015-06-19, Fri, 3443.0, 3499.0, 3440.0, 3488.0, 104096.0, 516792.0
```

使用此方法 `cerebro.chaindata`，结果应该很清楚：

* 每当数据馈送结束时，下一个接管
* 这种情况总是在星期五和星期一之间发生：样本中的期货总是在星期五到期

### Futures roll-over with no checks
让我们执行使用 roll-over 的脚本:
```
$ ./rollover.py --rollover --plot

Len, Name, RollName, Datetime, WeekDay, Open, High, Low, Close, Volume, OpenInterest
0001, FESX, 199FESXM4, 2013-09-26, Thu, 2829.0, 2843.0, 2829.0, 2843.0, 3.0, 1000.0
0002, FESX, 199FESXM4, 2013-09-27, Fri, 2842.0, 2842.0, 2832.0, 2841.0, 16.0, 1101.0
...
0176, FESX, 199FESXM4, 2014-06-20, Fri, 3315.0, 3324.0, 3307.0, 3322.0, 134777.0, 520978.0
0177, FESX, 199FESXU4, 2014-06-23, Mon, 3301.0, 3305.0, 3265.0, 3285.0, 730211.0, 3003692.0
...
0241, FESX, 199FESXU4, 2014-09-19, Fri, 3287.0, 3308.0, 3286.0, 3294.0, 144692.0, 566249.0
0242, FESX, 199FESXZ4, 2014-09-22, Mon, 3248.0, 3263.0, 3231.0, 3240.0, 582077.0, 2976624.0
...
0306, FESX, 199FESXZ4, 2014-12-19, Fri, 3196.0, 3202.0, 3131.0, 3132.0, 226415.0, 677924.0
0307, FESX, 199FESXH5, 2014-12-22, Mon, 3151.0, 3177.0, 3139.0, 3168.0, 547095.0, 2952769.0
...
0366, FESX, 199FESXH5, 2015-03-20, Fri, 3680.0, 3698.0, 3672.0, 3695.0, 147632.0, 887205.0
0367, FESX, 199FESXM5, 2015-03-23, Mon, 3654.0, 3655.0, 3608.0, 3618.0, 802344.0, 3521988.0
...
0426, FESX, 199FESXM5, 2015-06-18, Thu, 3398.0, 3540.0, 3373.0, 3465.0, 1173246.0, 811805.0
0427, FESX, 199FESXM5, 2015-06-19, Fri, 3443.0, 3499.0, 3440.0, 3488.0, 104096.0, 516792.0
```
和前面 concatenation 的结果相同。可以清楚地看到，合同的变更发生在三月，六月，九月，十二月的第三个周五

但这是错误的。`backtrader` 无法得知这些，但作者知道 EuroStoxx 50 期货在12:00 CET 停止交易。因此，即使在到期月的第三个星期五有一个 daily bar, 但是换合约已经晚了。

### Changing during the Week
该示例中 `checkdate` 实现了一个 Callable 对象(函数)，计算了当前有效合约的到期日期。

`checkdate` 会在包含该月的第三个星期五的这周(week)刚到时, 立即进行 roll over（例如，如果星期一是银行假日，则可能是星期二）
```
$ ./rollover.py --rollover --checkdate --plot

Len, Name, RollName, Datetime, WeekDay, Open, High, Low, Close, Volume, OpenInterest
0001, FESX, 199FESXM4, 2013-09-26, Thu, 2829.0, 2843.0, 2829.0, 2843.0, 3.0, 1000.0
0002, FESX, 199FESXM4, 2013-09-27, Fri, 2842.0, 2842.0, 2832.0, 2841.0, 16.0, 1101.0
...
0171, FESX, 199FESXM4, 2014-06-13, Fri, 3283.0, 3292.0, 3253.0, 3276.0, 734907.0, 2715357.0
0172, FESX, 199FESXU4, 2014-06-16, Mon, 3261.0, 3275.0, 3252.0, 3262.0, 180608.0, 844486.0
...
0236, FESX, 199FESXU4, 2014-09-12, Fri, 3245.0, 3247.0, 3220.0, 3232.0, 650314.0, 2726874.0
0237, FESX, 199FESXZ4, 2014-09-15, Mon, 3209.0, 3224.0, 3203.0, 3221.0, 153448.0, 983793.0
...
0301, FESX, 199FESXZ4, 2014-12-12, Fri, 3127.0, 3143.0, 3038.0, 3042.0, 1409834.0, 2934179.0
0302, FESX, 199FESXH5, 2014-12-15, Mon, 3041.0, 3089.0, 2963.0, 2980.0, 329896.0, 904053.0
...
0361, FESX, 199FESXH5, 2015-03-13, Fri, 3657.0, 3680.0, 3627.0, 3670.0, 867678.0, 3499116.0
0362, FESX, 199FESXM5, 2015-03-16, Mon, 3594.0, 3641.0, 3588.0, 3629.0, 250445.0, 1056099.0
...
0426, FESX, 199FESXM5, 2015-06-18, Thu, 3398.0, 3540.0, 3373.0, 3465.0, 1173246.0, 811805.0
0427, FESX, 199FESXM5, 2015-06-19, Fri, 3443.0, 3499.0, 3440.0, 3488.0, 104096.0, 516792.0
```
这样就好多了。现在将在5天前进行 roll over 换期。快速查看Len索引即可看到它。例如：

* `199FESXM4` 到 `199FESXU4` 发生在 LEN 171-172。没有 `checkdate` 它发生在 176-177

展期将在到期月份的第三个星期五之前的星期一进行。

### Adding a volume condition
即使前面有了改进，还可以进一步优化，因为不仅要考虑日期，而且还要考虑 `volume` 。当新合约的交易量大于当前活跃合约的交易量时，进行切换。

让我们添加一个 `checkcondition` 运行。
```
$ ./rollover.py --rollover --checkdate --checkcondition --plot

Len, Name, RollName, Datetime, WeekDay, Open, High, Low, Close, Volume, OpenInterest
0001, FESX, 199FESXM4, 2013-09-26, Thu, 2829.0, 2843.0, 2829.0, 2843.0, 3.0, 1000.0
0002, FESX, 199FESXM4, 2013-09-27, Fri, 2842.0, 2842.0, 2832.0, 2841.0, 16.0, 1101.0
...
0175, FESX, 199FESXM4, 2014-06-19, Thu, 3307.0, 3330.0, 3300.0, 3321.0, 717979.0, 759122.0
0176, FESX, 199FESXU4, 2014-06-20, Fri, 3309.0, 3318.0, 3290.0, 3298.0, 711627.0, 2957641.0
...
0240, FESX, 199FESXU4, 2014-09-18, Thu, 3249.0, 3275.0, 3243.0, 3270.0, 846600.0, 803202.0
0241, FESX, 199FESXZ4, 2014-09-19, Fri, 3273.0, 3293.0, 3250.0, 3252.0, 1042294.0, 3021305.0
...
0305, FESX, 199FESXZ4, 2014-12-18, Thu, 3095.0, 3175.0, 3085.0, 3172.0, 1309574.0, 889112.0
0306, FESX, 199FESXH5, 2014-12-19, Fri, 3195.0, 3200.0, 3106.0, 3147.0, 1329040.0, 2964538.0
...
0365, FESX, 199FESXH5, 2015-03-19, Thu, 3661.0, 3691.0, 3646.0, 3668.0, 1271122.0, 1054639.0
0366, FESX, 199FESXM5, 2015-03-20, Fri, 3607.0, 3664.0, 3595.0, 3646.0, 1182235.0, 3407004.0
...
0426, FESX, 199FESXM5, 2015-06-18, Thu, 3398.0, 3540.0, 3373.0, 3465.0, 1173246.0, 811805.0
0427, FESX, 199FESXM5, 2015-06-19, Fri, 3443.0, 3499.0, 3440.0, 3488.0, 104096.0, 516792.0
```
更棒了。我们已经将切换至 到期月的第三个周五前的周四(而不是周一)

这不足为奇，因为即将到期的期货在该星期五的交易时间要少得多，并且交易量必须很小。

> 注意
> roll over 日期也可以由 `checkdate` 函数设置为该星期四 。但这不是本例的重点。

## Concluding
backtrader现在包括一个灵活的机制，允许期货滚动以创建连续流。
## Sample Usage
```
$ ./rollover.py --help
usage: rollover.py [-h] [--no-cerebro] [--rollover] [--checkdate]
                   [--checkcondition] [--plot [kwargs]]

Sample for Roll Over of Futures

optional arguments:
  -h, --help            show this help message and exit
  --no-cerebro          Use RollOver Directly (default: False)
  --rollover
  --checkdate           Change during expiration week (default: False)
  --checkcondition      Change when a given condition is met (default: False)
  --plot [kwargs], -p [kwargs]
                        Plot the read data applying any kwargs passed For
                        example: --plot style="candle" (to plot candles)
                        (default: None)
```

## Sample Code
```
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)


import argparse
import bisect
import calendar
import datetime

import backtrader as bt


class TheStrategy(bt.Strategy):
    def start(self):
        header = ['Len', 'Name', 'RollName', 'Datetime', 'WeekDay', 'Open',
                  'High', 'Low', 'Close', 'Volume', 'OpenInterest']
        print(', '.join(header))

    def next(self):
        txt = list()
        txt.append('%04d' % len(self.data0))
        txt.append('{}'.format(self.data0._dataname))
        # Internal knowledge ... current expiration in use is in _d
        txt.append('{}'.format(self.data0._d._dataname))
        txt.append('{}'.format(self.data.datetime.date()))
        txt.append('{}'.format(self.data.datetime.date().strftime('%a')))
        txt.append('{}'.format(self.data.open[0]))
        txt.append('{}'.format(self.data.high[0]))
        txt.append('{}'.format(self.data.low[0]))
        txt.append('{}'.format(self.data.close[0]))
        txt.append('{}'.format(self.data.volume[0]))
        txt.append('{}'.format(self.data.openinterest[0]))
        print(', '.join(txt))


def checkdate(dt, d):
    # Check if the date is in the week where the 3rd friday of Mar/Jun/Sep/Dec

    # EuroStoxx50 expiry codes: MY
    # M -> H, M, U, Z (Mar, Jun, Sep, Dec)
    # Y -> 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 -> year code. 5 -> 2015
    MONTHS = dict(H=3, M=6, U=9, Z=12)

    M = MONTHS[d._dataname[-2]]

    centuria, year = divmod(dt.year, 10)
    decade = centuria * 10

    YCode = int(d._dataname[-1])
    Y = decade + YCode
    if Y < dt.year:  # Example: year 2019 ... YCode is 0 for 2020
        Y += 10

    exp_day = 21 - (calendar.weekday(Y, M, 1) + 2) % 7
    exp_dt = datetime.datetime(Y, M, exp_day)

    # Get the year, week numbers
    exp_year, exp_week, _ = exp_dt.isocalendar()
    dt_year, dt_week, _ = dt.isocalendar()

    # print('dt {} vs {} exp_dt'.format(dt, exp_dt))
    # print('dt_week {} vs {} exp_week'.format(dt_week, exp_week))

    # can switch if in same week
    return (dt_year, dt_week) == (exp_year, exp_week)


def checkvolume(d0, d1):
    return d0.volume[0] < d1.volume[0]  # Switch if volume from d0 < d1


def runstrat(args=None):
    args = parse_args(args)

    cerebro = bt.Cerebro()

    fcodes = ['199FESXM4', '199FESXU4', '199FESXZ4', '199FESXH5', '199FESXM5']
    store = bt.stores.VChartFile()
    ffeeds = [store.getdata(dataname=x) for x in fcodes]

    rollkwargs = dict()
    if args.checkdate:
        rollkwargs['checkdate'] = checkdate

        if args.checkcondition:
            rollkwargs['checkcondition'] = checkvolume

    if not args.no_cerebro:
        if args.rollover:
            cerebro.rolloverdata(name='FESX', *ffeeds, **rollkwargs)
        else:
            cerebro.chaindata(name='FESX', *ffeeds)
    else:
        drollover = bt.feeds.RollOver(*ffeeds, dataname='FESX', **rollkwargs)
        cerebro.adddata(drollover)

    cerebro.addstrategy(TheStrategy)
    cerebro.run(stdstats=False)

    if args.plot:
        pkwargs = dict(style='bar')
        if args.plot is not True:  # evals to True but is not True
            npkwargs = eval('dict(' + args.plot + ')')  # args were passed
            pkwargs.update(npkwargs)

        cerebro.plot(**pkwargs)


def parse_args(pargs=None):

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Sample for Roll Over of Futures')

    parser.add_argument('--no-cerebro', required=False, action='store_true',
                        help='Use RollOver Directly')

    parser.add_argument('--rollover', required=False, action='store_true')

    parser.add_argument('--checkdate', required=False, action='store_true',
                        help='Change during expiration week')

    parser.add_argument('--checkcondition', required=False,
                        action='store_true',
                        help='Change when a given condition is met')

    # Plot options
    parser.add_argument('--plot', '-p', nargs='?', required=False,
                        metavar='kwargs', const=True,
                        help=('Plot the read data applying any kwargs passed\n'
                              '\n'
                              'For example:\n'
                              '\n'
                              '  --plot style="candle" (to plot candles)\n'))

    if pargs is not None:
        return parser.parse_args(pargs)

    return parser.parse_args()


if __name__ == '__main__':
    runstrat()
```