- [Data Feeds - Filters](#data-feeds---filters)
  - [Purpose](#purpose)
  - [Filters at work](#filters-at-work)
  - [Filter Interface](#filter-interface)
  - [A Sample Filter](#a-sample-filter)
  - [Data Pseudo-API for Filters](#data-pseudo-api-for-filters)
  - [Another example: Pinkfish Filter](#another-example-pinkfish-filter)
- [Filters Reference](#filters-reference)
  - [SessionFilter](#sessionfilter)
  - [SessionFilterSimple](#sessionfiltersimple)
  - [SessionFilller](#sessionfilller)
  - [CalendarDays](#calendardays)
  - [BarReplayer_Open](#barreplayer_open)
  - [DaySplitter_Close](#daysplitter_close)
  - [HeikinAshi](#heikinashi)
  - [Renko](#renko)
---------------------------------------
# Data Feeds - Filters 
此功能是 `backtrader` 添加的相对较晚的功能，已经安装到存在的内部组件中。这使得它不像所希望的那样灵活，并且具有100%完整的功能，但是在许多情况下仍然可以达到目的。

尽管该实现尝试允许即插即用过滤器链接，但由于预先存在的内部结构，很难确保始终能够实现这一点。因此，一些过滤器可能是连锁的，而另一些则不是。

## Purpose

* 转换 data Feed 的值, 以提供一个不同的 data Feed

开始实现是为了简化 cerebro API 直接使用的两个明显的过滤器。他们是：

* `Resampling`（`cerebro.resampledata`）    
  在这里，过滤器变换输入 data feed 的 `timeframe` 和 `compression` 。例如：

    > (Seconds, 1) -> (Days, 1)

    这意味着原始 data feed 是分辨率为1秒的 bars。该重采样滤波器截取数据并对其进行缓冲，直到它可以提供一个1 Day bar。这将发生在第二天的1秒条出现时。

* `Replaying` （`cerebro.replaydata`）  
  对于与上述相同的时间范围，过滤器将使用1秒分辨率重建 1 day bar。
  
  这意味着 1 day bar 的发送次数与 1 second bar 的发送次数一样多，并已更新为包含最新信息。
  
  例如，这模拟了实际交易日的发展方式。
  
  > 注意    
  > len(data)只要日期不改变，数据的长度以及策略的长度就保持不变。

## Filters at work
给定一个现有的 data feed/source，您可以使用 data feed 的 addfilter 方法：
```
data = MyDataFeed(dataname=myname)
data.addfilter(filter, *args, **kwargs)
cerebro.addata(data)
```
甚至它可以兼容 resample/replay 过滤，以下可以这么操作:
```
data = MyDataFeed(dataname=myname)
data.addfilter(filter, *args, **kwargs)
cerebro.replaydata(data)
```

## Filter Interface
filter必须符合以下接口定义

* 一个可调用对象，它接受该签名
  > callable(data, *args, **kwargs)

或者

* 一个类能被实例化，实例能被调用

    * 实例化的 `__init__` 方法必须支持如下签名:
    ```
    def __init__(self, data, *args, **kwargs)
    ```

    * `__call__` 方法签名如下:
    ```
    def __call__(self, data, *args, **kwargs)
    ```
    从 data feed 传进来的每一个新的值都将调用实例。`*args` 和 `*kwargs` 与 `__init__` 方法中一致

    返回值:
    ```
    * `True`: the inner data fetching loop of the data feed must retry
    fetching data from the feed, becaue the length of the stream was
    manipulated

    * `False` even if data may have been edited (example: changed
    `close` price), the length of the stream has remain untouched
    ```
    
    在基于类的过滤器的情况下，可以实现其他方法
    * `last` 具有以下签名：
    ```
    def last(self, data, *args, **kwargs)
    ```
    data feed 结束时将调用此方法，从而允许过滤器传递可能已缓存的数据。典型的情况是 重采样，因为1个bar的 buffered 是直到看到下一个时间段的数据为止。data feed 结束时，没有新数据可以将缓冲的数据 push out。

    last 提供了将缓冲的数据推出的机会。

  如果filter没有参数, 那么签名可以被如下简化:
  ```
  def __init__(self, data, *args, **kwargs) -> def __init__(self, data)
  ```

## A Sample Filter
一个filter的快速实现:
```
class SessionFilter(object):
    def __init__(self, data):
        pass

    def __call__(self, data):
        if data.p.sessionstart <= data.datetime.time() <= data.p.sessionend:
            # bar is in the session
            return False  # tell outer data loop the bar can be processed

        # bar outside of the regular session times
        data.backwards()  # remove bar from data stack
        return True  # tell outer data loop to fetch a new bar
```
* 使用 `data.p.sessionstart` 和 `data.p.sessionend`（标准数据Feed参数）来确定会话中是否有一个bar。

* 如果处于会话中，则返回 False, 表示未执行任何操作，并且当前的 bar 处理可以继续

* 如果不在会话中，则将 bar 从流中删除并返回 True, 表示必须获取新的 bar。

> `data.backwards()` 使用 `LineBuffer interface`. backtrader的底层机制

使用此过滤器：

某些 data feed 包含非正常交易时间数据，交易者可能不感兴趣。使用此过滤器，将仅考虑会话中的 bar。

## Data Pseudo-API for Filters
在上面的示例中，已显示了过滤器如何调用 `data.backwards()` 以从流中删除当前bar。来自datafeed 对象的有用调用（被称为过滤器的伪API）是：

* `data.backwards(size=1, force=False)`：   
  通过向后移动逻辑指针，从数据流中删除 size 条（默认为1）bars。如果为 force=True，则还将删除物理存储。

  移除物理存储是一项微妙的操作，仅意味着对内部操作的 hack。

* `data.forward(value=float('NaN'), size=1)`：  
  向前移动 size 大小的 bars 存储空间，并在需要时增加物理存储空间并填充 value

* `data._addtostack(bar, stash=False)`：  
  添加 bar 到堆栈中供以后处理。bar 是一个可迭代对象, 包含与 data Feed 中 lines 数据一样多的值。

  如果 `stash=False` , 添加到堆栈中的 bar 将在下一次迭代开始时被系统立即消耗。

  如果 `stash=True` , 该 bar 会经历的整个循环处理包括可能由过滤器重新解析

* `data._save2stack(erase=False, force=False)`：  
  将当前数据 bar 保存到堆栈中供以后处理。如果 `erase=True` , 随后 `data.backwards` 将被调用，并将收到参数 `force`

* `data._updatebar(bar, forward=False, ago=0)`：  
  使用迭代器 bar 中的值, 覆盖数据流 `ago` 位置中的值。默认值`ago=0`，当前 bar 将被更新。使用 -1，更新上一个。

## Another example: Pinkfish Filter
这是一个可以被链接 chained 的过滤器的示例，并且意味着可以链接到另一个过滤器，即重播过滤器 replay filter。Pinkfish 名字源自一个 library , 描述其主页的想法：使用盘中的数据来执行 daily 数据的操作。

为了要达到这个效果：

* 一个 daily bar 将分为2个部分：`OHL` 和 `C`。

* 这两个片段通过 replay 链接在一起，在流中发生以下事件：
  ```
  With Len X     -> OHL
  With Len X     -> OHLC
  With Len X + 1 -> OHL
  With Len X + 1 -> OHLC
  With Len X + 2 -> OHL
  With Len X + 2 -> OHLC
  ...
  ```

处理逻辑:
* 当一个 OHLC bar 被接收到, 然后被复制到一个可交互且分解成为：

  * 一个OHL bar。因为这个概念实际上不存收盘价，所以将收盘价替换为开盘价以真正形成一个OHLO bar。

  * 一个 C bar 也并不存在。实际情况是，它将像 tick 一样传递 CCCC

  * volume 如果在两个部分之间分配

  * 从流中删除当前 bar

  * 该OHLO部分被放入 stack 以便立即处理

  * 该CCCC部分被放入 stash 在下一轮处理

  * 由于堆栈中有立即处理的内容，因此过滤器返回 False。

该过滤器可与以下功能一起使用：

* 这个 replay filter 把 `OHLO` 和 `CCCC` 部分放一起, 最终实现的 OHLC bar。

用例：

* 如果今天的最大值的是在过去的20个 sessions 最高的最大值, 发出 平仓`Close` 订单, 第二个tick执行。

```
class DaySplitter_Close(bt.with_metaclass(bt.MetaParams, object)):
    '''
    Splits a daily bar in two parts simulating 2 ticks which will be used to
    replay the data:

      - First tick: ``OHLX``

        The ``Close`` will be replaced by the *average* of ``Open``, ``High``
        and ``Low``

        The session opening time is used for this tick

      and

      - Second tick: ``CCCC``

        The ``Close`` price will be used for the four components of the price

        The session closing time is used for this tick

    The volume will be split amongst the 2 ticks using the parameters:

      - ``closevol`` (default: ``0.5``) The value indicate which percentage, in
        absolute terms from 0.0 to 1.0, has to be assigned to the *closing*
        tick. The rest will be assigned to the ``OHLX`` tick.

    **This filter is meant to be used together with** ``cerebro.replaydata``

    '''
    params = (
        ('closevol', 0.5),  # 0 -> 1 amount of volume to keep for close
    )

    # replaying = True

    def __init__(self, data):
        self.lastdt = None

    def __call__(self, data):
        # Make a copy of the new bar and remove it from stream
        datadt = data.datetime.date()  # keep the date

        if self.lastdt == datadt:
            return False  # skip bars that come again in the filter

        self.lastdt = datadt  # keep ref to last seen bar

        # Make a copy of current data for ohlbar
        ohlbar = [data.lines[i][0] for i in range(data.size())]
        closebar = ohlbar[:]  # Make a copy for the close

        # replace close price with o-h-l average
        ohlprice = ohlbar[data.Open] + ohlbar[data.High] + ohlbar[data.Low]
        ohlbar[data.Close] = ohlprice / 3.0

        vol = ohlbar[data.Volume]  # adjust volume
        ohlbar[data.Volume] = vohl = int(vol * (1.0 - self.p.closevol))

        oi = ohlbar[data.OpenInterest]  # adjust open interst
        ohlbar[data.OpenInterest] = 0

        # Adjust times
        dt = datetime.datetime.combine(datadt, data.p.sessionstart)
        ohlbar[data.DateTime] = data.date2num(dt)

        # Ajust closebar to generate a single tick -> close price
        closebar[data.Open] = cprice = closebar[data.Close]
        closebar[data.High] = cprice
        closebar[data.Low] = cprice
        closebar[data.Volume] = vol - vohl
        ohlbar[data.OpenInterest] = oi

        # Adjust times
        dt = datetime.datetime.combine(datadt, data.p.sessionend)
        closebar[data.DateTime] = data.date2num(dt)

        # Update stream
        data.backwards(force=True)  # remove the copied bar from stream
        data._add2stack(ohlbar)  # add ohlbar to stack
        # Add 2nd part to stash to delay processing to next round
        data._add2stack(closebar, stash=True)

        return False  # initial tick can be further processed from stack
```
--------------------------------------------------------------------
# Filters Reference

## SessionFilter
```
class backtrader.filters.SessionFilter(data)
```
此类可作为过滤器应用于数据源，并将过滤掉超出常规时段的bars, 留下盘中bars（即：前/后市场数据）

这是一个 “non-simple” 过滤器，必须管理数据堆栈（在 init 和 call 期间传递）

它不需要 “last” 方法，因为它没有什么可交付的


## SessionFilterSimple
```
class backtrader.filters.SessionFilterSimple(data)
```
此类可作为过滤器应用于数据源，并将过滤掉超出常规时段的bars, 留下盘中bars（即：前/后市场数据）

这是一个 “simple” 的过滤器，不能管理数据堆栈（在init和call期间传递）

它不需要 “last” 方法，因为它没有什么可交付的

bar 的管理工作将由 `SimpleFilterWrapper` 类完成，该类在 `DataBase.addfilter_simple` 调用期间添加


## SessionFilller
```
class backtrader.filters.SessionFiller(data)
```
Bar Filler 在声明的 session 开始/结束时间之内的数据源进行填充。

填充 bar 是使用声明的数据源构造的，`timeframe` 和 `compression`（用于计算中间的丢失时间）

参数：

* fill_price（def：None）：

  如果为 None，则使用前一个bar的收盘价。要以未在绘图中显示的bar(例如 time )结束，请使用float（'Nan'）

* fill_vol（def：float（'NaN'））：

  用于填充缺失volume的值

* fill_oi（def：float（'NaN'））：

  用于填补缺失的未平仓头寸的值

* skip_first_fill（def：`True`）：

  根据第一个有效bar, 而不是session start, 来fill bar


## CalendarDays
```
class backtrader.filters.CalendarDays(data)
```
Bar Filler 可将缺少的日历日添加到交易日中

参数：

* fill_price（def：None）：

  0：给定值填充0
  
  None：使用最近的已知收盘价
  
  -1：使用最后一个 bar 的中点（average(High-Low)）

* fill_vol（def：float（'NaN'））：

  用于填充缺失的 volume 值

* fill_oi（def：float（'NaN'））：

  用于填补缺失的未平仓头寸的值


## BarReplayer_Open
```
class backtrader.filters.BarReplayer_Open(data)
```
此过滤器将一个 bar 分为两个部分：

* `Open`：在初始化 bar 时, bar 的开盘价将用于交付相等的四个成分（OHLC）

  此初始化 bar 的 volume/未平仓量(openinterest)字段为 0

* `OHLC`：原始的 bar 随附原始的 volume/openinterest

此拆分模拟了replay，而无需使用 replay filter。


## DaySplitter_Close
```
class backtrader.filters.DaySplitter_Close(data)
```
将 daily bar 分为两个部分，模拟2个 ticks，将用于重播数据：

* 第一个 tick： `OHLX`

  `Close` 将被替换为 `Open`, `High` 和 `Low` 的平均值

  这个 tick 使用 session opening time

* 第二个 tick： `CCCC`

  `Close` 价格将用于价格的四个组成部分

  这个 tick 使用 session closing time

volume 将使用以下参数在2个 tick 之间分配：

  * `closevol`（默认值: 0.5）   
  该值指示必须将哪个百分比（绝对值从0.0到1.0）分配给 closing tick。其余的将分配给OHLX tick。

该过滤器旨在与 `cerebro.replaydata` 一同使用

## HeikinAshi
```
class backtrader.filters.HeikinAshi(data)
```
这个 filter 重塑 open,high,low,close 来制造 HeikinAshi 蜡烛图

* [https://en.wikipedia.org/wiki/Candlestick_chart#Heikin_Ashi_candlesticks](https://en.wikipedia.org/wiki/Candlestick_chart#Heikin_Ashi_candlesticks)

* [http://stockcharts.com/school/doku.php?id=chart_school:chart_analysis:heikin_ashi](http://stockcharts.com/school/doku.php?id=chart_school:chart_analysis:heikin_ashi)

## Renko
```
class backtrader.filters.Renko(data)
```
修改数据流以绘制Renko bars（或 bricks）

参数：

* `hilo`（默认值：`False`）使用 high 和 low , 而不是 close 来确定是否需要新的 brick

* `size`（默认值：`None`）要为每个 brick 考虑的大小

* `autosize`（默认值：20.0）如果 `size` 为 `None`，它将用于自动计算 bricks 的大小（将当前价格除以给定值即可）

* `dynamic`（默认值：`False`）如果为`True`并使用`autosize`，则在移动到新 brick 时将重新计算 brick 的 size。当然，这将消除 Renko bricks 的完美对齐。

* `align`（默认值：1.0）使用因子来对齐砖的价格边界。例如，如果价格为 3563.25 且 align 为 10.0，则得出的对齐价格为 3560。计算：

  * 3563.25 / 10.0 = 356.325

  * 将其舍入并删除小数点后小数 -> 356

  * 356 * 10.0 -> 3560

[http://stockcharts.com/school/doku.php?id=chart_school:chart_analysis:renko](http://stockcharts.com/school/doku.php?id=chart_school:chart_analysis:renko)