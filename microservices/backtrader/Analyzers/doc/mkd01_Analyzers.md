- [Analyzers](#analyzers)
  - [Nature of analyzers](#nature-of-analyzers)
  - [Location in the ecosystem](#location-in-the-ecosystem)
    - [Additional Location](#additional-location)
  - [Attributes](#attributes)
    - [Returning the analysis](#returning-the-analysis)
  - [Modus operandi(操作方式)](#modus-operandi操作方式)
  - [Analyzer Patterns](#analyzer-patterns)
  - [A quick example](#a-quick-example)
  - [Forensic Analysis of an Analyzer](#forensic-analysis-of-an-analyzer)
  - [Reference](#reference)
    - [class backtrader.Analyzer()](#class-backtraderanalyzer)
    - [start()](#start)
    - [stop()](#stop)
    - [prenext()](#prenext)
    - [nextstart()](#nextstart)
    - [next()](#next)
    - [notify_cashvalue(cash, value)](#notify_cashvaluecash-value)
    - [notify_fund(cash, value, fundvalue, shares)](#notify_fundcash-value-fundvalue-shares)
    - [notify_order(order)](#notify_orderorder)
    - [notify_trade(trade)](#notify_tradetrade)
    - [get_analysis()](#get_analysis)
    - [create_analysis()](#create_analysis)
    - [print(*args, **kwargs)](#printargs-kwargs)
    - [pprint(*args, **kwargs)](#pprintargs-kwargs)
    - [len()](#len)
- [Analyzers - PyFolio](#analyzers---pyfolio)
- [Analyzers - PyFolio - Integration](#analyzers---pyfolio---integration)
- [Analyzers - Reference](#analyzers---reference)
-------------------------------------------------------------
# Analyzers
无论是回测还是交易，能够分析交易系统的性能可以知道不止获得利润，而且承担的风险是否过大, 与参考资产（或无风险资产）相比, 是否值得付出努力。

那就是 `Analyzer` 对象族的来源：提供对发生的事件甚至实际发生的事件的分析。

## Nature of analyzers
该接口是按照 `Lines` 对象的接口建模的，例如具有 `next` 方法，但有一个主要区别：

* `Analyzers` 不保存 `lines`。

这意味着它们在内存方面并不昂贵，因为即使在分析了数千个价格 bars 之后，它们仍可能仅将单个结果保存在内存中。

## Location in the ecosystem
`Analyzer` 通过 `cerebro` 实例将对象（例如策略，观察者和数据）添加到系统中：
```
addanalyzer(ancls, *args, **kwargs)
```
但是当涉及到 `cerebro.run` 操作时，系统中存在的每种策略都会发生以下情况:

* `ancls` 将在 `cerebro.run` 期间实例化, 带着参数`*args` 和 `**kwargs`

* 该 `ancls` 的实例将附加到该策略

这意味着：

* 假如回溯测试运行包含3个 strategies , 则3个 `ancls` 的实例将被创建, 他们每个将被连接到一个不同的策略。

原则：analyzer 分析单个策略的性能，而不是整个系统的性能

### Additional Location
某些 `Analyzer` 对象实际上可能会使用其他分析器来完成其工作。例如： `SharpeRatio` 使用 `TimeReturn` 的输出进行计算。

这些 `sub-analyzers` 或 `slave-analyzers` 也将被插入到与创建它们的策略相同的策略中。但是它们对于用户是完全不可见的。

## Attributes
为了执行预期的工作，为Analyzer对象提供了一些默认属性，这些属性会自动传递并在实例中设置以便于使用：

* `self.strategy`：策略子类的引用, analyzer 对象运行在该策略中。策略可以访问的任何内容也可以被分析器访问

* `self.datas[x]`：策略中存在的data Feed数组。尽管可以通过策略引用来访问，但是快捷方式使工作更加舒适。

* `self.data`：`self.datas[0]`的快捷方式，提供额外的舒适感。

* `self.dataX`：`self.datas[x]`的快捷方式 

可以使用其他一些别名，尽管它们可能有点过头了：
* `self.dataX_Y`    
    `X` 是 `self.datas[X]` 的引用, `Y` 指向 line, 最终指向 `self.datas[X].lines[Y]`

如果line有名字, 下面这种方式也可用:
* `self.dataX_Name`     
    相比 `self.datas[X].Name` 方式, 方便一点

对于第一个数据, 后面两种简写可以省去 `X`, 例如:
* `self.data_2` refers to `self.datas[0].lines[2]`

同时:
* `self.data_close` refers to `self.datas[0].close`

### Returning the analysis
分析器基类创建 `self.rets`（`collections.OrderedDict`类型）成员属性返回分析。这是在方法 `create_analysis` 中完成的，如果创建自定义分析器，该方法可以被子类覆盖。

## Modus operandi(操作方式)
尽管 `Analyzer` 对象不是 `Lines` 对象，因此不能在 lines 上进行迭代，但是它们被设计为遵循相同的操作模式。

1. 在系统投入运行之前实例化（因此调用 `__init__`）
2. 通过`start`发出信号, 开始运行 
3. `prenext/nextstart/next`的调用将跟随在策略中 indicator 所计算的最小周期之后

    `prenext` 和 `nextstart` 的默认行为是激活 `next`，因为分析器可能从系统处于活动状态的第一刻就开始分析。

    在 Lines 的对象中, 可能是习惯性地调用 len(self) ，检查bars的实际数量。这也可以在 `Analyzers` 中通过返回 `self.strategy` 做到
4. 订单和交易将通过 `notify_order` 和 `notify_trade` 通知, 像 `strategy` 一样 
5. Cash 和 value 也可以被通知，通过 `notify_cashvalue` 方法完成, 就像策略一样
6. Cash，value，fundvalue 和 fund shares 也可得到通知，通过 notify_fund 方法完成, 就像策略一样
7. 将调用 `stop` 来发出操作结束的信号

一旦完成正常的操作流程，分析仪便会采用其他方法来提取/输出信息

* `get_analysis`：理想情况下（不强制执行）返回包含分析结果的 dict-like 对象。
    ```
    def get_analysis(self):
        '''Returns a *dict-like* object with the results of the analysis
    
        The keys and format of analysis results in the dictionary is
        implementation dependent.
    
        It is not even enforced that the result is a *dict-like object*, just
        the convention
    
        The default implementation returns the default OrderedDict ``rets``
        created by the default ``create_analysis`` method
    
        '''
        return self.rets
    ```
* `print`: 使用标准 `backtrader.WriterFile`（除非覆盖）来写入来自 `get_analysis` 的分析结果。
    ```
    def print(self, *args, **kwargs):
        '''Prints the results returned by ``get_analysis`` via a standard
        ``Writerfile`` object, which defaults to writing things to standard
        output
        '''
        writer = bt.WriterFile(*args, **kwargs)
        writer.start()
        pdct = dict()
        pdct[self.__class__.__name__] = self.get_analysis()
        writer.writedict(pdct)
        writer.stop()
    ```
* `pprint`（pretty print）: 使用 Python pprint模块来打印 `get_analysis` 结果。
    ```
    def pprint(self, *args, **kwargs):
        '''Prints the results returned by ``get_analysis`` using the pretty
        print Python module (*pprint*)
        '''
        pp.pprint(self.get_analysis(), *args, **kwargs)
    ```
最后：

* `get_analysis` 返回成员属性 `self.rets`(collections.OrderedDict类型)，分析程序将分析结果写入其中。
    
    Analyzer的子类可以重写此方法以更改此行为

## Analyzer Patterns
在backtrader平台中, 分析器对象的开发提供了两种不同的使用模式来生成分析：

1. 在执行过程中，通过 `notify_xxx` 和 `next` 方法收集信息，并在 `next` 中生成当前的分析信息

    比如, `TradeAnalyzer`, 只使用 `notify_trade` 方法来生成统计数据。

2. 收集（或不收集）上述信息，但在 `stop` 方法执行过程中单次生成分析

    比如, 计算`SQN`（System Quality Number）时要在 `notify_trade` 过程中收集 trade 信息，在stop方法中统计生成

## A quick example
```
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime

import backtrader as bt
import backtrader.analyzers as btanalyzers
import backtrader.feeds as btfeeds
import backtrader.strategies as btstrats

cerebro = bt.Cerebro()

# data
dataname = '../datas/sample/2005-2006-day-001.txt'
data = btfeeds.BacktraderCSVData(dataname=dataname)

cerebro.adddata(data)

# strategy
cerebro.addstrategy(btstrats.SMA_CrossOver)

# Analyzer
cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe')

thestrats = cerebro.run()
thestrat = thestrats[0]

print('Sharpe Ratio:', thestrat.analyzers.mysharpe.get_analysis())
```
脚本运行:
```
$ ./analyzer-test.py
Sharpe Ratio: {'sharperatio': 11.647332609673256}
```
没有绘图, 因为 `SharpeRatio` 是一个最后统计的值

## Forensic Analysis of an Analyzer
`Analyzers` 不是 `Lines` 对象, 但是他们在 `backtrader` 生态中无缝对接, 遵循了几个Lines对象的内部API约定（实际上是它们的混合）

> SharpeRatio的代码已经进化到考虑年率化，这里的版本只是一个参考。

有一个 `SharpeRatio_A`, 提供了直接年化表示, 无视看到的 `timeframe` 

SharpeRatio作为基础的代码（简化版）
```
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import operator

from backtrader.utils.py3 import map
from backtrader import Analyzer, TimeFrame
from backtrader.mathsupport import average, standarddev
from backtrader.analyzers import AnnualReturn


class SharpeRatio(Analyzer):
    params = (('timeframe', TimeFrame.Years), ('riskfreerate', 0.01),)

    def __init__(self):
        super(SharpeRatio, self).__init__()
        self.anret = AnnualReturn()

    def start(self):
        # Not needed ... but could be used
        pass

    def next(self):
        # Not needed ... but could be used
        pass

    def stop(self):
        retfree = [self.p.riskfreerate] * len(self.anret.rets)
        retavg = average(list(map(operator.sub, self.anret.rets, retfree)))
        retdev = standarddev(self.anret.rets)

        self.ratio = retavg / retdev

    def get_analysis(self):
        return dict(sharperatio=self.ratio)
```
代码可以被拆解成如下:
* `params`      
    尽管示例中声明的没有全部使用, 但是Analyzers如同 backtrader 其他大多数对象一样, 支持参数

* `__init__`    
    就像策略在`__init__`中声明指标一样，分析器也是如此。

    在这种情况下：`SharpeRatio`是用年回报率(Annual Returns)计算的。计算将自动进行，`SharpeRatio` 可自行计算。

    > SharpeRatio的实际实现使用了更通用和更晚开发的 TimeReturn 分析器

* `next` method
    `SharpeRatio` 不需要它，但是每次调用父策略之后都会调用这个方法

* `start` method
    在回溯测试开始之前调用。可用于额外的初始化任务。`Sharperatio` 不需要它

* `stop` method
    在回溯测试结束后立即调用。和 `SharpeRatio` 一样，它可以用来完成/进行计算

* `get_analysis` method (returns a dictionary)
    外部调用者访问生成的分析结果

    返回一个字典类型的分析结果

------------------------------------------------------------------
## Reference

### class backtrader.Analyzer()
分析器基类。所有的分析器都是这个的子类

Analyzer 实例在策略框架中运行，并为该策略提供分析。

自动设置成员属性：

* `self.strategy` (giving access to the strategy and anything accessible from it)

* `self.datas[x]` giving access to the array of data feeds present in the the system, which could also be accessed via the strategy reference

* `self.data`, giving access to `self.datas[0]`

* `self.dataX` -> `self.datas[X]`

* `self.dataX_Y` -> `self.datas[X].lines[Y]`

* `self.dataX_name` -> `self.datas[X].name`

* `self.data_name` -> `self.datas[0].name`

* `self.data_Y` -> `self.datas[0].lines[Y]`

这不是一个Lines对象，但是方法和操作遵循相同的设计

* `__init__` during instantiation and initial setup

* ` start / stop` to signal the begin and end of operations

* `prenext / nextstart / next` family of methods that follow the calls made to the same methods in the strategy

* `notify_trade / notify_order / notify_cashvalue / notify_fund` which receive the same notifications as the equivalent methods of the strategy

操作模式为开放式，无模式优先。因此，分析可以在 `next` 调用中生成，在stop期间的操作结束时生成，甚至可以使用 `notify_trade` 这样的单一方法生成。

重要的是重写 `get_analysis` 返回包含分析结果的dict-like对象（实际格式取决于实现）

### start()
调用以指示操作的开始，给分析器时间设置所需的内容

### stop()
调用以指示操作结束，给分析器时间关闭所需的东西

### prenext()
为策略的每次 `prenext` 调用，直到达到策略的最短周期

分析器的默认行为是调用 `next`

### nextstart()
Invoked exactly once for the nextstart invocation of the strategy, when the minimum period has been first reached
在策略的 nextstart调用, 且只调用一次，当第一次达到最小周期时

### next()
一旦达到策略的最小周期条件，每次调用策略的 next 时调用

### notify_cashvalue(cash, value)
Receives the cash/value notification before each next cycle
在 next 前收到 cash/value 通知

### notify_fund(cash, value, fundvalue, shares)
Receives the current cash, value, fundvalue and fund shares
接收当前cash、value、fundvalue 和 fund shares

### notify_order(order)
Receives order notifications before each next cycle

### notify_trade(trade)
Receives trade notifications before each next cycle

### get_analysis()
Returns a dict-like object with the results of the analysis

The keys and format of analysis results in the dictionary is implementation dependent.

It is not even enforced that the result is a dict-like object, just the convention

The default implementation returns the default OrderedDict rets created by the default create_analysis method

### create_analysis()
Meant to be overriden by subclasses. Gives a chance to create the structures that hold the analysis.

The default behaviour is to create a OrderedDict named rets

### print(*args, **kwargs)
Prints the results returned by get_analysis via a standard Writerfile object, which defaults to writing things to standard output

### pprint(*args, **kwargs)
Prints the results returned by get_analysis using the pretty print Python module (pprint)

### len()
Support for invoking len on analyzers by actually returning the current length of the strategy the analyzer operates on

-------------------------------------------------------------
# [Analyzers - PyFolio](./mkd02_PyFolio.md)
# [Analyzers - PyFolio - Integration](./mkd03_Pyfolio_Integration.md)
# [Analyzers - Reference](./mkd04_Reference.md)