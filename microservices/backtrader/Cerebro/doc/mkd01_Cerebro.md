- [Cerebro](#cerebro)
  - [Gathering input](#gathering-input)
  - [Execute the backtesting](#execute-the-backtesting)
    - [Standard Observers](#standard-observers)
  - [Returning the results](#returning-the-results)
  - [Giving access to the plotting facilities](#giving-access-to-the-plotting-facilities)
  - [Backtesting logic](#backtesting-logic)
- [Reference](#reference)
- [Cerebro - Memory Savings](#cerebro---memory-savings)
- [Cerebro - Optimization - Improvements](#cerebro---optimization---improvements)
- [Cerebro - Exceptions](#cerebro---exceptions)
- [Logging - Writer](#logging---writer)
---------------------------------------------------
# Cerebro
该类是 backtrader 的基石，因为它是以下方面的核心点：

1. 收集所有的 inputs（data feeds），actors（Stratgegies），spectators （Observers），critics（Analyzers）和 documenters （Writers）, 确保整个系统在任何时刻正常运转。
2. 执行回测/或实时 data feeding/trading
3. 返回结果
4. 对接绘图组件

## Gathering input
1. 创建一个 `cerebro`:
    ```
    cerebro = bt.Cerebro(**kwargs)
    ```
    参数 `**kwargs` 控制执行, 查看引用文档(同样的参数也可以被 `run` 方法使用)

2. 添加 Data Feeds
    通用模式是 `cerebro.adddata(data)`, 这里 data 是一个已经实例化的 data feed, 比如:
    ```
    data = bt.BacktraderCSVData(dataname='mypath.days', timeframe=bt.TimeFrame.Days)
    cerebro.adddata(data)
    ```
    Resampling 和 Replaying 遵循以下这种模式:
    ```
    data = bt.BacktraderCSVData(dataname='mypath.min', timeframe=bt.TimeFrame.Minutes)
    cerebro.resampledata(data, timeframe=bt.TimeFrame.Days)
    ```
    或
    ```
    data = bt.BacktraderCSVData(dataname='mypath.min', timeframe=bt.TimeFrame.Minutes)
    cerebro.replaydatadata(data, timeframe=bt.TimeFrame.Days)
    ```
    该系统可以接受任何数量的 data feeds，包括将常规数据做 `resample和`/或 `replay` 的数据组合。当然，这些组合中的某些组合肯定会毫无意义，并且为了能够组合数据而施加了限制：时间对其。请参阅` Data - Multiple Timeframes`, `Data Resampling - Resampling` 和 `Data - Replay` 部分。

3. 添加策略
    与添加 data feeds 不同的是, `cerebro` 添加策略不需要实例化策略类, 直接将 Strategy class 作为参数传入. 背后的原因是在做参数优化的时候, class 可以被多次实例化, 然后传入不同的参数

    即使没有优化过程, 这种模式依然如此应用:
    ```
    cerebro.addstrategy(MyStrategy, myparam1=value1, myparam2=value2)
    ```

    当需要优化参数时, 详细参见 Optimization 部分, 基本模式为:
    ```
    cerebro.optstrategy(MyStrategy, myparam1=range(10, 20))
    ```
    运行 `MyStrategy` 10次, 参数 `myparam1` 变化从10到19

4. 其他要素 
    还有些其他可以追加的元素以提升回测体验, 详细请查阅相关章节, 这些方法是:
    * `addwriter`
    * `addanalyzer`
    * `addobserver` (or `addobservermulti`)

5. 修改 `broker`
    Cerebro 使用 backtrader 提供的默认 broker, 但是可以被重写
    ```
    broker = MyBroker()
    cerebro.broker = broker  # property using getbroker/setbroker methods
    ```

6. 接收通知(notifications)
    如果 data feeds 还有 brokers 发送通知(或者 一个 store 提供者), 他们将通过 `Cerebro.notify_store` 方法接收. 有三种方式使用这些通知
    
    * 在 cerebro 实例中添加一个 callback, 使用 `addnotifycallback(callback)`. callback函数签名如下:
        ```
        callback(msg, *args, **kwargs)
        ```

    接收到的 `msg, *args, **kwargs` 应该被定义好(完全根据 `data`/`broker`/`store`), 但是通常不要指望他们能打印出允许接收的东西.
    
    * 重写 `Strategy` 子类中的 `notify_store` 方法, 签名如下:
        ```
        notify_store(self, msg, *args, **kwargs)
        ```

    * 重写 Cerebro 子类中的 `notify_store` 方法, 签名同上   
    **这是最不推荐的方法**

## Execute the backtesting
有个单独方法启动回测, 也支持一些选项(在实例化的时候设置)确定如何 run
```
result = cerebro.run(**kwargs)
```
具体参数请查阅后面的文档

### Standard Observers
如果没有特意指定, `cerebro`自动实例化3个标准的 observers:

* 一个 Broker observer 跟踪 cash 和 value(portfolio)
* 一个 Trades observer 可以显示每次 trade 的影响
* 一个 Buy/Sell observer 记录执行操作

设置参数 `stdstats=False`, 可以使绘图更加干净

## Returning the results
`cerebro` 返回回测中创建的策略实例, 可以对其进行分析, 因为所有在策略中的要素都是可以访问的:
```
result = cerebro.run(**kwargs)
```
根据是否做参数优化(用 `optstrategy` 方法添加策略), `run` 返回的 `result` 会有不同:

* 通过 `addstrategy` 添加的所有策略
    `result` 是一个 list, 里面元素是回测中策略的实例

* 通过 `optstrategy` 添加1个或更多策略
    `result` 是一个 list 的 list, 内层list是回测中优化策略的实例

> 优化的默认行为被更改为只返回系统中存在的分析器，以使计算机内核之间的消息传递变得更轻。

## Giving access to the plotting facilities
画图的话:
```
cerebro.plot()
```
详细请查看 Plotting 部分文档

## Backtesting logic
大致流程如下:

1.  传递 store notification
   
2.  让 data feed 传 下一组 ticks/bars
    
    * 版本变更: version 1.9.0.99 之后新模式:  
        data feeds 通过即将提供的下一组可用数据的 datetime 进行同步. 在新的周期中, 还没有进行交易的 feeds 依然可以提供旧数据点, 有新数据的 data feeds (与指标计算一同) 也提供旧数据

    * 旧模式(Cerebro 使用参数 oldsync=True 保留)
        第1个插入到系统的数据是 `datamaster` ，系统将等待它传出1个tick

        其他data feeds 或多或少是 `datamaster` 和的奴隶：

        ```
        * 如果下一个即将传出的 tick 比 datamaster 传出的还新(datetime-wise判断), 那么下一个tick将不会被传出

        * 可能由于一些原因没有传一个新的tick而返回退出
        ```
    这里的逻辑被设计的更加容易同步多个 data feeds 和 多个不同 timeframe 的data feeds

3.  通知到 strategies 关于 队列中的 broker 的 orders, trades 和 cash/value 的 notification

4.  告知 broker 接收 orders 队列, 同时根据最新的 data, 执行等待中的 orders

5.  调用策略中的 next 方法, 让策略评估新的数据(可能分发broker队列中的 orders)
    
    在策略/指标满足最小周期要求之前, 执行 prenext 或者 nextstart

    策略内部还运行着 observers, indicators, analyzers 和 其他活动的元素

6.  告知 writers 记录 data 到相应目标中

> 上面步骤1, 当data feeds传出组新的bars, 那些 bars 是 closed, 意味着数据已经发生了

因此，步骤4中由策略发出的订单, 无法使用步骤中1的数据去执行。

这意味着订单将以 x + 1 的概念执行。x时刻的bar生成order, x + 1 下一个时刻是执行订单的最早时刻

----------------------------------------------------
# [Reference](./mkd02_Reference.md)
# [Cerebro - Memory Savings](./mkd03_Memory_Savings.md)
# [Cerebro - Optimization - Improvements](./mkd04_Optimization.md)
# [Cerebro - Exceptions](./mkd05_Exceptions.md)
# [Logging - Writer](mkd06_Logging_Writer.md)