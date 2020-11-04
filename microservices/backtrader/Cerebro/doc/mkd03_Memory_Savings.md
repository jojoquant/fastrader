- [Cerebro - Memory Savings](#cerebro---memory-savings)
  - [Script Code and Usage](#script-code-and-usage)
--------------------------------------------------------------------
# Cerebro - Memory Savings
backtrader 是（并将进一步）在具有大RAM的机器上开发的，并且结合了以下事实：通过绘图获得视觉反馈非常好，而且几乎是必须具备的，这使得设计决策很容易：将所有内容保留在内存中。

这个决定有一些缺点：

* array.array 当超出某些范围时，用于数据存储的数据必须分配和移动数据

* RAM小的机器可能会受到影响

* 连接到实时数据源，该数据源可以在线运行数周/数月，将大量秒/分钟级ticks输入系统

第三点比第一点更重要, 因此设计出backtrader的一种使用场景：

* 如果需要，可以使用纯Python来在嵌入式系统中运行

    未来的情况可能是backtrader连接到提供实时数据的第二台计算机，而backtrader运行在Raspberry Pi或其他更受限制的设备（如ADSL路由器）中（带有Freetz图像的AVM Frit！Box 7490 ）。

因此需要具有backtrader支持动态内存方案。现在 `Cerebro` 可以被实例化或run with以下参数：

* `exactbars`（默认值：`False`）    
    用默认的False, 每个值都存储在 line 中, 并被保存在内存中

    可能的值：

    * `True` 或 `1`：所有 line 对象将内存使用量减少到自动计算的最短周期。   
    如果简单移动平均线的周期为30，则基础数据将始终具有30条的运行缓冲区，以允许计算简单移动平均线

      * 此设置将停用preload，runonce

      * 使用此设置也会停用 plotting

    * `-1`：策略中的 datas 和 indicators/operations 将保存所有数据在内存中。例如：`RSI`内部使用指标`UpDay`进行计算。该子指标不会将所有数据保留在内存中

      * 这允许保留plotting和preloading主动。

      * runonce 将被停用

    * `-2`：作为策略属性保留的数据和指标将所有数据保留在内存中。例如：RSI内部使用指标UpDay进行计算。该子指标不会将所有数据保留在内存中. 如果在__init__某样东西 a = self.data.close - self.data.high中定义了，那么a 不会将所有数据保留在内存中

        * 这允许保留plotting和preloading主动。

        * runonce 将被停用

与往常一样，一个例子值得一千个单词。示例脚本显示了差异。它违背了雅虎的1996年至2015年的日数据，共4965天。
> 这是一个小样本。每天交易14小时的EuroStoxx50期货在短短1个月的交易中将产生约18000条1分钟的柱线。

执行1st脚本可以查看在没有请求节省内存时使用了多少个内存位置：
```
$ ./memory-savings.py --save 0
Total memory cells used: 506430
```
对于level 1(全部节省):
```
$ ./memory-savings.py --save 1
Total memory cells used: 2041
```
 系统中的每个 line 对象都使用1个 `collections.deque` 作为buffer（而不是 `array.array`），并且其长度限制在所请求操作的绝对最低要求。例：

* 在data Feed上使用 SimpleMovingAverage, 周期为30的策略。

在这种情况下，将进行以下调整：

* data feed将具有1个30个位置的buffer，SimpleMovingAverage需要该数量30,产生的下一个值

* SimpleMovingAverage将有一个buffer, position为1，因为除非需要其他指标（这将依赖于移动平均线），在此没有必要保持较大的缓冲。

> 此模式最吸引人且可能很重要的功能是，在脚本的整个生命周期中，使用的内存量保持不变。

无论data feed的大小如何。

如果长时间连接到live feed，这将很有用。

但要考虑到：

1. Plotting 不可用

2. 还有其他一些内存消耗来源，这些消耗会随着时间的推移而累积，例如该策略所产生的orders消耗。

3. 这种模式只能与使用 `runonce=False` 在 `cerebro`中。对于实时数据Feed，这也是强制性的，但是在简单的回测的情况下，此速度比 `runonce=True` 慢。  
可以肯定有一个折衷点，从这个折衷点来看，内存管理比逐步执行回测要珍贵，但这只能由平台的最终用户根据情况进行判断。

现在看下负水平。这些是为了在保持绘图可用的同时仍节省大量内存。

首先 level -1：
```
$ ./memory-savings.py --save -1
Total memory cells used: 184623
```
在这种情况下，level 1的指标（那些在策略声明）保持其全长缓冲区。但是，如果此指标依靠其他指标（是这种情况）来完成其工作，则子对象将是有界的。在这种情况下，我们从：

* 506430 内存下降到-> 184623

节省超过50％。

> 当然，array.array已经对对象进行了折中， `collections.deque`尽管在操作方面要快一些，但是在内存方面更昂贵。但是`collection.deque` 对象很小，节省的空间接近所使用的大致存储位置。

接下来看下 level -2，这也意味着保存在策略级别声明的已标记的指标不被plot：
```
$ ./memory-savings.py --save -2
Total memory cells used: 174695
```
现在没有节省太多。这是因为单个指标已被标记为不绘制：`TestInd().plotinfo.plot = False`

让我们看一下最后一个示例中的绘图：
```
$ ./memory-savings.py --save -2 --plot
Total memory cells used: 174695
```
![](./memory-savings.png)

对于感兴趣的读者，示例脚本可以对指标层次结构中遍历的每行对象进行详细分析。在启用绘图的情况下运行 （保存在）：-1
```
$ ./memory-savings.py --save -1 --lendetails
-- Evaluating Datas
---- Data 0 Total Cells 34755 - Cells per Line 4965
-- Evaluating Indicators
---- Indicator 1.0 Average Total Cells 30 - Cells per line 30
---- SubIndicators Total Cells 1
---- Indicator 1.1 _LineDelay Total Cells 1 - Cells per line 1
---- SubIndicators Total Cells 1
...
---- Indicator 0.5 TestInd Total Cells 9930 - Cells per line 4965
---- SubIndicators Total Cells 0
-- Evaluating Observers
---- Observer 0 Total Cells 9930 - Cells per Line 4965
---- Observer 1 Total Cells 9930 - Cells per Line 4965
---- Observer 2 Total Cells 9930 - Cells per Line 4965
Total memory cells used: 184623
```
相同，但1启用了最大节省量（）：
```
$ ./memory-savings.py --save 1 --lendetails
-- Evaluating Datas
---- Data 0 Total Cells 266 - Cells per Line 38
-- Evaluating Indicators
---- Indicator 1.0 Average Total Cells 30 - Cells per line 30
---- SubIndicators Total Cells 1
...
---- Indicator 0.5 TestInd Total Cells 2 - Cells per line 1
---- SubIndicators Total Cells 0
-- Evaluating Observers
---- Observer 0 Total Cells 2 - Cells per Line 1
---- Observer 1 Total Cells 2 - Cells per Line 1
---- Observer 2 Total Cells 2 - Cells per Line 1
```
的2次立即输出示出了如何中相应的线数据进料已被封端至38存储器位置，而不是4965其包括完整的数据源的长度。

而指标和观察家已经在可能的情况要加盖1在输出的最后几行看到。

## Script Code and Usage
可作为来源中的样本backtrader。用法：
```
$ ./memory-savings.py --help
usage: memory-savings.py [-h] [--data DATA] [--save SAVE] [--datalines]
                         [--lendetails] [--plot]

Check Memory Savings

optional arguments:
  -h, --help    show this help message and exit
  --data DATA   Data to be read in (default: ../../datas/yhoo-1996-2015.txt)
  --save SAVE   Memory saving level [1, 0, -1, -2] (default: 0)
  --datalines   Print data lines (default: False)
  --lendetails  Print individual items memory usage (default: False)
  --plot        Plot the result (default: False)
```
代码如下:
```
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import argparse
import sys

import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.indicators as btind
import backtrader.utils.flushfile


class TestInd(bt.Indicator):
    lines = ('a', 'b')

    def __init__(self):
        self.lines.a = b = self.data.close - self.data.high
        self.lines.b = btind.SMA(b, period=20)


class St(bt.Strategy):
    params = (
        ('datalines', False),
        ('lendetails', False),
    )

    def __init__(self):
        btind.SMA()
        btind.Stochastic()
        btind.RSI()
        btind.MACD()
        btind.CCI()
        TestInd().plotinfo.plot = False

    def next(self):
        if self.p.datalines:
            txt = ','.join(
                ['%04d' % len(self),
                 '%04d' % len(self.data0),
                 self.data.datetime.date(0).isoformat()]
            )

            print(txt)

    def loglendetails(self, msg):
        if self.p.lendetails:
            print(msg)

    def stop(self):
        super(St, self).stop()

        tlen = 0
        self.loglendetails('-- Evaluating Datas')
        for i, data in enumerate(self.datas):
            tdata = 0
            for line in data.lines:
                tdata += len(line.array)
                tline = len(line.array)

            tlen += tdata
            logtxt = '---- Data {} Total Cells {} - Cells per Line {}'
            self.loglendetails(logtxt.format(i, tdata, tline))

        self.loglendetails('-- Evaluating Indicators')
        for i, ind in enumerate(self.getindicators()):
            tlen += self.rindicator(ind, i, 0)

        self.loglendetails('-- Evaluating Observers')
        for i, obs in enumerate(self.getobservers()):
            tobs = 0
            for line in obs.lines:
                tobs += len(line.array)
                tline = len(line.array)

            tlen += tdata
            logtxt = '---- Observer {} Total Cells {} - Cells per Line {}'
            self.loglendetails(logtxt.format(i, tobs, tline))

        print('Total memory cells used: {}'.format(tlen))

    def rindicator(self, ind, i, deep):
        tind = 0
        for line in ind.lines:
            tind += len(line.array)
            tline = len(line.array)

        thisind = tind

        tsub = 0
        for j, sind in enumerate(ind.getindicators()):
            tsub += self.rindicator(sind, j, deep + 1)

        iname = ind.__class__.__name__.split('.')[-1]

        logtxt = '---- Indicator {}.{} {} Total Cells {} - Cells per line {}'
        self.loglendetails(logtxt.format(deep, i, iname, tind, tline))
        logtxt = '---- SubIndicators Total Cells {}'
        self.loglendetails(logtxt.format(deep, i, iname, tsub))

        return tind + tsub


def runstrat():
    args = parse_args()

    cerebro = bt.Cerebro()
    data = btfeeds.YahooFinanceCSVData(dataname=args.data)
    cerebro.adddata(data)
    cerebro.addstrategy(
        St, datalines=args.datalines, lendetails=args.lendetails)

    cerebro.run(runonce=False, exactbars=args.save)
    if args.plot:
        cerebro.plot(style='bar')


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Check Memory Savings')

    parser.add_argument('--data', required=False,
                        default='../../datas/yhoo-1996-2015.txt',
                        help='Data to be read in')

    parser.add_argument('--save', required=False, type=int, default=0,
                        help=('Memory saving level [1, 0, -1, -2]'))

    parser.add_argument('--datalines', required=False, action='store_true',
                        help=('Print data lines'))

    parser.add_argument('--lendetails', required=False, action='store_true',
                        help=('Print individual items memory usage'))

    parser.add_argument('--plot', required=False, action='store_true',
                        help=('Plot the result'))

    return parser.parse_args()


if __name__ == '__main__':
    runstrat()
```