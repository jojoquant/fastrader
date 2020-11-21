- [Target Orders](#target-orders)
  - [**`order_target_size`**](#order_target_size)
  - [**`order_target_value`**](#order_target_value)
  - [**`order_target_percent`**](#order_target_percent)
- [The Sample](#the-sample)
  - [order_target_size](#order_target_size-1)
  - [order_target_value](#order_target_value-1)
  - [order_target_percent](#order_target_percent-1)
- [Sample Usage](#sample-usage)
- [Sample Code](#sample-code)

--------------------------------------------------------
# Target Orders
直到版本 1.8.10.96, 智能 staking 变成可能, 是通过 backtrader 在策略中的方法：buy 和 sell。根本原因是增加了一个 `Sizer` 在方程中, 负责 stake 的 size。

`Sizer` 不能做的是确定操作是一个 buy 还是 sell。这就意味着需要一个新的概念，其中增加了一个小的智能层来做出这样的决定。

这正是 `order_target_xxx` 方法系列在策略中发挥作用的地方。受 zipline 的启发，这些方法提供了简单地指定最终目标(final target)的机会，即目标：

* `size` -> 特定资产组合中的股份数量，合同数量

* `value` -> 投资组合中资产的货币单位值

* `percent` -> 当前投资组合中资产价值的百分比（来自当前投资组合）

> 这些方法的说明可以在 Strategy 文档中找到。该方法使用相同的签名作为 `buy` 与 `sell` , 除了其中参数 `size` 由 `target` 替代

在这种情况下，所有操作都与指定最终目标有关，并且该方法确定操作将是买入还是卖出。相同的逻辑适用于3种方法。

## **`order_target_size`**

* 如果目标大于发出买入的头寸，则差额 target - position_size

    例如:

    * Pos: 0, target: 7 -> buy(size=7 - 0) -> buy(size=7)
    * Pos: 3, target: 7 -> buy(size=7 - 3) -> buy(size=4)
    * Pos: -3, target: 7 -> buy(size=7 - -3) -> buy(size=10)
    * Pos: -3, target: -2 -> buy(size=-2 - -3) -> buy(size=1)

* 如果目标小于头寸，则发出差价卖出 position_size - target

    例如：

    * Pos: 0, target: -7 -> sell(size=0 - -7) -> sell(size=7)
    * Pos: 3, target: -7 -> sell(size=3 - -7) -> sell(size=10)
    * Pos: -3, target: -7 -> sell(size=-3 - -7) -> sell(size=4)
    * Pos: 3, target: 2 -> sell(size=3 - 2) -> sell(size=1)

## **`order_target_value`**

当使用 **`order_target_value`** 设定目标值时，将考虑资产在投资组合中的当前价值和头寸规模(position size)，以确定最终的底层操作究竟是什么。原理：

* 如果头寸规模(position size)为负数（short）并且目标值(target value)必须大于当前值，则意味着：卖出更多

因此，逻辑的运行如下：
* If target > value and size >=0 -> buy
* If target > value and size < 0 -> sell
* If target < value and size >= 0 -> sell
* If target < value and size < 0 -> buy

## **`order_target_percent`** 
`order_target_percent` 的逻辑 与 `order_target_value` 的逻辑相同。该方法仅考虑投资组合的当前总价值来确定资产的目标价值。

# The Sample
backtrader尝试为每种新功能提供一个样本，这也不例外。测试的结果和预想的一致。这是 `order_target` 目录中的示例中。

样本中的逻辑相当笨拙，仅用于测试：
* 在奇数月（1月，3月，...）中，将日期用作目标（如果order_target_value将日期乘以1000）, 这模仿了一个不断增加的目标
* 在偶数月（2月，4月...）中，将其31 - day用作目标, 这模仿了降低的目标

## order_target_size
来看下1月和2月发生了什么:
```
$ ./order_target.py --target-size -- plot
0001 - 2005-01-03 - Position Size:     00 - Value 1000000.00
0001 - 2005-01-03 - Order Target Size: 03
0002 - 2005-01-04 - Position Size:     03 - Value 999994.39
0002 - 2005-01-04 - Order Target Size: 04
0003 - 2005-01-05 - Position Size:     04 - Value 999992.48
0003 - 2005-01-05 - Order Target Size: 05
0004 - 2005-01-06 - Position Size:     05 - Value 999988.79
...
0020 - 2005-01-31 - Position Size:     28 - Value 999968.70
0020 - 2005-01-31 - Order Target Size: 31
0021 - 2005-02-01 - Position Size:     31 - Value 999954.68
0021 - 2005-02-01 - Order Target Size: 30
0022 - 2005-02-02 - Position Size:     30 - Value 999979.65
0022 - 2005-02-02 - Order Target Size: 29
0023 - 2005-02-03 - Position Size:     29 - Value 999966.33
0023 - 2005-02-03 - Order Target Size: 28
...
```
在1月, 目标开始在当年的第一个交易日建仓03, 然后增加。Position 从 0 到 3，然后增量1。

在1月结束时，最后一个 `order_target` 为31，并且 在进入2月1日这一天会报告该头寸大小，此时要求新的目标为30, 同时随着头寸的减1变化。

![](order_target_size.png)

## order_target_value
target value使用类似的行为:
```
$ ./order_target.py --target-value --plot
0001 - 2005-01-03 - Position Size:     00 - Value 1000000.00
0001 - 2005-01-03 - data value 0.00
0001 - 2005-01-03 - Order Target Value: 3000.00
0002 - 2005-01-04 - Position Size:     78 - Value 999854.14
0002 - 2005-01-04 - data value 2853.24
0002 - 2005-01-04 - Order Target Value: 4000.00
0003 - 2005-01-05 - Position Size:     109 - Value 999801.68
0003 - 2005-01-05 - data value 3938.17
0003 - 2005-01-05 - Order Target Value: 5000.00
0004 - 2005-01-06 - Position Size:     138 - Value 999699.57
...
0020 - 2005-01-31 - Position Size:     808 - Value 999206.37
0020 - 2005-01-31 - data value 28449.68
0020 - 2005-01-31 - Order Target Value: 31000.00
0021 - 2005-02-01 - Position Size:     880 - Value 998807.33
0021 - 2005-02-01 - data value 30580.00
0021 - 2005-02-01 - Order Target Value: 30000.00
0022 - 2005-02-02 - Position Size:     864 - Value 999510.21
0022 - 2005-02-02 - data value 30706.56
0022 - 2005-02-02 - Order Target Value: 29000.00
0023 - 2005-02-03 - Position Size:     816 - Value 999130.05
0023 - 2005-02-03 - data value 28633.44
0023 - 2005-02-03 - Order Target Value: 28000.00
...
```

还有一条额外的信息行，告诉您（组合中的）实际数据值是多少。这有助于确定目标值是否已达到。

初始目标为3000.0，报告的初始值为 2853.24。这里的问题是，这是否足够接近。答案是肯定的

* 该示例在每日 bar 结尾处使用 Market 订单, 最后的可用价格来计算满足目标值(value)的目标大小(size)
* 执行将使用 open 第二天的价格，这不太可能是前一天的 close 价格

以任何其他方式进行操作将意味着有人在欺骗他/她自己。

下一个目标值和最终值十分接近：4000和 3938.17。

进入2月后，目标值开始从 31000 减小到 30000 再减小到 29000。数据值也是如此从 30580.00 到 30706.56 再到 28633.44

* 30580->30706.56 是一个正的变化

    确实。在这种情况下所计算的大小的目标值碰到一个开盘价将其值抬到 30706.56

如何避免这种影响：

* 该示例使用 `Market` 类型订单执行，无法避免这种影响
* `order_target_xxx` 这些方法允许指定 执行类型 和 价格。

可以指定一个 `Limit` 执行订单，然后将价格设为 收盘价（如果没有其他方法提供，则由该方法选择），或者提供指定的 price

![](./order_target_value.png)

## order_target_percent
在本例中，它只是当前投资组合价值的一个百分比。
```
$ ./order_target.py --target-percent --plot
0001 - 2005-01-03 - Position Size:     00 - Value 1000000.00
0001 - 2005-01-03 - data percent 0.00
0001 - 2005-01-03 - Order Target Percent: 0.03
0002 - 2005-01-04 - Position Size:     785 - Value 998532.05
0002 - 2005-01-04 - data percent 0.03
0002 - 2005-01-04 - Order Target Percent: 0.04
0003 - 2005-01-05 - Position Size:     1091 - Value 998007.44
0003 - 2005-01-05 - data percent 0.04
0003 - 2005-01-05 - Order Target Percent: 0.05
0004 - 2005-01-06 - Position Size:     1381 - Value 996985.64
...
0020 - 2005-01-31 - Position Size:     7985 - Value 991966.28
0020 - 2005-01-31 - data percent 0.28
0020 - 2005-01-31 - Order Target Percent: 0.31
0021 - 2005-02-01 - Position Size:     8733 - Value 988008.94
0021 - 2005-02-01 - data percent 0.31
0021 - 2005-02-01 - Order Target Percent: 0.30
0022 - 2005-02-02 - Position Size:     8530 - Value 995005.45
0022 - 2005-02-02 - data percent 0.30
0022 - 2005-02-02 - Order Target Percent: 0.29
0023 - 2005-02-03 - Position Size:     8120 - Value 991240.75
0023 - 2005-02-03 - data percent 0.29
0023 - 2005-02-03 - Order Target Percent: 0.28
...
```

并且该信息已更改为查看该数据在投资组合中所代表的百分比。
![](./order_target_percent.png)

# Sample Usage
```
$ ./order_target.py --help
usage: order_target.py [-h] [--data DATA] [--fromdate FROMDATE]
                       [--todate TODATE] [--cash CASH]
                       (--target-size | --target-value | --target-percent)
                       [--plot [kwargs]]

Sample for Order Target

optional arguments:
  -h, --help            show this help message and exit
  --data DATA           Specific data to be read in (default:
                        ../../datas/yhoo-1996-2015.txt)
  --fromdate FROMDATE   Starting date in YYYY-MM-DD format (default:
                        2005-01-01)
  --todate TODATE       Ending date in YYYY-MM-DD format (default: 2006-12-31)
  --cash CASH           Ending date in YYYY-MM-DD format (default: 1000000)
  --target-size         Use order_target_size (default: False)
  --target-value        Use order_target_value (default: False)
  --target-percent      Use order_target_percent (default: False)
  --plot [kwargs], -p [kwargs]
                        Plot the read data applying any kwargs passed For
                        example: --plot style="candle" (to plot candles)
                        (default: None)
```

# Sample Code
```
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import argparse
from datetime import datetime

import backtrader as bt


class TheStrategy(bt.Strategy):
    '''
    This strategy is loosely based on some of the examples from the Van
    K. Tharp book: *Trade Your Way To Financial Freedom*. The logic:

      - Enter the market if:
        - The MACD.macd line crosses the MACD.signal line to the upside
        - The Simple Moving Average has a negative direction in the last x
          periods (actual value below value x periods ago)

     - Set a stop price x times the ATR value away from the close

     - If in the market:

       - Check if the current close has gone below the stop price. If yes,
         exit.
       - If not, update the stop price if the new stop price would be higher
         than the current
    '''

    params = (
        ('use_target_size', False),
        ('use_target_value', False),
        ('use_target_percent', False),
    )

    def notify_order(self, order):
        if order.status == order.Completed:
            pass

        if not order.alive():
            self.order = None  # indicate no order is pending

    def start(self):
        self.order = None  # sentinel to avoid operrations on pending order

    def next(self):
        dt = self.data.datetime.date()

        portfolio_value = self.broker.get_value()
        print('%04d - %s - Position Size:     %02d - Value %.2f' %
              (len(self), dt.isoformat(), self.position.size, portfolio_value))

        data_value = self.broker.get_value([self.data])

        if self.p.use_target_value:
            print('%04d - %s - data value %.2f' %
                  (len(self), dt.isoformat(), data_value))

        elif self.p.use_target_percent:
            port_perc = data_value / portfolio_value
            print('%04d - %s - data percent %.2f' %
                  (len(self), dt.isoformat(), port_perc))

        if self.order:
            return  # pending order execution

        size = dt.day
        if (dt.month % 2) == 0:
            size = 31 - size

        if self.p.use_target_size:
            target = size
            print('%04d - %s - Order Target Size: %02d' %
                  (len(self), dt.isoformat(), size))

            self.order = self.order_target_size(target=size)

        elif self.p.use_target_value:
            value = size * 1000

            print('%04d - %s - Order Target Value: %.2f' %
                  (len(self), dt.isoformat(), value))

            self.order = self.order_target_value(target=value)

        elif self.p.use_target_percent:
            percent = size / 100.0

            print('%04d - %s - Order Target Percent: %.2f' %
                  (len(self), dt.isoformat(), percent))

            self.order = self.order_target_percent(target=percent)


def runstrat(args=None):
    args = parse_args(args)

    cerebro = bt.Cerebro()
    cerebro.broker.setcash(args.cash)

    dkwargs = dict()
    if args.fromdate is not None:
        dkwargs['fromdate'] = datetime.strptime(args.fromdate, '%Y-%m-%d')
    if args.todate is not None:
        dkwargs['todate'] = datetime.strptime(args.todate, '%Y-%m-%d')

    # data
    data = bt.feeds.YahooFinanceCSVData(dataname=args.data, **dkwargs)
    cerebro.adddata(data)

    # strategy
    cerebro.addstrategy(TheStrategy,
                        use_target_size=args.target_size,
                        use_target_value=args.target_value,
                        use_target_percent=args.target_percent)

    cerebro.run()

    if args.plot:
        pkwargs = dict(style='bar')
        if args.plot is not True:  # evals to True but is not True
            npkwargs = eval('dict(' + args.plot + ')')  # args were passed
            pkwargs.update(npkwargs)

        cerebro.plot(**pkwargs)


def parse_args(pargs=None):

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Sample for Order Target')

    parser.add_argument('--data', required=False,
                        default='../../datas/yhoo-1996-2015.txt',
                        help='Specific data to be read in')

    parser.add_argument('--fromdate', required=False,
                        default='2005-01-01',
                        help='Starting date in YYYY-MM-DD format')

    parser.add_argument('--todate', required=False,
                        default='2006-12-31',
                        help='Ending date in YYYY-MM-DD format')

    parser.add_argument('--cash', required=False, action='store',
                        type=float, default=1000000,
                        help='Ending date in YYYY-MM-DD format')

    pgroup = parser.add_mutually_exclusive_group(required=True)

    pgroup.add_argument('--target-size', required=False, action='store_true',
                        help=('Use order_target_size'))

    pgroup.add_argument('--target-value', required=False, action='store_true',
                        help=('Use order_target_value'))

    pgroup.add_argument('--target-percent', required=False,
                        action='store_true',
                        help=('Use order_target_percent'))

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