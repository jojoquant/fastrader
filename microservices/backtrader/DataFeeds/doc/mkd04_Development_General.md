- [Data Feeds - Development - General](#data-feeds---development---general)
  - [简单的二进制 datafeed](#简单的二进制-datafeed)
    - [初始化](#初始化)
    - [Start](#start)
    - [Stop](#stop)
    - [Actual Loading](#actual-loading)
  - [其他二进制格式](#其他二进制格式)
  - [VChartData Test](#vchartdata-test)
  - [VChartData Full Code](#vchartdata-full-code)

--------------------------------------
# Data Feeds - Development - General
>示例中使用的二进制文件goog.fd属于VisualChart，不能使用分发backtrader

对于有兴趣直接使用二进制文件的用户，可以免费下载 [VisualChart](http://www.visualchart.com/)。

CSV Data feed 开发显示了如何添加基于 CSV 的data feeds。现有的基类CSVDataBase提供的框架将大部分工作从子类中移除，在大多数情况下，子类可以简单地完成这些工作：

```
def _loadline(self, linetokens):

  # parse the linetokens here and put them in self.lines.close,
  # self.lines.high, etc

  return True # if data was parsed, else ... return False
```

基类负责参数设置，初始化，文件打开，读取行，将tokens中的行拆分以及其他一些事情，例如跳过最终用户可能定义的日期范围（fromdate，todate）中不适合的行。

开发非CSV datafeed 遵循相同的模式，而无需深入了解已经拆分的行令牌。

要做的事情：

* 从`backtrader.feed.DataBase`派生
* 添加您可能需要的任何参数
* 如果需要初始化，请覆盖 `__init__(self)` 和/或 `start(self)`
* 如果需要任何清理代码，请覆盖 `stop(self)`
* 这项工作发生在必须始终被覆盖的方法内部： `_load(self)`

让我们看一下已经提供的参数 `backtrader.feed.DataBase`：

```
from backtrader.utils.py3 import with_metaclass

...
...

class DataBase(with_metaclass(MetaDataBase, dataseries.OHLCDateTime)):

    params = (('dataname', None),
        ('fromdate', datetime.datetime.min),
        ('todate', datetime.datetime.max),
        ('name', ''),
        ('compression', 1),
        ('timeframe', TimeFrame.Days),
        ('sessionend', None))
```

具有以下含义：

* `dataname` 使 data feed 能够识别如何获取数据。在此情况下, `CSVDataBase` 此参数应是文件或已经是类似文件的对象的路径。

* `fromdate` 和 `todate` 定义将传递给策略的日期范围。feed 提供的任何超出此范围的值都将被忽略

* `name` 是用于绘图

* `timeframe` 指示工作时间帧  
  备选值: `Ticks`, `Seconds`, `Minutes`, `Days`, `Weeks`, `Months` and `Years`

* `compression` (默认值:1)     
  每条 `bar` 中实际包含的 `bars` 个数。仅在数据 `Resampling/Replaying` 有效。

* `sessionend` (默认值:`None`)     
  如果传入（datetime.time对象），则将添加到 datafeed `datetime` 行中，该行允许标识会话结束


## 简单的二进制 datafeed

`backtrader` 已经为 VisualChart 的导出定义了CSV datafeed（VChartCSVData），但是也可以直接读取二进制数据文件。

让我们开始吧（完整的 datafeed 代码可以在底部找到）

### 初始化

二进制 VisualChart 数据文件可以包含 daily（扩展名.fd）或 日内数据（扩展名.min）。在此，该参数 `timeframe` 将用于区分正在读取的文件类型。

在`__init__`常量期间，每种类型的常量都不同。

```
    def __init__(self):
        super(VChartData, self).__init__()

        # Use the informative "timeframe" parameter to understand if the
        # code passed as "dataname" refers to an intraday or daily feed
        if self.p.timeframe >= TimeFrame.Days:
            self.barsize = 28
            self.dtsize = 1
            self.barfmt = 'IffffII'
        else:
            self.dtsize = 2
            self.barsize = 32
            self.barfmt = 'IIffffII'
```

### Start
datafeed 将在回测开始时启动（实际上在优化过程中可以多次启动）

在该`start`方法中，除非已传递类似文件的对象，否则打开二进制文件。
```
    def start(self):
        # the feed must start ... get the file open (or see if it was open)
        self.f = None
        if hasattr(self.p.dataname, 'read'):
            # A file has been passed in (ex: from a GUI)
            self.f = self.p.dataname
        else:
            # Let an exception propagate
            self.f = open(self.p.dataname, 'rb')
```

### Stop
回测完成时被调用, 如果一个文件被打开, 它将被关闭
```
    def stop(self):
        # Close the file if any
        if self.f is not None:
            self.f.close()
            self.f = None
```

### Actual Loading
实际工作在 `_load` 中完成。调用以加载下一组数据，在本例中为下一个：`datetime，open，high，low，close，volume，openinterest`。在 `backtrader` 中, “actual” 时刻对应于 index 0。

从打开的文件中读取多个字节（由`__init__`期间设置的常量确定），与`struct`模块一起解析，并在需要时进行进一步处理（如日期和时间的 divmod 操作），并存储在 datafeed 的 `lines` 中：`datetime, open, high, low, close, volume, openinterest`.

如果无法从文件中读取任何数据，则假定已达到文件结尾（EOF）

* 返回 False 表示没有更多数据的事实

否则，如果数据已被加载和解析：

* 返回 True 表示数据集加载成功

```
    def _load(self):
        if self.f is None:
            # if no file ... no parsing
            return False

        # Read the needed amount of binary data
        bardata = self.f.read(self.barsize)
        if not bardata:
            # if no data was read ... game over say "False"
            return False

        # use struct to unpack the data
        bdata = struct.unpack(self.barfmt, bardata)

        # Years are stored as if they had 500 days
        y, md = divmod(bdata[0], 500)
        # Months are stored as if they had 32 days
        m, d = divmod(md, 32)
        # put y, m, d in a datetime
        dt = datetime.datetime(y, m, d)

        if self.dtsize > 1:  # Minute Bars
            # Daily Time is stored in seconds
            hhmm, ss = divmod(bdata[1], 60)
            hh, mm = divmod(hhmm, 60)
            # add the time to the existing atetime
            dt = dt.replace(hour=hh, minute=mm, second=ss)

        self.lines.datetime[0] = date2num(dt)

        # Get the rest of the unpacked data
        o, h, l, c, v, oi = bdata[self.dtsize:]
        self.lines.open[0] = o
        self.lines.high[0] = h
        self.lines.low[0] = l
        self.lines.close[0] = c
        self.lines.volume[0] = v
        self.lines.openinterest[0] = oi

        # Say success
        return True
```

## 其他二进制格式
相同的模型可以应用于任何其他二进制源：

* 数据库
* 分层数据存储
* 在线资源

再次执行以下步骤：

* `__init__` -> 实例的任何初始化代码，仅一次

* `start` -> 开始回测（一次或多次，如果将运行优化）   
  例如，这将打开与数据库的连接或与在线服务的套接字

* `stop` -> 清理，如关闭数据库连接或打开套接字

* `_load` -> 在数据库或在线源中查询下一组数据，并将其加载到 `lines` 对象的中。标准字段为：`datetime, open, high, low, close, volume, openinterest`

## VChartData Test
`VCharData` 从本地“ .fd”文件中加载 Google 的2006年的数据。

它仅用于加载数据，因此甚至不需要 `Strategy` 的子类。
```
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime

import backtrader as bt
from vchart import VChartData


if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro(stdstats=False)

    # Add a strategy
    cerebro.addstrategy(bt.Strategy)

    ###########################################################################
    # Note:
    # The goog.fd file belongs to VisualChart and cannot be distributed with
    # backtrader
    #
    # VisualChart can be downloaded from www.visualchart.com
    ###########################################################################
    # Create a Data Feed
    datapath = '../../datas/goog.fd'
    data = VChartData(
        dataname=datapath,
        fromdate=datetime.datetime(2006, 1, 1),
        todate=datetime.datetime(2006, 12, 31),
        timeframe=bt.TimeFrame.Days
    )

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    # Run over everything
    cerebro.run()

    # Plot the result
    cerebro.plot(style='bar')
```

## VChartData Full Code
```
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime
import struct

from backtrader.feed import DataBase
from backtrader import date2num
from backtrader import TimeFrame


class VChartData(DataBase):
    def __init__(self):
        super(VChartData, self).__init__()

        # Use the informative "timeframe" parameter to understand if the
        # code passed as "dataname" refers to an intraday or daily feed
        if self.p.timeframe >= TimeFrame.Days:
            self.barsize = 28
            self.dtsize = 1
            self.barfmt = 'IffffII'
        else:
            self.dtsize = 2
            self.barsize = 32
            self.barfmt = 'IIffffII'

    def start(self):
        # the feed must start ... get the file open (or see if it was open)
        self.f = None
        if hasattr(self.p.dataname, 'read'):
            # A file has been passed in (ex: from a GUI)
            self.f = self.p.dataname
        else:
            # Let an exception propagate
            self.f = open(self.p.dataname, 'rb')

    def stop(self):
        # Close the file if any
        if self.f is not None:
            self.f.close()
            self.f = None

    def _load(self):
        if self.f is None:
            # if no file ... no parsing
            return False

        # Read the needed amount of binary data
        bardata = self.f.read(self.barsize)
        if not bardata:
            # if no data was read ... game over say "False"
            return False

        # use struct to unpack the data
        bdata = struct.unpack(self.barfmt, bardata)

        # Years are stored as if they had 500 days
        y, md = divmod(bdata[0], 500)
        # Months are stored as if they had 32 days
        m, d = divmod(md, 32)
        # put y, m, d in a datetime
        dt = datetime.datetime(y, m, d)

        if self.dtsize > 1:  # Minute Bars
            # Daily Time is stored in seconds
            hhmm, ss = divmod(bdata[1], 60)
            hh, mm = divmod(hhmm, 60)
            # add the time to the existing atetime
            dt = dt.replace(hour=hh, minute=mm, second=ss)

        self.lines.datetime[0] = date2num(dt)

        # Get the rest of the unpacked data
        o, h, l, c, v, oi = bdata[self.dtsize:]
        self.lines.open[0] = o
        self.lines.high[0] = h
        self.lines.low[0] = l
        self.lines.close[0] = c
        self.lines.volume[0] = v
        self.lines.openinterest[0] = oi

        # Say success
        return True
```