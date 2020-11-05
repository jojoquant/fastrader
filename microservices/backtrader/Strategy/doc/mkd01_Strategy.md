- [Strategy](#strategy)
  - [How to Buy/Sell/Close](#how-to-buysellclose)
  - [Information Bits:](#information-bits)
  - [Member Attributes:](#member-attributes)
  - [Member Attributes (meant for statistics/observers/analyzers):](#member-attributes-meant-for-statisticsobserversanalyzers)
  - [Reference: Strategy](#reference-strategy)
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

Size to use (positive) of units of data to use for the order.

If None the sizer instance retrieved via getsizer will be used to determine the size.

* `price` (default: `None`)

Price to use (live brokers may place restrictions on the actual format if it does not comply to minimum tick size requirements)

None is valid for Market and Close orders (the market determines the price)

For Limit, Stop and StopLimit orders this value determines the trigger point (in the case of Limit the trigger is obviously at which price the order should be matched)

* `plimit` (default: `None`)

Only applicable to StopLimit orders. This is the price at which to set the implicit Limit order, once the Stop has been triggered (for which price has been used)

* `exectype` (default: `None`)

Possible values:

Order.Market or None. A market order will be executed with the next available price. In backtesting it will be the opening price of the next bar

Order.Limit. An order which can only be executed at the given price or better

Order.Stop. An order which is triggered at price and executed like an Order.Market order

Order.StopLimit. An order which is triggered at price and executed as an implicit Limit order with price given by pricelimit

* `valid` (default: `None`)

Possible values:

None: this generates an order that will not expire (aka Good til cancel) and remain in the market until matched or canceled. In reality brokers tend to impose a temporal limit, but this is usually so far away in time to consider it as not expiring

datetime.datetime or datetime.date instance: the date will be used to generate an order valid until the given datetime (aka good til date)

Order.DAY or 0 or timedelta(): a day valid until the End of the Session (aka day order) will be generated

numeric value: This is assumed to be a value corresponding to a datetime in matplotlib coding (the one used by backtrader) and will used to generate an order valid until that time (good til date)

* `tradeid` (default: 0)

This is an internal value applied by backtrader to keep track of overlapping trades on the same asset. This tradeid is sent back to the strategy when notifying changes to the status of the orders.

* `**kwargs`: additional broker implementations may support extra parameters. backtrader will pass the kwargs down to the created order objects

Example: if the 4 order execution types directly supported by backtrader are not enough, in the case of for example Interactive Brokers the following could be passed as kwargs:


orderType='LIT', lmtPrice=10.0, auxPrice=9.8
This would override the settings created by backtrader and generate a LIMIT IF TOUCHED order with a touched price of 9.8 and a limit price of 10.0.

## Information Bits:
## Member Attributes:
## Member Attributes (meant for statistics/observers/analyzers):
## Reference: Strategy


----------------------------------------------------------------
# [Strategy - Signals](./mkd02_Signals.md)
# [Strategy - Reference](./mkd03_Reference.md)