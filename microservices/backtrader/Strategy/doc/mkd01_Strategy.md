- [Strategy](#strategy)
  - [How to Buy/Sell/Close](#how-to-buysellclose)
  - [Information Bits:](#information-bits)
  - [Member Attributes:](#member-attributes)
  - [Member Attributes (meant for statistics/observers/analyzers):](#member-attributes-meant-for-statisticsobserversanalyzers)
- [Strategy - Signals](#strategy---signals)
- [Strategy - Reference](#strategy---reference)

---------------------------------------------------------------
# Strategy
如果把 `Cerebro` 比作 `backtrader` 的心脏, 那么 `Strategy` 同样重要

策略通过方法展示其生命周期

> 策略在诞生时可以抛出 `StrategySkipError` 异常, 异常错误在 `backtrader.errors` 模块中  
> 这可以避免有错误的策略继续回测, 详见 `Exceptions`

1. 怀孕阶段: `__init__`     
    实例化期间显示调用: `indicators` 和 其他属性 将在这里被创建, 例如:
    ```
    def __init__(self):
        self.sma = btind.SimpleMovingAverage(period=15)
    ```

2. 出生阶段: `start`    
    cerebro 告知 strategy 开始启动, 存在一个默认的空方法

3. 孩童阶段: `prenext`  
    在怀孕阶段声明的 indicators 将限制 strategy 的成熟时间: 也被称为 `minimum period`. 上面 `__init__` 创建的 SimpleMovingAverage with a period=15.
    只要系统看到的 bars 小于 15, `prenext` 将被调用(默认的实现是没有任何操作的, 即空方法)

4. 成人阶段: `next`     
    一旦系统看到了15个bars, `SimpleMovingAverage` 有了足够大的buffer去生成数据值, strategy 此时足够成熟可以执行了.

    这里还有一个 `nextstart` 方法, 只被调用一次, 标记从 `prenext` 切换到 `next`. `nextstart` 的默认实现非常简单, 只是调用 `next` 而已

5. 繁殖阶段: None   
    如果有优化操作的话, 会多次使用不同的参数实例化策略

6. 终结阶段: `stop`     
    系统告知 strategy 重置, 默认是个空方法

大多数情况下常规用法如下:
```
class MyStrategy(bt.Strategy):

    def __init__(self):
        self.sma = btind.SimpleMovingAverage(period=15)

    def next(self):
        if self.sma > self.data.close:
            # Do something
            pass

        elif self.sma < self.data.close:
            # Do something else
            pass
```
* `__init__` 阶段给 `indicator` 分配一个 属性
* 此处空方法 `start` 没有重写
* `prenext` 和 `nextstart` 也没有重写
* 在 `next` 方法中, `indicator` 与 收盘价比较然后做些操作
* 默认的空方法 `stop` 没有重写

Strateges 就像真实世界中的交易员, 当事件发生的时候会获得通知. 每次 next 过程, 策略都将有如下操作:
* 通过 `notify_order(order)` 收到 `order` 的任何状态变化通知;
* 通过 `notify_trade(trade)` 收到 `opening/updating/closing` 的交易信息;
* 通过 `notify_cashvalue(cash, value)` 收到当前 `broker` 的 `cash` 和 `portfolio` 信息;
* 通过 `notify_fund(cash, value, fundvalue, shares)` 收到当前 `broker` 的 `cash` , `portfolio`, `fundvalue` 和 `shares` 信息;
* 通过 `notify_store(msg, *args, **kwargs)` 收到 `Events` (单独实现的)  
    看下 `Cerebro` 关于 `store notification` 这部分的说明, 这些信息将被传递到 `strategy` 中, 即使他们开始是被传给 `cerebro` 实例的(通过重写 `notify_store` 或者 使用 `callback` )

`Strategies` 也像交易员一样, 为了盈利, 在市场中有机会执行操作:
* buy 方法可以 long or reduce/close a short position
* sell 方法可以 short or reduce/close a long position
* close 方法可以显示地平掉现有的仓位
* cancel 方法可以取消还没执行的 order

## How to Buy/Sell/Close
`Buy` 和 `Sell` 方法产生 `orders`, 当调用他们时, 会返回一个 `Order`(或者 子类)的实例作为引用. 这个 `order` 有一个唯一的 `ref` 标识, 可以用来比对

> 专有的 broker 实现的 Order的子类 可能带有 broker 提供的额外的唯一的身份标识

创建order可以使用以下这些参数:
* `data` (default: `None`)  
    指定创建的 order 属于哪个 data, 如果为 None, 则将使用系统的第1个data, 即self.datas[0] or self.data0 (aka self.data) 

* `size` (default: `None`)  
    订单使用的数据单位的 `size` (正)。

    如果为 `None`，那么通过 `getsizer` 获取的 `sizer` 实例将用于确定 size。

* `price` (default: `None`)     
    使用的价格（如果实际格式不符合 `minimum tick size` 要求，实时 broker 可能会对输入格式进行限制）

    对 Market市价 和 Close 关闭订单指令无效(市场决定价格)
    
    对 `Limit`, `Stop` 和 `StopLimit` 订单，这个值决定了触发点(在Limit的情况下，触发点显然是该指令应该匹配的价格)。

* `plimit` (default: `None`)    
    仅适用于 `StopLimit` 订单。一旦止损被触发，这就是设定隐含的限价指令的价格（已使用的价格）

* `exectype` (default: `None`)  
可选值:
    * `Order.Market` or `None`   
    市价单将在下一个合适的价格被执行, 在回测中, 将是下个 bar 的 open 价

    * `Order.Limit`   
    限价单, 不解释

    * `Order.Stop`   
    指定价格执行, 类似市价单 `Order.Market` order

    * `Order.StopLimit`   
    指定价格触发, 执行隐含的 `Limit order`, 价格由 `pricelimit` 给出

* `valid` (default: `None`) 
可选值:
    * `None`:    
    这将生成一个不会过期的订单(也就是在取消之前的好订单)，并且在匹配或取消之前保持在市场中。在现实中，brokers 往往会设定一个时间限制，但这通常是如此遥远，以至于认为它不会到期

    * `datetime.datetime` or `datetime.date` instance:   
    该日期将用于生成在给定日期之前有效的订单(也称为良好日期）
    
    * `Order.DAY` or `0` or `timedelta()`:  
    生成会话结束前的有效日期(又名 day order)
    a day valid until the End of the Session (aka day order) will be generated

    * `numeric value`:      
    假设该值对应 `matplotlib` 编码中的 datetime (backtrader中使用的)，并将用于生成在该日期之前有效的订单(最佳日期)

* `tradeid` (default: 0)    
    这是 `backtrader` 应用的一个内部值，用于跟踪同一资产上的重叠交易。当通知订单状态的更新时，这个 `tradeid` 被发送回策略。

* `**kwargs`:    
    其他 `broker` 实现, 可能支持额外的参数。backtrader将把 kwargs 传递到创建的 `order` 对象

    示例：如果 `backtrader` 直接支持的4种订单执行类型还不够，在 `IB` 的例子中，可以将以下内容作为 kwargs 传递：
    ```
    orderType='LIT', lmtPrice=10.0, auxPrice=9.8
    ```
    这将覆盖backtrader创建的设置，并生成一个触发(toched)价格为9.8、限价为10.0的限价单。

## Information Bits:
策略的长度总是等于主数据的长度(datas[0])，当然可以通过len(self)得到

如果正在 `replayed` 数据或传递 live feed，并且同一时间点（长度）的新 ticks 到达，调用 `next`, 数据长度没有发生变化

## Member Attributes:
* `env`: Strategy 归属的 cerebro

* `datas`: 传递给 cerebro 的 data feeds 数组

    * `data/data0` is an alias for datas[0]

    * `dataX` is an alias for datas[X]

    如果已经分配了一个data feeds，也可以按名称访问该 data feeds（请参阅参考资料）

* `dnames`: 按名称(使用[name]或.name符号)访问 data feeds 的另一种方法

    例如，如果重新采样数据像这样:
    ```
    ...
    data0 = bt.feeds.YahooFinanceData(datname='YHOO', fromdate=..., name='days')
    cerebro.adddata(data0)
    cerebro.resampledata(data0, timeframe=bt.TimeFrame.Weeks, name='weeks')
    ...
    ```
    之后在这个策略里，你可以在每一个上面创建这样的指标:
    ```
    ...
    smadays = bt.ind.SMA(self.dnames.days, period=30)  # or self.dnames['days']
    smaweeks = bt.ind.SMA(self.dnames.weeks, period=10)  # or self.dnames['weeks']
    ...
    ```

* `broker`: 与此策略关联的代理的引用(来自`cerebro`)

* `stats`: list/named tuple-like 序列, 里面包含 `cerebro`  为该策略创建的观察者 `Observers`

* `analyzers`: list/named tuple-like 序列, 里面包含 `cerebro`  为该策略创建的 `Analyzers`

* `position`: 实际上是一个为data0提供当前位置的属性。检索所有 positions 的方法(请参阅参考资料)

## Member Attributes (meant for statistics/observers/analyzers):
`_orderspending`: 在调用 `next` 之前通知策略的订单列表

`_tradespending`: 在调用 `next` 之前将被通知给策略的交易列表

`_orders`: 已被通知的订单列表。一个 order 可以在列表中多次出现，具有不同的状态和不同的执行 bits。这个名单是用来保存历史记录的。

`_trades`: 已经被通知的 trade 列表。一个 trade 可以在列表中多次出现，就像一个order。

> 请记住，`prenext`、`nextstart`和 `next` 可以在同一时间点被多次调用(当使用daily timeframe时，ticks 更新 daily bar 的价格)

----------------------------------------------------------------
# [Strategy - Signals](./mkd02_Signals.md)
# [Strategy - Reference](./mkd03_Reference.md)