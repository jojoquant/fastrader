- [Data Feeds - Reference](#data-feeds---reference)
  - [AbstractDataBase](#abstractdatabase)
  - [BacktraderCSVData](#backtradercsvdata)
  - [CSVDataBase](#csvdatabase)
  - [Chainer](#chainer)
  - [DataClone](#dataclone)
  - [DataFiller (注意! 是填充, 不是过滤)](#datafiller-注意-是填充-不是过滤)
  - [DataFilter (是过滤! 不是填充)](#datafilter-是过滤-不是填充)
  - [GenericCSVData](#genericcsvdata)
  - [IBData](#ibdata)
  - [InfluxDB](#influxdb)
  - [MT4CSVData](#mt4csvdata)
  - [OandaData](#oandadata)
  - [PandasData](#pandasdata)
  - [PandasDirectData](#pandasdirectdata)
  - [Quandl](#quandl)
  - [QuandlCSV](#quandlcsv)
  - [RollOver](#rollover)
  - [SierraChartCSVData](#sierrachartcsvdata)
  - [VCData](#vcdata)
  - [VChartCSVData](#vchartcsvdata)
  - [VChartData](#vchartdata)
  - [VChartFile](#vchartfile)
  - [YahooFinanceCSVData](#yahoofinancecsvdata)
  - [YahooFinanceData](#yahoofinancedata)
  - [YahooLegacyCSV](#yahoolegacycsv)
------------------------------------------------
# Data Feeds - Reference
## AbstractDataBase
Lines:
```
* close
* low
* high
* open
* volume
* openinterest
* datetime
```
Params:
```
* dataname (None)
* name ()
* compression (1)
* timeframe (5)
* fromdate (None)
* todate (None)
* sessionstart (None)
* sessionend (None)
* filters ([])
* tz (None)
* tzinput (None)
* qcheck (0.0)
* calendar (None)
```

## BacktraderCSVData
解析自定义的用于测试的csv数据
* `dataname`: 待解析文件名或者文件对象

Lines:
```
* close
* low
* high
* open
* volume
* openinterest
* datetime
```
Params:
```
* dataname (None)
* name ()
* compression (1)
* timeframe (5)
* fromdate (None)
* todate (None)
* sessionstart (None)
* sessionend (None)
* filters ([])
* tz (None)
* tzinput (None)
* qcheck (0.0)
* calendar (None)
------------------
* headers (True)
* separator (,)
```

## CSVDataBase
实现 CSV datafeeds 的基类, 该类负责打开文件，读取行并标记它们。

子类只需要重写：
* _loadline(tokens)     
`_loadline` 的返回值（True/False）是 重写基类 `_load` 的返回值

Lines:
```
* close
* low
* high
* open
* volume
* openinterest
* datetime
```
Params:
```
* dataname (None)
* name ()
* compression (1)
* timeframe (5)
* fromdate (None)
* todate (None)
* sessionstart (None)
* sessionend (None)
* filters ([])
* tz (None)
* tzinput (None)
* qcheck (0.0)
* calendar (None)
------------------
* headers (True)
* separator (,)
```

## Chainer
chains datas 的类

Lines:
```
* close
* low
* high
* open
* volume
* openinterest
* datetime
```
Params:
```
* dataname (None)
* name ()
* compression (1)
* timeframe (5)
* fromdate (None)
* todate (None)
* sessionstart (None)
* sessionend (None)
* filters ([])
* tz (None)
* tzinput (None)
* qcheck (0.0)
* calendar (None)
```

## DataClone
Lines:
```
* close
* low
* high
* open
* volume
* openinterest
* datetime
```
Params:
```
* dataname (None)
* name ()
* compression (1)
* timeframe (5)
* fromdate (None)
* todate (None)
* sessionstart (None)
* sessionend (None)
* filters ([])
* tz (None)
* tzinput (None)
* qcheck (0.0)
* calendar (None)
```

## DataFiller (注意! 是填充, 不是过滤)
此类将使用自 底层数据源 的以下信息位来填补 源数据 中的空白

* `timeframe` 和 `compression` 以确定输出 bars 的维度

* `sessionstart` 和 `sessionend`

如果 data Feed 在 10:31 和 10:34 之间缺少 bars，并且 timeframe 是分钟，则输出将使用最后一个bar（10:31的收盘价）在分钟10:32和10:33中填充条形图。 

Params:
```
* dataname (None)
* name ()
* compression (1)
* timeframe (5)
* fromdate (None)
* todate (None)
* sessionstart (None)
* sessionend (None)
* filters ([])
* tz (None)
* tzinput (None)
* qcheck (0.0)
* calendar (None)
-----------------------------------------------
* fill_price (None): 
    如果为None（或被判断为False），将使用收盘价，否则使用传递的值（例如，可以是'NaN'，但在评估中缺少条形，但存在就时间而言

* fill_vol (nan): 用于填充丢失的 volume
* fill_oi (nan): 用于填充丢失的 openinterest
```

## DataFilter (是过滤! 不是填充)
此类过滤给定数据源中的 bars。除了数据库的标准参数外，它还包含一个可以调用的参数 `funcfilter` 

逻辑：

* funcfilter 将与基础数据源一起调用
    * 返回值True：将使用当前数据源 bar values
    * 返回值False：当前数据源 bar values 将被丢弃

Lines:
```
* close
* low
* high
* open
* volume
* openinterest
* datetime
```
Params:
```
* dataname (None)
* name ()
* compression (1)
* timeframe (5)
* fromdate (None)
* todate (None)
* sessionstart (None)
* sessionend (None)
* filters ([])
* tz (None)
* tzinput (None)
* qcheck (0.0)
* calendar (None)
* funcfilter (None)
```

## GenericCSVData
根据参数定义的顺序和字段存在情况解析CSV文件

具体参数（或具体含义）：

* `dataname`：要解析的文件名或类似文件的对象

* 行参数（datetime，open，high…）采用数值型表示

    值-1表示CSV源中不存在该字段

* 如果 `time` 存在（参数 `time` >= 0），则源要是包含日期和时间的单独两个字段，这些字段将合并

* `nullvalue`

    如果缺少应有的值（CSV字段为空）将使用的值

* `dtformat`：用于解析CSV字段 datetime 的格式。有关格式，请参见 python `strptime`/`strftime` 文档。

    如果指定了数值，则其解释如下

    * `1`：该值是类型为Unix的时间戳，`int` 表示自1970年1月1日以来的秒数

    * `2`：值是Unix时间戳类型 `float`

    如果一个 callable 对象被传入

    * 它将接受一个字符串并返回一个 `datetime.datetime` python实例

* `tmformat`：如果“存在”，则用于解析CSV time字段的格式（“time” CSV字段的默认值是不存在）

Lines:
```
* close
* low
* high
* open
* volume
* openinterest
* datetime
```
Params:
```
* dataname (None)
* name ()
* compression (1)
* timeframe (5)
* fromdate (None)
* todate (None)
* sessionstart (None)
* sessionend (None)
* filters ([])
* tz (None)
* tzinput (None)
* qcheck (0.0)
* calendar (None)
-----------------------------------------
* headers (True)
* separator (,)
-----------------------------------------
* nullvalue (nan)
* dtformat (%Y-%m-%d %H:%M:%S)
* tmformat (%H:%M:%S)
-----------------------------------------
* datetime (0)
* time (-1)
* open (1)
* high (2)
* low (3)
* close (4)
* volume (5)
* openinterest (6)
```

## IBData
Interactive Brokers Data Feed.

参数 `dataname` 支持指定以下合约
```
TICKER # Stock type and SMART exchange

TICKER-STK # Stock and SMART exchange

TICKER-STK-EXCHANGE # Stock

TICKER-STK-EXCHANGE-CURRENCY # Stock

TICKER-CFD # CFD and SMART exchange

TICKER-CFD-EXCHANGE # CFD

TICKER-CDF-EXCHANGE-CURRENCY # Stock

TICKER-IND-EXCHANGE # Index

TICKER-IND-EXCHANGE-CURRENCY # Index

TICKER-YYYYMM-EXCHANGE # Future

TICKER-YYYYMM-EXCHANGE-CURRENCY # Future

TICKER-YYYYMM-EXCHANGE-CURRENCY-MULT # Future

TICKER-FUT-EXCHANGE-CURRENCY-YYYYMM-MULT # Future

TICKER-YYYYMM-EXCHANGE-CURRENCY-STRIKE-RIGHT # FOP

TICKER-YYYYMM-EXCHANGE-CURRENCY-STRIKE-RIGHT-MULT # FOP

TICKER-FOP-EXCHANGE-CURRENCY-YYYYMM-STRIKE-RIGHT # FOP

TICKER-FOP-EXCHANGE-CURRENCY-YYYYMM-STRIKE-RIGHT-MULT # FOP

CUR1.CUR2-CASH-IDEALPRO # Forex

TICKER-YYYYMMDD-EXCHANGE-CURRENCY-STRIKE-RIGHT # OPT

TICKER-YYYYMMDD-EXCHANGE-CURRENCY-STRIKE-RIGHT-MULT # OPT

TICKER-OPT-EXCHANGE-CURRENCY-YYYYMMDD-STRIKE-RIGHT # OPT

TICKER-OPT-EXCHANGE-CURRENCY-YYYYMMDD-STRIKE-RIGHT-MULT # OPT
```

Params:

* `sectype` (default: `STK`)

    如果 `dataname` specification 中未提供，则默认值用证券类型(security type)

* `exchange` (default: `SMART`)

    如果 `dataname` specification 中未提供，则用默认值作为交易所

* `currency` (default: '')

    如果 `dataname` specification 中未提供，则用默认值作为 currency

* `historical` (default: `False`)

    如果设置为 `True`, 则 data Feed 将在首次下载数据后停止。

    标准 data feed 参数 `fromdate` 和 `todate` 将被用作参考。

    如果请求的时间大于IB允许的数据 `timeframe/compression` 时间，则 data feed 将发出多个请求。

* `what` (default: `None`)

    如果将不同资产类型的默认值 `None` 用于历史数据请求：

    现金资产用 `BID`

    其他用 `TRADES`

    检查IB API文档是否需要其他值

* `rtbar` (default: `False`)

    如果True, 使用盈透证券提供的 5 Seconds Realtime bars 作为最小tick。根据文档，它们对应于实时值（由IB整理和策划）

    如果False，将使用 `RTVolume` 价格，该价格基于接收的 ticks。对于CASH资产（例如EUR.JPY），将始终使用 RTVolume 价格, 其bid价格（根据互联网上散布的文献，使用IB的行业实际标准）

    即使设置为True，如果数据重采样/保留到 Seconds/5 以下的 timeframe/compression，将不会使用实时bars，因为IB不会在该水平以下提供数据

* `qcheck` (default: 0.5)

    如果未接收到数据，则以秒为单位的唤醒时间，以便有机会正确地 resample/replay 数据包并在链上传递通知

* `backfill_start` (default: `True`)

    在 start 阶段执行 backfilling。最大的历史数据将在单个请求中获取。

* `backfill` (default: `True`)

    在断开/重新连接周期后执行 backfill 。间隔持续时间将用于下载尽可能少的数据

* `backfill_from` (default: `None`)

    可以传递一个另外的数据源来进行回填的初始化层。数据源耗尽后，如果发出数据请求，将从IB进行回填。理想情况下，这意味着从已经存储的源（例如磁盘上的文件）回填，但不限于此。

* `latethrough` (default: `False`)

    如果对数据源进行了重采样/回放，则对于已进行重新采样/回放的bar可能会出现一些 tick 太迟 late。如果是 `True` 这样的话，那么在任何情况下，这些 tick 都 late。

    查看 `Resampler` 文档，以了解谁该考虑了这些 ticks。

    尤其是如果在实例中将 timeoffset 设置为False，IBStore实例 和 TWS服务器时间与本地计算机的时间不同步，则可能会发生这种情况

* `tradename` (default: `None`)     
    `None` 在某些特定情况下很有用，例如CFD，一种资产提供价格，而在不同的网上进行交易
    * SPY-STK-SMART-USD-> SP500 ETF（将指定为dataname）
    * SPY-CFD-SMART-USD->是对应的CFD，不仅提供价格跟踪，还在这种情况下将作为交易资产（指定为tradename）

参数中的默认值是允许应用的, 像 TICKER , sectype 参数 (default:STK ), 还有 exchange (default:SMART`) 之类的东西。

某些资产, 比如 `AAPL` 需要完整的规范 specification，包括 `currency` （默认值：''），而其他资产 `TWTR` 则可以直接传递。

* AAPL-STK-SMART-USD 是 `dataname` 的完整规范

    Or else: `IBData` as `IBData(dataname='AAPL', currency='USD')` 使用默认值（`STK`和 `SMART`）并将货币覆盖为 `USD`

Lines:
```
* close
* low
* high
* open
* volume
* openinterest
* datetime
```
Params:
```
* dataname (None)
* name ()
* compression (1)
* timeframe (5)
* fromdate (None)
* todate (None)
* sessionstart (None)
* sessionend (None)
* filters ([])
* tz (None)
* tzinput (None)
* qcheck (0.5)    # 这里有点不一样
* calendar (None)
-----------------------------------------
-----------------------------------------
-----------------------------------------
------------------------------------------
* sectype (STK)
* exchange (SMART)
* currency ()
* rtbar (False)
* historical (False)
* what (None)
* useRTH (False)
* backfill_start (True)
* backfill (True)
* backfill_from (None)
* latethrough (False)
* tradename (None)
```

## InfluxDB
Lines:
```
* close
* low
* high
* open
* volume
* openinterest
* datetime
```
Params:
```
* dataname (None)
* name ()
* compression (1)
* timeframe (5)
* fromdate (None)
* todate (None)
* sessionstart (None)
* sessionend (None)
* filters ([])
* tz (None)
* tzinput (None)
* qcheck (0.0)
* calendar (None)
-----------------------------------------
* host (127.0.0.1)
* port (8086)
* username (None)
* password (None)
* database (None)
* startdate (None)
-----------------------------------------
-----------------------------------------
-----------------------------------------
* high (high_p)
* low (low_p)
* open (open_p)
* close (close_p)
* volume (volume)
* ointerest (oi)
```

## MT4CSVData
解析 `Metatrader4` 历史记录中心 CSV 导出文件。

具体参数（或具体含义）：

* `dataname`：要解析的文件名或类似文件的对象

* 使用 `GenericCSVData` 并简单地修改参数

Lines:
```
* close
* low
* high
* open
* volume
* openinterest
* datetime
```
Params:
```
* dataname (None)
* name ()
* compression (1)
* timeframe (5)
* fromdate (None)
* todate (None)
* sessionstart (None)
* sessionend (None)
* filters ([])
* tz (None)
* tzinput (None)
* qcheck (0.0)
* calendar (None)
-----------------------------------------
* headers (True)
* separator (,)
-----------------------------------------
* nullvalue (nan)
* dtformat (%Y.%m.%d)  # 这里不一样
* tmformat (%H:%M)    # 这里不一样
-----------------------------------------
* datetime (0)
* time (1)   # 往后都不一样
* open (2)
* high (3)
* low (4)
* close (5)
* volume (6)
* openinterest (-1)
```

## OandaData
## PandasData
使用Pandas DataFrame作为提要源，并使用列名的索引（可以是“数字”）

这意味着与行相关的所有参数都必须具有数值作为元组的索引

Params:

* `nocase` (default `True`) 不区分大小写的列名称匹配

Note:

* 该 `dataname` 参数是 Pandas DataFrame

* `datetime` 可能的值:
    * `None`: 索引包含 datetime
    * `-1`: 无索引，自动检测列
    * `0/string`: 指定列标识

* 对于其他行参数
    * `None`: column 不呈现
    * `-1`: 自动检测
    * `0/string`: 特定列标识

Lines:
```
* close
* low
* high
* open
* volume
* openinterest
* datetime
```

Params:
```
* dataname (None)
* name ()
* compression (1)
* timeframe (5)
* fromdate (None)
* todate (None)
* sessionstart (None)
* sessionend (None)
* filters ([])
* tz (None)
* tzinput (None)
* qcheck (0.0)
* calendar (None)
------------------------------
* nocase (True)
------------------------------
* datetime (None)
* open (-1)
* high (-1)
* low (-1)
* close (-1)
* volume (-1)
* openinterest (-1)
```

## PandasDirectData
使用Pandas DataFrame作为 feed 源，直接在 itertuples 返回的元组上进行迭代。

这意味着与 lines 相关的所有参数都必须具有数值作为元组的索引

Note:
* 该 `dataname` 参数是 Pandas DataFrame
* 数据行的任何参数中的负值表示它在 DataFrame 中不存在

Lines:
```
* close
* low
* high
* open
* volume
* openinterest
* datetime
```

Params:
```
* dataname (None)
* name ()
* compression (1)
* timeframe (5)
* fromdate (None)
* todate (None)
* sessionstart (None)
* sessionend (None)
* filters ([])
* tz (None)
* tzinput (None)
* qcheck (0.0)
* calendar (None)
------------------------------------
* datetime (0)
* open (1)
* high (2)
* low (3)
* close (4)
* volume (5)
* openinterest (6)
```

## Quandl
## QuandlCSV
## RollOver
## SierraChartCSVData
## VCData
## VChartCSVData
## VChartData
## VChartFile
## YahooFinanceCSVData
## YahooFinanceData
## YahooLegacyCSV