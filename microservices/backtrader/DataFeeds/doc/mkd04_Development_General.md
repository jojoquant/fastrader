- [Data Feeds - Development - General](#data-feeds---development---general)

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

