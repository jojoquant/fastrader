- [Observers Reference](#observers-reference)
  - [Benchmark](#benchmark)
  - [Broker](#broker)
    - [Broker - Cash](#broker---cash)
    - [Broker - Value](#broker---value)
  - [BuySell](#buysell)
  - [DrawDown](#drawdown)
  - [TimeReturn](#timereturn)
  - [Trades](#trades)
  - [LogReturns](#logreturns)
  - [LogReturns2](#logreturns2)
  - [FundValue](#fundvalue)
  - [FundShares](#fundshares)

-------------------------------------------------------
# Observers Reference
## Benchmark
```
class backtrader.observers.Benchmark()
```
该观察者存储策略的 returns 和 asset return(传入系统的datas中的1个)

Params:
* `timeframe` (default: `None`)     
    如果为 None, 全部回测周期的完整 return 将被报告

* `compression` (default: `None`)   
    对于 sub-day timeframes 有用, 比如1个 hourly timeframe只要指定为 `TimeFrame.Minutes`, 同时 `compression=60`

* `data` (default: `None`)  
    跟踪比对的 asset
    > 该数据必须被 cerebro 通过 addata, resampledata or replaydata 添加先

* `_doprenext` (default: `False`)   
    Benchmarking 从策略开始才开始跟踪(比如: 当策略的最小period满足时)

    设置为True, benchmarking 值将从data feeds开始时算起

* `firstopen` (default: `False`)    
    设置为`False`, 第一次 value 和 benchmark 比对点从 0% 开始, 因此benchmark 不会使用开盘价

    详细解释, 参考 TimeReturn 分析器说明

* `fund` (default: `None`)
    如果为 `None`, `broker` 的模式(fundmode - True/False)将被自动检测, 然后决定 returns 是基于 全部净资产值 还是 基金值. 详细请参考broker的文档 set_fundmode

    Set it to True or False for a specific behavior

请记住，在运行的任何时刻，都可以通过在索引0处按名称查看 lines, 来检查当前值。

--------------------------------------------------------
## Broker
```
class backtrader.observers.Broker(*args, **kwargs)
```
观察者跟踪broker中当前 cash 数目 和 组合值

Params: None

--------------------------------------------------------
### Broker - Cash
```
class backtrader.observers.Cash(*args, **kwargs)
```
观察者跟踪broker中当前 cash 数目

--------------------------------------------------------
### Broker - Value
```
class backtrader.observers.Value(*args, **kwargs)
```
观察者跟踪broker中当前组合值(包含cash)

Params:

* `fund` (default: `None`)      
    如果为 `None`, `broker` 的模式(fundmode - True/False)将被自动检测, 然后决定 returns 是基于 全部净资产值 还是 基金值. 详细请参考broker的文档 set_fundmode

    Set it to True or False for a specific behavior

--------------------------------------------------------
## BuySell
```
class backtrader.observers.BuySell(*args, **kwargs)
```
观察者追踪每个 buy/sell orders, 将在图表上沿着执行价格附近数据绘制出来

Params:

* `barplot` (default: `False`)      
    在绘制buy信号在价格最小值下方, sell信号在价格最大值上方

    如果为 `False`, 绘制在执行期间的平均价格

* `bardist` (default: `0.015` 1.5%)     
    当`barplot`设置为True时, max/min 的距离

--------------------------------------------------------
## DrawDown
```
class backtrader.observers.DrawDown()
```
这个观察者跟踪当前的 drawdown 级别(绘制)和 maxdrawdown 级别(未绘制)

Params:

* `fund` (default: `None`)      
    如果为 `None`, `broker` 的模式(fundmode - True/False)将被自动检测, 然后决定 returns 是基于 全部净资产值 还是 基金值. 详细请参考broker的文档 set_fundmode

    Set it to True or False for a specific behavior


--------------------------------------------------------
## TimeReturn
```
class backtrader.observers.TimeReturn()
```
观察者存储的策略的收入returns

Params:

* `timeframe` (default: `None`)     
    如果为 None, 全部回测周期的完整 return 将被报告

* `compression` (default: `None`)   
    对于 sub-day timeframes 有用, 比如1个 hourly timeframe只要指定为 `TimeFrame.Minutes`, 同时 `compression=60`

* `fund` (default: `None`)           
    如果为 `None`, `broker` 的模式(fundmode - True/False)将被自动检测, 然后决定 returns 是基于 全部净资产值 还是 基金值. 详细请参考broker的文档 set_fundmode

    Set it to True or False for a specific behavior

请记住，在运行的任何时刻，都可以通过在索引0处按名称查看 lines, 来检查当前值。

--------------------------------------------------------
## Trades
```
class backtrader.observers.Trades()
```
该观察者跟踪全部trades, 当一个trade关闭时绘制 PnL 

当 position 从 0(或者穿过0) 变成 X 一个 trade 开始, 当 postion 回到0(或者反方向交叉过0), 该trade关闭

Params:
* `pnlcomm` (def: `True`)       
    显示 net profit and loss, 即算上手续费. 

    如果设置为`False`, 将显示没算手续费的 交易结果

--------------------------------------------------------
## LogReturns
```
class backtrader.observers.LogReturns()
```
该观察者存储策略的 log return

Params:

* `timeframe` (default: `None`)     
    如果为 None, 全部回测周期的完整 return 将被报告

* `compression` (default: `None`)   
    对于 sub-day timeframes 有用, 比如1个 hourly timeframe只要指定为 `TimeFrame.Minutes`, 同时 `compression=60`

* `fund` (default: `None`)           
    如果为 `None`, `broker` 的模式(fundmode - True/False)将被自动检测, 然后决定 returns 是基于 全部净资产值 还是 基金值. 详细请参考broker的文档 set_fundmode

    Set it to True or False for a specific behavior

请记住，在运行的任何时刻，都可以通过在索引0处按名称查看 lines, 来检查当前值。

--------------------------------------------------------
## LogReturns2
```
class backtrader.observers.LogReturns2()
```
扩展LogReturns 显示2个 instruments

--------------------------------------------------------
## FundValue
```
class backtrader.observers.FundValue(*args, **kwargs)
```
追踪当前 fund-like value

Params: None

--------------------------------------------------------
## FundShares
```
class backtrader.observers.FundShares(*args, **kwargs)
```
追踪当前 fund-like shares

Params: None