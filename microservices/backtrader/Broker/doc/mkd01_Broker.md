- [Broker - Reference](#broker---reference)
  - [backtrader.brokers.BackBroker()](#backtraderbrokersbackbroker)
    - [Params:](#params)
    - [Methods](#methods)
- [Broker - Slippage](#broker---slippage)
- [Broker - Cheat-On-Open](#broker---cheat-on-open)
- [Broker - Volume Filling - Fillers](#broker---volume-filling---fillers)
- [Position](#position)
- [Trade](#trade)


----------------------------------------------
# Broker - Reference

## backtrader.brokers.BackBroker()
```
class backtrader.brokers.BackBroker()
```
Broker 模拟器

该模拟器支持不同的订单(`order`)类型, 根据当前现金核对提交的订单现金需求, 跟踪每次 `cerebro` 迭代的现金和价值，并在不同的数据上保持当前 `position`

现金(`cash`)在每一次迭代中都会针对像期货等标的进行调整, 价格变化意味着在真正的经纪人中增加/减少现金

支持的定单类型:
* `Market`: 在下个bar的开盘价执行

* `Close`: 是指日内交易中，以最后一个bar的收盘价执行指令

* `Limit`: 如果在会话期间看到给定的限价，则执行

* `Stop`: 如果看到给定的止损价格，则执行市价单

* `StopLimit`: 如果看到给定的止损价格，则设置一个动态的限价指令

由于 `broker` 是由 `Cerebro` 实例化的，而且（大多数情况下）没有理由替换 broker，因此实例的用户不需要控制参数。要更改此设置，有两个选项:

1. 使用所需的参数手动创建此类的实例, 并使用 `cerebro.broker=instance` 将实例设置为运行执行的 broker
2. 使用 `set_xxx` 设置, `cerebro.broker.set_xxx`, 这里 `xxx` 代表要设置的参数名
> `cerebro.broker` 支持 `Cerebro` 的 `getbroker` 和 `setbroker` 方法

### Params:
* `cash` (default: 10000) 
    开始的现金

* `commission` (default: `CommInfoBase(percabs=True)`)      
    所有assets使用的基本commission 方案

* `checksubmit` (default: `True`)   
    在系统中接受订单之前检查保证金(margin)/现金(cash)

* `eosbar` (default: `False`)   
    对于日内 bars，将与会话结束时间相同的bar视为会话的结束。通常情况并非如此，因为有些bar（最终叫价auction）是由许多交易所在交易结束后的几分钟内为许多标的产生的

* `filler` (default: `None`)    
    一个可以调用的签名: `callable(order, price, ago)`

    * `order`: 显然是执行中的定单。这提供了对数据（以及ohlc和成交量）、执行类型、剩余size(`order.executed.remsize`)等等的访问, 请检查订单文档和参考，以获取订单(`Order`)实例中可用的内容

    * `price`: 订单在 `ago bar` 执行的价格

    * `ago`: 索引配合 `order.data` 使用, 提取ohlc和批量价格。在大多数情况下，这将是0，但在 `Close orders` 的情况下，这将是-1。为了获取bar的volume, 我们可以这么做: `volume = order.data.voluume[ago]`

    调用对象必须返回 执行size(一个 >=0 的值)

    带 `__call__` 的可调用对象是一个与前述签名匹配的对象

    默认 `None` 情况下，命令将在一次操作中完全执行

* `slip_perc` (default: 0.0)    
    绝对条件下的百分比（和正值），用于向上/向下滑点买入/卖出订单的价格
    > 0.01 = 1%
    >
    > 0.001 = 0.1%

* `slip_fixed` (default: 0.0)   
    单位百分比（正数），用于向上/向下滑动买入/卖出订单的价格
    > 注：如果 `slip_perc` 不为零，则它会优先于`slip_fixed`。

* `slip_open` (default: `False`)    
    是否为订单执行滑点价格，它将专门使用下一个 bar 的开盘价。一个例子是市价订单，它是用下一个可用的 tick 来执行的，即：bar的开盘价。

    这也适用于其他一些执行，因为当移动到一个新的 bar 时，逻辑将尝试检测开盘价格是否与请求的价格/执行类型匹配。

* `slip_match` (default: `True`)    
    如果为 `True` ，broker 将提供一个匹配的上下限，在高/低价格上，以防超过他们。

    如果为 `False`，broker 将不匹配订单与当前价格，并将在下一次迭代中尝试执行


* `slip_limit` (default: `True`)    
    即使 `slip_match` 为 `False`，也将匹配所请求的精确匹配价格的限价订单。

    此选项控制该行为:
    * 如果为 `True` ，则限价订单将通过 limit/high/low 价格来匹配

    * 如果为 `False` 同时滑点超过上限，那么将没有匹配

* `slip_out` (default: `False`)     
    即使价格跌到 (high - low) 范围之外，也要提供滑动。

* `coc` (default: `False`)    
    可以通过 `set_coc` 来设置 coc(Cheat-On-Close), 将市价指令与发出 order 的那个 bar 的收盘价相匹配。这实际上是欺骗，因为bar是已经收盘了，任何订单都应该首先与下一个bar的价格相匹配

* `coo` (default: `False`)  
    可以通过 `set_coo` 来设置 coo(Cheat-On-Open), 将“Market”订单与开盘价相匹配，例如使用“cheat”设置为“True”的计时器，因为这样的计时器在经纪人评估之前就被执行了

* `int2pnl` (default: `True`)   
    将产生的利息（如有）分配给减少头寸（无论是长期还是短期）的PnL。在某些情况下，这可能是不可取的，因为不同的策略是竞争的，利益将在不确定的基础上分配给其中任何一个。

* `shortcash` (default: `True`)     
    如果为 `True`，则当股票类资产被做空时，现金将增加，资产的计算值将为负值。

    如果为 `False`，则现金将作为运营成本扣除，计算值将为正，最终得到相同的金额

* `fundstartval` (default: 100.0)   
    此参数控制基金类方式衡量业绩的起始值，即：增加份额可以增加或减少现金。业绩不是用 `porftoflio` 的资产净值来衡量的，而是用基金的价值来衡量的

* `fundmode` (default: `False`)     
    如果设置为True，像 `TimeReturn` 这样的分析器可以根据基金价值而不是总资产净值自动计算收益

### Methods
* `set_cash(cash)`    
    设置现金 (alias: `setcash`)

* `get_cash()`    
    返回当前现金 (alias: `getcash`)

* `get_value(datas=None, mkt=False, lever=False)`   
    返回给定数据的资产组合值（如果 datas 为 `None` ，则返回组合的总值 (alias: getvalue)

* `set_eosbar(eosbar)`  
    设置参数 `eosbar` (alias: `seteosbar`)

* `set_checksubmit(checksubmit)`    
    设置 `checksubmit`

* `set_filler(filler)`    
    设置 volume filler

* `set_coc(coc)`    
    配置 `Cheat-On-Close` 方法来购买close On order bar

* `set_coo(coo)`    
    配置 `Cheat-On-Open` 方法 to buy the open on order bar

* `set_int2pnl(int2pnl)`    
    给 PnL 配置 interest

* `set_fundstartval(fundstartval)`  
    配置基金类绩效跟踪的起始值

* `set_slippage_perc(perc, slip_open=True, slip_limit=True, slip_match=True, slip_out=False)`   
    配置百分比滑点

* `set_slippage_fixed(fixed, slip_open=True, slip_limit=True, slip_match=True, slip_out=False)`     
    配置固定值滑点

* `get_orders_open(safe=False)`     
    返回一个iterable，其中的订单仍处于 open 状态(未执行或部分执行), 返回的订单不能使用, 如果需要修改, 设置参数`safe=True`

* `getcommissioninfo(data)`     
    检索给定data的 `CommissionInfo` 方案

* `setcommission(commission=0.0, margin=None, mult=1.0, commtype=None, percabs=True, stocklike=False, interest=0.0, interest_long=False, leverage=1.0, automargin=False, name=None)`    
    该方法为 broker 中的资产管理设置一个` CommissionInfo` 对象. 详细内容查阅 `CommInfoBase`

    如果 `name=None`, 无法找到其他commoninfo方案的资产的默认值

* `addcommissioninfo(comminfo, name=None)`      
    添加一个 `CommissionInfo` 对象作为默认值, 给所有 `name=None` 的 assets

* `getposition(data)`   
    返回给定数据的当前 position 状态(一个 Position 实例)

* `get_fundshares()`    
    返回基金类模式的当前份额数 number of shares

* `get_fundvalue()`     
    返回基金类份额值 share value

* `add_cash(cash)`  
    Add/Remove cash to the system (use a negative value to remove)

-------------------------------------------------------
# [Broker - Slippage](./mkd02_Slippage.md)
# [Broker - Cheat-On-Open](./mkd03_Cheat_On_Open.md)
# [Broker - Volume Filling - Fillers](./mkd04_Volume_Fillers.md)
# [Position](./mkd05_Position.md)
# [Trade](./mkd06_Trade.md)