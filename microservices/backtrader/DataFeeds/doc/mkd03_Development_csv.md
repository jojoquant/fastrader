- [Data Feeds - Development - CSV](#data-feeds---development---csv)
  - [注意事项](#注意事项)
-------------------------------------------
# Data Feeds - Development - CSV

`backtrader` 已经提供了通用 CSV data feed 和一些特定的CSV data Feeds, 包括：

* GenericCSVData
* VisualChartCSVData
* YahooFinanceData（用于在线下载）
* YahooFinanceCSVData（用于已下载的数据）
* BacktraderCSVData（内部…用于测试目的，但可以使用）

但是即使如此，最终用户还是希望为特定的 CSV data feed 提供支持。

通常的座右铭是：“说起来容易做起来难”。实际上，该结构旨在使其变得容易。

步骤:

* 继承自 `backtrader.CSVDataBase`
* 如果需要, 定义 `params` 
* 在 `start` 方法中进行初始化
* 在 `stop` 方法中进行清理
* 定义实际工作发生的 `_loadline` 方法

    此方法接收一个参数：`linetokens`

    顾名思义，它根据 `separator` 参数拆分了当前行之后的标记（从基类继承）

    如果在完成工作后有新数据……填写相应的行并返回 `True`

    如果没有可用的内容，因此解析结束：`return False`

    如果正在读取文件行的​​后台代码发现没有更多行可以解析，则甚至不需要返回 `False`。

已经考虑的事情：

* 打开文件（或接收类似文件的对象）
* 如果设置了 `headers` 参数，则跳过标题行
* 读取行
* 标记(Tokenizing)行
* 预加载支持（一次将整个 `data feed` 加载到内存中）

通常，一个例子值得一千个需求描述。让我们使用来自的内部定义的CSV解析代码的简化版本 `BacktraderCSVData`。这不需要初始化或清理（例如，可以打开一个套接字，然后再将其关闭）。
>backtrader数据供稿包含要填充的常规行业标准供稿。即：
>* datetime
>* open
>* high
>* low
>* close
>* volume
>* openinterest

如果您的策略/算法或简单的数据细读仅需要收盘价，您可以让其他价格保持不变（每次迭代都会在最终用户代码有机会做任何事情之前自动用float（'NaN'）值填充它们）。

在此示例中，仅支持每日格式：
```
import itertools
...
import backtrader as bt

class MyCSVData(bt.CSVDataBase):

    def start(self):
        # Nothing to do for this data feed type
        pass

    def stop(self):
        # Nothing to do for this data feed type
        pass

    def _loadline(self, linetokens):
        i = itertools.count(0)

        dttxt = linetokens[next(i)]
        # Format is YYYY-MM-DD
        y = int(dttxt[0:4])
        m = int(dttxt[5:7])
        d = int(dttxt[8:10])

        dt = datetime.datetime(y, m, d)
        dtnum = date2num(dt)

        self.lines.datetime[0] = dtnum
        self.lines.open[0] = float(linetokens[next(i)])
        self.lines.high[0] = float(linetokens[next(i)])
        self.lines.low[0] = float(linetokens[next(i)])
        self.lines.close[0] = float(linetokens[next(i)])
        self.lines.volume[0] = float(linetokens[next(i)])
        self.lines.openinterest[0] = float(linetokens[next(i)])

        return True
```

该代码期望所有字段都就位并且可以转换为浮点数，日期时间除外，该日期时间具有固定的 YYYY-MM-DD 格式，无需使用即可进行解析 `datetime.datetime.strptime`。

只需添加几行代码以说明空值和日期格式解析，就可以满足更复杂的需求。在 `GenericCSVData` 这样做的。

## 注意事项
使用 `GenericCSVData` 继承可以完成很多支持格式。

让我们添加对 `Sierra Chart` 的每日格式（始终以CSV格式存储）的支持。

定义(通过查看“ .dly”数据文件)：

* Fields：Date, Open, High, Low, Close, Volume, OpenInterest

    行业标准和已经支持的 GenericCSVData顺序相同（也是行业标准）

* Separator：,

* 日期格式：YYYY/MM/DD

这些文件的解析器：
```
class SierraChartCSVData(backtrader.feeds.GenericCSVData):

    params = (('dtformat', '%Y/%m/%d'),)
```
该 `params` 定义只是重新定义了基类中的现有参数之一。在这个例子中，只需更改日期的格式字符串即可。

就这样...Sierra Chart的解析器完成了。

`GenericCSVData` 的默认参数定义, 在此展示一下：
```
class GenericCSVData(feed.CSVDataBase):
    params = (
        ('nullvalue', float('NaN')),
        ('dtformat', '%Y-%m-%d %H:%M:%S'),
        ('tmformat', '%H:%M:%S'),

        ('datetime', 0),
        ('time', -1),
        ('open', 1),
        ('high', 2),
        ('low', 3),
        ('close', 4),
        ('volume', 5),
        ('openinterest', 6),
    )
```
