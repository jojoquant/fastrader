- [Data Feeds](#data-feeds)
  - [Data Feeds 常用参数](#data-feeds-常用参数)
  - [CSV Data Feeds 常用参数](#csv-data-feeds-常用参数)
  - [GenericCSVData](#genericcsvdata)
- [Data Feeds - Extending](#data-feeds---extending)
- [Data Feeds - Development - CSV](#data-feeds---development---csv)
- [Data Feeds - Development - General](#data-feeds---development---general)
- [Data Feeds - Mutiple Timeframes](#data-feeds---mutiple-timeframes)
- [Data Feeds - Resample](#data-feeds---resample)
- [Data Feeds - Replay](#data-feeds---replay)
- [Data Feeds - Rollover](#data-feeds---rollover)
- [Data Feeds - Filters](#data-feeds---filters)
- [Data Feeds - Yahoo](#data-feeds---yahoo)
- [Data Feeds - Panda](#data-feeds---panda)
- [Data Feeds - Reference](#data-feeds---reference)
----------------------------------------------------
# Data Feeds
`backtrader` 随附了一组 Data Feed 解析器(在编写所有基于CSV时)，可让您从其他来源加载数据。

* Yahoo(在线或已保存到文件)
* VisualChart [请参见](www.visualchart.com)
* Backtrader CSV (用于测试的技巧格式)
* 通用CSV支持

从《快速入门》指南中可以清楚地看到，您已将数据供稿添加到 `Cerebro` 实例。稍后将使用 `data feeds` 给不同策略使用:

* 一个 `array self.datas`(插入顺序)
* `array` 对象的别名:
  * `self.data` 和 `self.data0` 指向第一个元素
  * `self.dataX` 指向数组中索引为 X 的元素

快速提醒您如何进行插入:
```
import backtrader as bt
import backtrader.feeds as btfeeds

data = btfeeds.YahooFinanceCSVData(dataname='wheremydatacsvis.csv')

cerebro = bt.Cerebro()

cerebro.adddata(data)  # a 'name' parameter can be passed for plotting purposes
```
-----------------------------------------------------
## Data Feeds 常用参数
该 data feed 可以直接从Yahoo下载数据并将其馈送到系统中。

参数:
* `dataname` (默认值:`None`)必须提供   
  根据 data feed 的类型(文件位置，ticker，…)而异。

* `name` (默认:'')     
  绘图中用于装饰目的。如果未指定，则可能来自dataname(例如:文件路径的最后一部分)

* `fromdate` (默认值:mindate)     
  Python datetime对象，表示忽略此日期之前的数据

* `todate` (默认值:maxdate)    
  Python datetime对象，指示该日期之后的数据应该被忽略

* `timeframe` (默认值:`TimeFrame.Days`)  
  可选值包括:`Ticks`，`Seconds`，`Minutes`，`Days`，`Weeks`， `Months`和`Years`

* `compression` (默认值:1)     
  每条 `bar` 中实际包含的 `bars` 个数。仅在数据 `Resampling/Replaying` 有效。

* `sessionstart` (默认值:`None`)   
  表示数据的会话开始时间。可能被一些 classes 在一些场景使用(比如: resampling)

* `sessionend` (默认值:`None`)     
  数据的会话结束时间指示。可能被一些 classes 在一些场景使用(比如: resampling)

## CSV Data Feeds 常用参数
参数(除常见参数外):

* `headers` (默认值:`True`)  
  表示所传递的数据是否具有初始化的 headers 行

* `separator` (默认:",")  
  分隔符是要考虑到标记每个CSV行

## GenericCSVData
此类公开了一个通用接口，该接口几乎可以解析所有CSV文件格式。

根据参数定义的顺序和字段存在情况解析CSV文件

具体参数(或具体含义):

* `dataname`    
  要解析的文件名或类似文件的对象

* `datetime` (默认值:0)  
  包含`date`(或`datetime`)字段的列

* `time` (默认值:-1)     
  包含`time`字段(如果与`datetime`字段分开的列)(-1表示不存在)

* `open`(默认:1)，`high`(默认:2)，`low`(默认:3)， `close`(默认:4)，`volume`(默认:5)，`openinterest` (默认:6)  
  包含相应字段的列的索引, 如果传递负值(例如:-1)，则表明该字段不在CSV数据中

* `nullvalue` (默认值:float('NaN'))    
  如果缺少应有的值(CSV字段为空)将使用的值

* `dtformat` (默认值:%Y-%m-%d %H:%M:%S)     
  用于解析日期时间CSV字段的格式

* `tmformat` (默认值:%H:%M:%S)   
  如果`time`字段存在，则用于解析时间CSV字段的格式(默认不存在 `time` CSV字段)

满足以下要求的示例用法:

* 将输入限制为2000年
* HLOC 订单而不是 OHLC
* 缺少的值将替换为零(0.0)
* 提供每日条形图，datetime 仅是日期，格式为YYYY-MM-DD
* 没有`openinterest`列

代码如下:
```
import datetime
import backtrader as bt
import backtrader.feeds as btfeeds

...
...

data = btfeeds.GenericCSVData(
    dataname='mydata.csv',

    fromdate=datetime.datetime(2000, 1, 1),
    todate=datetime.datetime(2000, 12, 31),

    nullvalue=0.0,

    dtformat=('%Y-%m-%d'),

    datetime=0,
    high=1,
    low=2,
    open=3,
    close=4,
    volume=5,
    openinterest=-1
)

...
```
稍作修改的要求：

* 将输入限制为2000年
* HLOC订单而不是OHLC
* 缺少的值将替换为零（0.0）
* 提供日内柱线，带有单独的日期和时间列
    * 日期格式为YYYY-MM-DD
    * 时间的格式为HH.MM.SS（而不是通常的HH：MM：SS）
* 没有`openinterest`列

代码如下:
```
import datetime
import backtrader as bt
import backtrader.feeds as btfeed

...
...

data = btfeeds.GenericCSVData(
    dataname='mydata.csv',

    fromdate=datetime.datetime(2000, 1, 1),
    todate=datetime.datetime(2000, 12, 31),

    nullvalue=0.0,

    dtformat=('%Y-%m-%d'),
    tmformat=('%H.%M.%S'),

    datetime=0,
    time=1,
    high=2,
    low=3,
    open=4,
    close=5,
    volume=6,
    openinterest=-1
)
```
也可以通过子类使其永久化：
```
import datetime
import backtrader.feeds as btfeed

class MyHLOC(btfreeds.GenericCSVData):

  params = (
    ('fromdate', datetime.datetime(2000, 1, 1)),
    ('todate', datetime.datetime(2000, 12, 31)),
    ('nullvalue', 0.0),
    ('dtformat', ('%Y-%m-%d')),
    ('tmformat', ('%H.%M.%S')),

    ('datetime', 0),
    ('time', 1),
    ('high', 2),
    ('low', 3),
    ('open', 4),
    ('close', 5),
    ('volume', 6),
    ('openinterest', -1)
)
```

现在，只需提供以下内容即可重用该新类dataname：
```
data = btfeeds.MyHLOC(dataname='mydata.csv')
```

# [Data Feeds - Extending](./mkd02_Extending.md)
# [Data Feeds - Development - CSV](./mkd03_Development_csv.md)
# [Data Feeds - Development - General](./mkd04_Development_General.md)
# [Data Feeds - Mutiple Timeframes](./mkd05_Multiple_Timeframes.md)
# [Data Feeds - Resample](./mkd06_Resample.md)
# Data Feeds - Replay
# Data Feeds - Rollover
# Data Feeds - Filters 
# Data Feeds - Yahoo
# Data Feeds - Panda
# Data Feeds - Reference