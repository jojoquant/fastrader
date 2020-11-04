- [Analyzers - Reference](#analyzers---reference)
  - [AnnualReturn](#annualreturn)
  - [Calmar](#calmar)
  - [DrawDown](#drawdown)
  - [TimeDrawDown](#timedrawdown)
  - [GrossLeverage](#grossleverage)
  - [PositionsValue](#positionsvalue)
  - [PyFolio](#pyfolio)
  - [LogReturnsRolling](#logreturnsrolling)
  - [PeriodStats](#periodstats)
  - [Returns](#returns)
  - [SharpeRatio](#sharperatio)
  - [SharpeRatio_A](#sharperatio_a)
  - [SQN](#sqn)
  - [TimeReturn](#timereturn)
  - [TradeAnalyzer](#tradeanalyzer)
  - [Transactions](#transactions)
  - [VWR](#vwr)

-----------------------------------------------------------
# Analyzers - Reference

-----------------------------------------------------------
## AnnualReturn
```
class backtrader.analyzers.AnnualReturn()

  ...
  if cur_year not in self.ret:
      # finish calculating pending data
      annualret = (value_end / value_start) - 1.0
      self.rets.append(annualret)
      self.ret[cur_year] = annualret
```
这个 `analyzer` 计算 `AnnualReturns` 通过看一年的开始和结束

Params:
* (None)

Member Attributes:
* `rets`: 计算的年回报率的 list
* `ret`: 年回报率的 dict (key: year)

Member methods:
* `get_analysis`: 返回一个年回报率的字典 (key: year)

## Calmar
```
class backtrader.analyzers.Calmar()
```
Calmar比率(Calmar Ratio) 描述的是收益和最大回撤之间的关系。计算方式为年化收益率与历史最大回撤之间的比率。Calmar比率数值越大，基金的业绩表现越好。反之，基金的业绩表现越差。

这个 `analyzer` 计算 CalmarRatio timeframe, 这里的参数和底层数据不一样:
* `timeframe` (default: `None`)   
  * `None`: 系统中第1个data的 `timeframe` 将被使用 
  * `TimeFrame.NoTimeFrame`: 全部的数据集都没有时间限制

* `compression` (default: None)   
  * `None`: 系统中第1个data的 `compression` 将被使用
  * `integer`: 比如当使用 `TimeFrame.Minutes` 时, integer为60, 表示工作在小时 timeframe 上

* `None`

* `fund` (default: None) 
  * `None`: broker (fundmode - True/False) 的模式会被自动检测是否返回 total net asset value 或者 the fund value, 详细请查broker文档 set_fundmode 相关

Member methods:
* `get_analysis`: 返回一个 time period 为 key 的 OrderedDict, value 是 rolling Calmar ratio

Member Attributes::
* `calmar`: 最后计算出的 calmar ratio

## DrawDown
```
class backtrader.analyzers.DrawDown()
```
这个 `analyzer` 计算交易系统回撤情况, 比如回撤值和百分比, 最大回撤值和百分比, 回撤长度和最大回撤长度

Params:
* `fund` (default: `None`)  
  broker (fundmode - True/False) 的模式会被自动检测是否返回 total net asset value 或者 the fund value, 详细请查broker文档 set_fundmode 相关

Member methods:
* `get_analysis`: 返回一个包含回撤情况的字典, key如下
  * `drawdown` - drawdown value in 0.xx %
  * `moneydown` - drawdown value in monetary units
  * `len` - drawdown length
  * `max.drawdown` - max drawdown value in 0.xx %
  * `max.moneydown` - max drawdown value in monetary units
  * `max.len` - max drawdown length 

## TimeDrawDown
```
class backtrader.analyzers.TimeDrawDown()
```


## GrossLeverage
## PositionsValue
## PyFolio
## LogReturnsRolling
## PeriodStats
## Returns

## SharpeRatio
```
class backtrader.analyzers.SharpeRatio()
```
这个分析器使用无风险资产(即简单的利率)来计算策略的 SharpeRatio

Params:
* `timeframe`: (default: `TimeFrame.Years`)

* `compression` (default: 1)  
  如果想指定工作在1小时 timeframe 上, 指定上面 `timeframe=TimeFrame.Minutes`, `compression=60`

* `riskfreerate` (default: 0.01 -> 1%)  
  以年表示(见下面的 `convertrate`)

* `convertrate` (default: `True`)   
  将riskfreerate每年的费率转换成每月，每周或每天的费率。不支持 Sub-day 转化

* `factor` (default: `None`)  
  如果为 `None`， 则将从预定义表中选择无风险利率转换因子, 从 annual 到所选 timeframe 的

  > Days: 252, Weeks: 52, Months: 12, Years: 1

  否则将使用指定的值

* `annualize` (default: `False`)    
  如果 `convertrate` 是 `True`，则将以提供的 timeframe 处理 SharpeRatio。

  在大多数情况下，`SharpeRatio` 以年化形式提供。将 `riskfreerate` 每年的费率转换成每月，每周或每天的费率。不支持次日(Sub-day)转化

* `stddev_sample` (default: `False`)    
  如果设置为True, 标准差将被修正计算, 分母为 n-1。如果考虑到并非所有样本都用于计算，则在计算标准偏差时将使用此方法。这被称为贝塞尔修正

* `daysfactor` (default: `None`)     
  `factor` 的旧命名。如果设置为其他值, 同时timeframe是TimeFrame.Days的话, 将假设这是旧的代码和值会被使用

* `legacyannual` (default: `False`)   
  使用AnnualReturn收益分析器，顾名思义，它仅适用于年

* `fund` (default: `None`)  
  如果None将自动检测 broker 的实际模式（fundmode-True/False），以决定收益是基于总资产净值还是基于基金价值。请参阅 `set_fundmode` broker文件

## SharpeRatio_A
```
class backtrader.analyzers.SharpeRatio_A()
```
夏普比率的扩展，直接以年化形式返回夏普比率

与 SharpeRatio 相比, 下面这个参数不同
* `annualize` (default: `True`)

## SQN
```
class backtrader.analyzers.SQN()
```
SQN(System Quality Number)。由Van K.Tharp定义，用于对交易系统进行分类。

* 1.6-1.9低于平均水平
* 2.0-2.4平均值
* 2.5-2.9好
* 3.0-5.0很棒
* 5.1-6.9好极了
* 7.0-圣杯？

公式：  
```
SquareRoot(NumberTrades) * Average(TradesProfit) / StdDev(TradesProfit)
```

Member methods:
* `get_analysis`: 返回包含键 `sqn` 和 `trades` （考虑的交易数）的字典


## TimeReturn
## TradeAnalyzer
## Transactions
## VWR