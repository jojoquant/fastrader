- [Reference](#reference)
  - [class backtrader.Cerebro()](#class-backtradercerebro)
  - [addstorecb(callback)](#addstorecbcallback)
  - [notify_store(msg, *args, **kwargs)](#notify_storemsg-args-kwargs)
  - [adddatacb(callback)](#adddatacbcallback)
  - [notify_data(data, status, *args, **kwargs)](#notify_datadata-status-args-kwargs)
  - [adddata(data, name=None)](#adddatadata-namenone)
  - [resampledata(dataname, name=None, **kwargs)](#resampledatadataname-namenone-kwargs)
  - [replaydata(dataname, name=None, **kwargs)](#replaydatadataname-namenone-kwargs)
  - [chaindata(*args, **kwargs)](#chaindataargs-kwargs)
  - [rolloverdata(*args, **kwargs)](#rolloverdataargs-kwargs)
  - [addstrategy(strategy, *args, **kwargs)](#addstrategystrategy-args-kwargs)
  - [optstrategy(strategy, *args, **kwargs)](#optstrategystrategy-args-kwargs)
  - [optcallback(cb)](#optcallbackcb)
  - [addindicator(indcls, *args, **kwargs)](#addindicatorindcls-args-kwargs)
  - [addobserver(obscls, *args, **kwargs)](#addobserverobscls-args-kwargs)
  - [addobservermulti(obscls, *args, **kwargs)](#addobservermultiobscls-args-kwargs)
  - [addanalyzer(ancls, *args, **kwargs)](#addanalyzerancls-args-kwargs)
  - [addwriter(wrtcls, *args, **kwargs)](#addwriterwrtcls-args-kwargs)
  - [run(**kwargs)](#runkwargs)
  - [runstop()](#runstop)
  - [setbroker(broker)](#setbrokerbroker)
  - [getbroker()](#getbroker)
  - [plot(plotter=None, numfigs=1, iplot=True, start=None, end=None, width=16, height=9, dpi=300, tight=True, use=None, **kwargs)](#plotplotternone-numfigs1-iplottrue-startnone-endnone-width16-height9-dpi300-tighttrue-usenone-kwargs)
  - [addsizer(sizercls, *args, **kwargs)](#addsizersizercls-args-kwargs)
  - [addsizer_byidx(idx, sizercls, *args, **kwargs)](#addsizer_byidxidx-sizercls-args-kwargs)
  - [add_signal(sigtype, sigcls, *sigargs, **sigkwargs)](#add_signalsigtype-sigcls-sigargs-sigkwargs)
  - [signal_concurrent(onoff)](#signal_concurrentonoff)
  - [signal_accumulate(onoff)](#signal_accumulateonoff)
  - [signal_strategy(stratcls, *args, **kwargs)](#signal_strategystratcls-args-kwargs)
  - [addcalendar(cal)](#addcalendarcal)
  - [addtz(tz)](#addtztz)
  - [add_timer(when, offset=datetime.timedelta(0), repeat=datetime.timedelta(0), weekdays=[], weekcarry=False, monthdays=[], monthcarry=True, allow=None, tzdata=None, strats=False, cheat=False, *args, **kwargs)](#add_timerwhen-offsetdatetimetimedelta0-repeatdatetimetimedelta0-weekdays-weekcarryfalse-monthdays-monthcarrytrue-allownone-tzdatanone-stratsfalse-cheatfalse-args-kwargs)
  - [notify_timer(timer, when, *args, **kwargs)](#notify_timertimer-when-args-kwargs)
  - [add_order_history(orders, notify=True)](#add_order_historyorders-notifytrue)
-----------------------------------------------------------
# Reference
## class backtrader.Cerebro()
Params:

* `preload` (default: `True`)   
    是否需要对 data feeds 进行预加载

* `runonce` (default: `True`)   
    通过矢量化模式运行 Indicators 来加速整个系统. Strategies 和 Observers 还是以事件驱动方式运行

* `live` (default: `False`)
    没有数据是 live 的(根据 `islive` 方法判断), 如果希望live模式, 该参数可以设置为 `True`. 这将同时禁用 `preload` 和`runonce`。对内存节省方案没有影响。

* `maxcpus` (default: `None` -> 使用所有 cores)     
    设置优化时用多少个cpu

* `stdstats` (default: `True`)      
    为True时, 将添加默认的 Observers: `Broker`(Cash and Value), `Trades` 和 `BuySell` 

* `oldbuysell` (default: `False`)   
    如果 `stdstats` 为 `True`, 自动添加 observers, 自动切换`BuySell` observer 的控制行为

    `False`: 使用目前的模式, 将buy/sell信号分别绘制在 low/high 价格上下, 避免过于集中显示

    `True`: 使用已经弃用的模式, 将buy/sell信号绘制在订单执行的平均价附近, 观察不方便

* `oldtrades` (default: `False`)    
    如果 `stdstats` 为 `True`, 自动添加 observers, 自动切换`Trades` observer 的控制行为

    `False`: 目前的模式, 所有数据的 trades 被绘制为不同的标记

    `True`: 旧版本模式, trades 都是一样的标记, 只有他们为正或负才能看出差别

* `exactbars` (default: `False`)    
    * `False` :  
    每一个 value 都存储在 line 中, 保留在内存中

    * `True` or `1`:    
    所有的 lines 对象缩减内存用量, 自动计算出最小周期.  
    如果一个简单移动平均周期为30, 底层数据将总是运行一个30根bars的buffer, 来计算这个简单移动平均
        * 该设置会使 `preload` 和 `runonce` 失效
        * 该设置也会使 `plotting` 失效

    * `-1`:     
    datafeeds 和 indicatiors/operations 在策略级将全部data保留在内存中.  
    比如: `RSI` 使用 `UpDay` 来计算, 子indicator将不会在内存中保留数据
        * 该设置会使 `plotting` 和 `preloading` active.
        * 使 `runonce` deactivated

    * `-2`:     
    data feeds 和 indicators 作为策略属性, 全部数据点保存在内存中.    
    比如: `RSI` 使用 `UpDay` 来计算, 子indicator将不会在内存中保留数据    
    如果在 `__init__` 方法中, 存在`a = self.data.close - self.data.high`, 那么 `a` 在内存中不会保留全部数据
        * This allows to keep `plotting` and `preloading` active.
        * `runonce` will be deactivated

* `objcache` (default: `False`)     
    实验性质的参数选项, 实现一个 lines 对象的 cache, 减小lines的数量, 从`UltimateOscillator` 来的例子:
    ```
    bp = self.data.close - TrueLow(self.data)
    tr = TrueRange(self.data)  # -> creates another TrueLow(self.data)
    ```
    如果为 `True` , 在 `TrueRange` 内的第二个 `TrueLow(self.data)` 匹配 bp 计算中的签名, 这里将复用

    可能会发生一些极端情况，在这种情况下，这会使 line 对象脱离最小周期而产生问题，因此将其禁用

* `writer` (default: `False`)   
    如果设置为 `True`, 会创建一个默认的 `WriterFile` 打印输出到标准输出 stdout.将被添加到策略中(除了用户自己添加的 writers 之外)

* `tradehistory` (default: `False`)     
    如果设置为 True, 将在策略中的每个 trade 中激活更新事件日志. 同样的功能也可以通过单独策略中的 `set_tradehistory` 实现

* `optdatas` (default: `True`)  
    如果设置为 True, optimizing系统进行 预加载 和使用 runonce, 数据只在主进程中被预加载一次, 节省时间和资源, 测试显示有接近20%的速度提升


* `optreturn` (default: `True`)     
    如果 `True` ，优化结果将不包括完整的策略对象(还有所有数据、指标、观察者……)，只有以下属性的对象(与策略相同):
    ```
    * `params` (or `p`) the strategy had for the execution
    * `analyzers` the strategy has executed
    ```
    在大多数情况下，只有 `Analyzers` 和参数是评估策略的表现所需要的东西。如果需要对(例如)指标所生成的值进行详细分析，请关闭此功能

    测试显示执行时间提高了13% - 15%。与 optdatas 结合，在一次优化运行中，32%的时间加速。

* `oldsync` (default: `False`)      
    从版本1.9.0.99开始，多个不同长度的数据(相同或不同的时间框架)的同步被更改为允许。

    如果希望使用 data0 作为系统的主干的旧操作，则将该参数设置为true

* `tz` (default: `None`)    
    为策略添加全球时区, tz可以是:
    ```
    * `None`: 在这种情况下，策略所显示的日期时间将使用UTC，这一直是标准行为

    * `pytz` 实例，它将用于将UTC时间转换为所选时区

    * `string`. 将尝试实例化一个`pytz`实例。

    * `integer`. 对于策略，使用 `data` 在 `self.datas` 对应的时区。(' 0 '将使用' data0 '的时区)
    ```

* `cheat_on_open` (default: `False`)    
    策略中的 `next_open` 方法将被调用。这发生在 `next` 之前，在 `broker` 评估订单之前。`Indicators` 尚未重新计算。这允许发布一个订单，该订单考虑了前一天的指标，但使用开盘价计算股份下单

    对于 `cheat_on_open` 的订单执行，还是需要进行调用的 `cerebro.broker.set_coo(True)`，或者 `BackBroker(coo=True)` 实例化一个 `broker` 通过参数设置，或者设置参数 `broker_coo` 为 `True`。`Cerebro` 会自动完成，除非下面这个参数禁用。

* `broker_coo` (default: `True`)    
    这将自动调用 `cerebro.broker.set_coo(True)` 来激活 `cheat_on_open` 执行。只有在 `cheat_on_open` 也为 `True` 时才会这样做

* `quicknotify` (default: `False`)      
    Broker 通知将在 next 价格交付之前送达。对于回溯测试，这没有任何影响，但是对于实时 broker 来说，通知可以在bar交付之前很久发生。当设置为True时，将尽快发送通知（请参阅livefeeds 中的 qcheck）

    为兼容性设置为False。可以将其设置为True
--------------------------------------------------------------------------------
## addstorecb(callback)
添加一个回调以获取由 `notify_store` 方法处理的消息

回调的签名必须支持以下内容：
* callback(msg, *args, **kwargs)

接收到的真实消息、*arg和**kwarg是可定义的实现（完全取决于 data/broker/store），但一般来说，人们应该希望它们是可打印的，以便接收和实验。

## notify_store(msg, *args, **kwargs)
在 `cerebro` 中接收 `store` 的消息

这个方法可以被 `Cerebro` 的子类覆盖修改

接收到的真实消息、*arg和**kwarg是可定义的实现（完全取决于 data/broker/store），但一般来说，人们应该希望它们是可打印的，以便接收和实验。

--------------------------------------------------------------------------------
## adddatacb(callback)
添加一个回调以获取将由 `notify_data` 方法处理的消息

回调的签名必须支持以下内容：
* callback(data, status, *args, **kwargs)

接收到的真实消息、*arg和**kwarg是可定义的实现（完全取决于 data/broker/store），但一般来说，人们应该希望它们是可打印的，以便接收和实验。

## notify_data(data, status, *args, **kwargs)
在 `cerebro` 中接收 `data` 的消息

这个方法可以被 `Cerebro` 的子类覆盖修改

接收到的真实消息、*arg和**kwarg是可定义的实现（完全取决于 data/broker/store），但一般来说，人们应该希望它们是可打印的，以便接收和实验。

---------------------------------------------------------------------------------
## adddata(data, name=None)
添加 data feed 的实例

如果 `name` 不是 `None` ，它将被放入 `data._name`，用于装饰/绘图目的。

## resampledata(dataname, name=None, **kwargs)
添加系统需要的 resample data feed

如果 `name` 不是 `None` ，它将被放入 `data._name` ，用于装饰/打印目的。

另外的一些 resample filter 支持的关键字参数，比如 `timeframe`, `compression`, `todate`，都能被传递。

## replaydata(dataname, name=None, **kwargs)
添加系统需要的 replay data feed

如果 `name` 不是 `None` ，它将被放入 `data._name` ，用于装饰/打印目的。

另外的一些 replay filter 支持的关键字参数，比如 `timeframe`, `compression`, `todate`，都能被传递

## chaindata(*args, **kwargs)
将多个数据源链接成一个

如果 `name` 不是 `None` ，它将被放入 `data._name` ，用于装饰/打印目的。

如果 `None`，则使用第一个数据的 name

## rolloverdata(*args, **kwargs)
将多个数据源链接到一个

如果 `name` 不是 `None` ，它将被放入 `data._name` ，用于装饰/打印目的。

如果 `None`，则使用第一个数据的 name

任何其他的关键字参数都会传递给 `RollOver` 类

----------------------------------------------------------------------------------
## addstrategy(strategy, *args, **kwargs)
将一个策略类添加到单次运行的组合中。实例化将在运行时发生。

args 和 kwargs 将在实例化期间传递给策略

返回 添加的其他对象（如sizer）的索引，第一次添加是1，第二次添加是2。

## optstrategy(strategy, *args, **kwargs)
将策略类添加到组合中以进行优化。实例化将在运行时发生。

args 和 kwargs 必须是可迭代的，它们保存要检查的值。

示例：如果策略接受参数 period，则为了优化目的，调用optstrategy如下所示：
```
cerebro.optstrategy(MyStrategy, period=(15, 25))
```
这将对值15和25执行优化。鉴于
```
cerebro.optstrategy(MyStrategy, period=range(15, 25))
```
将使用值 15,16,...,24 执行 MyStrategy（不包括25，因为在Python中范围是半开放的）

如果传递了一个参数，但不应进行优化，则调用如下所示：
```
cerebro.optstrategy(MyStrategy, period=(15,))
```
注意，period仍然作为一个iterable…传递，只有1个元素

不管怎样，backtrader都会尝试识别以下情况：
```
cerebro.optstrategy(MyStrategy, period=15)
```
将创建一个内部伪iterable

## optcallback(cb)      
将回调添加到回调列表中，当每个策略运行时，将使用优化调用该回调

函数签名如下:
* cb(strategy)

## addindicator(indcls, *args, **kwargs)
添加 Indicator class 。实例化将在运行时在传递的策略中完成

## addobserver(obscls, *args, **kwargs)
将 Observer class 添加到组合中。实例化将在运行时完成

## addobservermulti(obscls, *args, **kwargs)
将 Observer class 添加到混合中。实例化将在运行时完成

将在系统中每个 `data` 添加时添加一次。使用例子是 buy/sell observer 观察各自的数据。

一个反例是 `CashValue` ，他观察的是整个系统的值

## addanalyzer(ancls, *args, **kwargs)
添加一个分析器的类。在 cerebro 运行期间实例化

## addwriter(wrtcls, *args, **kwargs)
将Writer类添加到混合中。实例化将在运行时在 cerebro 中完成

---------------------------------------------------------------------------------
## run(**kwargs)
执行回溯测试的核心方法。传递给它的任何 `kwargs` 都会影响 `Cerebro` 实例化的标准参数的值。

如果 `Cerebro` 没有数据，该方法将立即退出。

它返回不同的值:
* 对于 `No Optimization`：一个包含添加了addstrategy 的策略类实例的 `list`
* 对于 `Optimization`：包含添加了addstrategy 的策略类实例的 `list of list`

## runstop()
如果从策略内部或任何其他地方调用，包括其他线程，执行将尽快停止。

## setbroker(broker)
为策略设置一个特定的 `broker` 实例，替换从 cerebro 继承的 broker。

## getbroker()
返回代理实例。

同样也可以获得属性名为 broker 的属性

----------------------------------------------------------------------------------
## plot(plotter=None, numfigs=1, iplot=True, start=None, end=None, width=16, height=9, dpi=300, tight=True, use=None, **kwargs)
绘制在 cerebro 内的策略

如果 `plotter` 为 `None`，则创建一个默认的 Plot 实例，并在实例化期间向其传递 kwargs。

`numfigs` 将图分成指定数量的图表，如果需要，可降低图表密度

`iplot`：如果为 `True` 并且在 `notebook` 中运行，则图表将以内联方式显示

`use`: 将其设置为所需的 `matplotlib` 后端名称。它将优先于 `iplot`

`start`：设置绘图的开始时间, 可以是策略的 datetime line 数组的 `index`, 也可以是 `datetime.datetime` 实例 

`end`：设置绘图的结束时间, 可以是策略的 datetime line 数组的 `index`, 也可以是 `datetime.datetime` 实例 

`width`：保存图形的宽度, 英寸为单位

`height`：以保存图形的高度, 英寸为单位

`dpi`：保存图形的每英寸点数质量

`tight`:只保存实际内容，不保存图形的帧

--------------------------------------------------------------------------------
## addsizer(sizercls, *args, **kwargs)
添加一个Sizer类(和args)，它是添加到cerebro的任何策略的默认Sizer

## addsizer_byidx(idx, sizercls, *args, **kwargs)
针对不同的策略设置不同的Sizer, 通过idx添加一个Sizer类。这个idx是一个与addstrategy返回的引用兼容的引用。只有idx引用的策略才会收到这个sizer

## add_signal(sigtype, sigcls, *sigargs, **sigkwargs)
向系统添加一个信号，该信号稍后将被添加到 `SignalStrategy` 中

## signal_concurrent(onoff)
如果将信号添加到系统中，并且将 concurrent 值设置为 True，则允许并发订单

## signal_accumulate(onoff)
如果信号被添加到系统中，并且 accumulate 值被设置为 True，进入市场信号发出时, 如果已经在市场中，将被允许增加一个头寸

## signal_strategy(stratcls, *args, **kwargs)
添加可以接受信号的 SignalStrategy 子类

## addcalendar(cal)
向系统添加一个全球交易日历。单个data feed可能具有覆盖全局日历的单独日历

`cal` 可以是 `TradingCalendar` 字符串的实例，也可以是 `pandas_market_calendar` 的实例。一个字符串将被实例化为一个 `PandasMarketCalendar` (它需要在系统中安装 `pandas_market_calendar` 模块)。

如果传递了 `TradingCalendarBase` 的子类(不是实例)，那么它将被实例化

## addtz(tz)
这也可以通过参数tz来实现, 为策略添加全局时区。tz可以是:
* `None`: 在这种情况下，策略显示的日期时间将以UTC表示，这一直是标准行为
* `pytz` 实例: 它将用于将UTC时间转换为所选时区
* `string`: 将尝试实例化pytz实例。
* `integer`: 对于策略，请使用相应数据相同的时区 `self.datas` iterable（0将使用数据0中的时区）

## add_timer(when, offset=datetime.timedelta(0), repeat=datetime.timedelta(0), weekdays=[], weekcarry=False, monthdays=[], monthcarry=True, allow=None, tzdata=None, strats=False, cheat=False, *args, **kwargs)
调度一个计时器来调用notify_timer

Parameters:
* `when`:
    * `datetime.time` instance (see below `tzdata`)
    * `bt.timer.SESSION_START` to reference a session start
    * `bt.timer.SESSION_END` to reference a session end

* `offset`: `datetime.timedelta` instance   
    补偿参数 `when` 的值, 与 `SESSION_START` 和 `SESSION_END` 联系起来使用, 可以类似定时器的功能, 比如在 `SESSION_START` 之后15 分钟被调用

* `repeat`: which must be a `datetime.timedelta` instance   
    指示在第一次调用后，是否将在同一会话中按 delta 计划 repeat 调用

    一旦计时器经过会话结束，它将重置为 `when` 值

* `weekdays`:   
    排序的整数迭代对象，指示可以实际调用 日计时器 的日期（iso码，星期一为1，星期日为7）

    如果未指定，则计时器将全天处于活动状态

* `weekcarry` (default: `False`)    
    如果为 True, 没有设置 weekdays(比如: trading holiday)，则计时器将在第二天（即使是在新的一周）执行

* `monthdays`:      
    排序的整数迭代对象，指示可以实际调用的 月计时器 的日期, 比如一般是15天/月

    如果未指定，则计时器将全天处于活动状态
* `monthcarry` (default: `True`)    
    如果没有遇到 weekend, trading holiday之类, 该timer将在下一个可行的天执行

* `allow` (default: `None`)     
    一个回调, 接收一个 `datetime.date` 实例, 如果这个`date`符合timer, 返回 `True`, 否则返回 `False`

* `tzdata` : None (default) / a pytz instance / a data feed instance

    * `None`: when is interpreted at face value (which translates to handling it as if it where UTC even if it’s not)

    * `pytz` instance: when will be interpreted as being specified in the local time specified by the timezone instance.

    * `data feed` instance: when will be interpreted as being specified in the local time specified by the tz parameter of the data feed instance.
    
    > 注意  
    > 如果 `when` 是 `SESSION_START` 或者 `SESSION_END` , 同时 tzdata=None, 系统的第一个 data feed(self.data0) 将被用作引用来查找 session times

* `strats` (default: `False`) call also the notify_timer of strategies

* `cheat` (default `False`) if True the timer will be called before the broker has a chance to evaluate the orders. This opens the chance to issue orders based on opening price for example right before the session starts

* `*args`: 传给 notify_timer 的其他参数

* `**kwargs`: 传给 notify_timer 的其他参数

Return Value:

* The created timer

## notify_timer(timer, when, *args, **kwargs)
接收一个计时器通知，其中timer是由add_timer返回的计时器，when是调用时间。args和kwargs是传递给add_timer的任何附加参数

实际 `when` 时间可以晚一点，但系统可能已经无法调用之前的计时器。这个值是定时器值，不是系统时间。

## add_order_history(orders, notify=True)
添加要在代理中直接执行的订单的历史记录以进行性能评估

* `orders`: 是一个迭代对象 (比如: list, tuple, iterator, generator) , 其中的元素也应该是一个迭代对象(with length) 具有下面 sub-elements (2 formats are possible)

    * [datetime, size, price] or [datetime, size, price, data]
    > it must be sorted (or produce sorted elements) by datetime ascending

    这里:   
    `datetime` is a python date/datetime instance or a string with format YYYY-MM-DD[THH:MM:SS[.us]] where the elements in brackets are optional

    `size` is an integer (positive to buy, negative to sell)

    `price` is a float/integer

    `data` if present can take any of the following values

        `None` - The 1st data feed will be used as target

        `integer` - The data with that index (insertion order in Cerebro) will be used

        `string` - a data with that name, assigned for example with cerebro.addata(data, name=value), will be the target

* `notify` (default: `True`)    
If True the 1st strategy inserted in the system will be notified of the artificial orders created following the information from each order in orders
如果为True, 系统中插入的第1个策略将被通知从每个订单按顺序下来的人工订单的信息

> 注意  
> 描述中隐含的是需要添加作为订单目标的data feed。例如，这需要分析器跟踪收益