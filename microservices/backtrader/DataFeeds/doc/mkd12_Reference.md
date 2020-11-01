- [Data Feeds - Reference](#data-feeds---reference)
  - [AbstractDataBase](#abstractdatabase)
  - [BacktraderCSVData](#backtradercsvdata)
  - [CSVDataBase](#csvdatabase)
  - [Chainer](#chainer)
  - [DataClone](#dataclone)
  - [DataFiller (注意! 是填充, 不是过滤)](#datafiller-注意-是填充-不是过滤)
  - [DataFilter (是过滤! 不是填充)](#datafilter-是过滤-不是填充)
  - [GenericCSVData](#genericcsvdata)
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