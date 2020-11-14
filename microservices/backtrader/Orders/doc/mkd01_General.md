- [Orders](#orders)
- [Order creation](#order-creation)
- [Order notification](#order-notification)
- [Order Status values](#order-status-values)
- [Reference: Order and associated classes](#reference-order-and-associated-classes)
  - [class backtrader.order.Order()](#class-backtraderorderorder)
    - [Member Attributes:](#member-attributes)
    - [User Methods:](#user-methods)
  - [class backtrader.order.OrderData()](#class-backtraderorderorderdata)
    - [Member Attributes:](#member-attributes-1)
  - [class backtrader.order.OrderExecutionBit()](#class-backtraderorderorderexecutionbit)
    - [Member Attributes:](#member-attributes-2)
- [Orders - Creation/Execution](#orders---creationexecution)
- [Orders - Target Orders](#orders---target-orders)
- [Orders - OCO](#orders---oco)
- [Orders - Brackets](#orders---brackets)
- [Orders - Future-Spot Compensation](#orders---future-spot-compensation)
- [Orders - StopTrail](#orders---stoptrail)

---------------------------------------------------
# Orders
Cerebro 是 backtrader 整个系统的关键控制，策略（子类）是用户的关键控制点。后者需要一种链接到系统其他部分的方法，而这正是订单发挥关键作用的地方。

订单将策略中所做的逻辑决策转换为适合 broker 执行操作的消息。这是通过：

* Creation  
    通过策略的方法:buy，sell和close(策略)返回一个order实例作为引用

* Cancellation  
    通过策略的方法：cancel（Strategy）取一个订单实例进行操作

同时，这些 orders 还作为一种通信方式返回给用户，以通知 broker 程序中的运行情况。

* Notification      
    策略的方法:notify_order(策略), 报告一个订单实例


# Order creation
调用“买入”、“卖出”和“关闭”时，以下参数适用于创建：

* `data` (default: `None`)

    必须为其选择创建订单的数据。如果没有，那么系统中的第一个数据，`self.datas[0]` or `self.data0`(又名`self.data`)将被使用

* `size` (default: `None`)

    订单使用的数据单位的 size (正)。
    
    如果为 `None`，那么通过 `getsizer` 获取的 `sizer` 实例将用于确定 `size`。

* `price` (default: `None`)

    使用的价格（如果实际格式不符合最小 tick size 要求，live brokers 可能会对输入格式进行限制）

    对 `Market` 和 `Close` 交易指令无效(市场决定价格)

    对于 `Limit`, `Stop` 和 `StopLimit` 订单，这个值决定了触发点(在Limit的情况下，触发点显然是该指令应该匹配的价格)。

* `plimit` (default: `None`)

    仅适用于 `StopLimit` 指令。一旦止损(`Stop`)被触发，这就是设定隐含的限价指令的价格（已使用 `price`）

* `exectype` (default: `None`)

    可能的值:

    * `Order.Market` or `None`       
    一个 Market 订单将以下一个可用价格执行。在回溯测试中，它将是下一个 bar 的开盘价

    * `Order.Limit`        
    只能以给定价格或更好价格执行的订单

    * `Order.Stop`      
    当订单触发到这个价格的时候，按照 `Order.Market` 一样成交。

    * `Order.StopLimit`     
    一种以价格触发并以隐含的限价指令的形式执行的指令，价格由`pricelimit` 给出

* `valid` (default: `None`)

    可能的值:

    * `None`      
    这将生成一个不会过期的订单(也被称为 Good till cancel)，并且在匹配或取消之前保持在市场中。在现实中，broker 往往会设定一个时间限制，但这通常是如此遥远，以至于认为它不会到期


    * `datetime.datetime` or `datetime.date` instance       
    该日期将用于生成在给定日期之前有效的订单(也称为good till date)


    * `Order.DAY` or `0` or `timedelta()`       
    将产生在会话结束前的单日有效订单(又名 day order)

    * `numeric value`       
    假设该值对应 `matplotlib` 编码中的日期时间(backtrader使用的日期)，并将用于生成在该日期之前有效的订单(good till date)

* `tradeid` (default: 0)
    
    这是backtrader应用的一个内部值，用于跟踪同一资产上的重叠交易。当通知订单状态的更改时，这个 `tradeid` 被发送回策略。

* `**kwargs`

    其他 broker 实现可能支持额外的参数。backtrader将把 kwargs 传递到创建的 order 对象中

    示例：如果backtrader直接支持的4种订单执行类型还不够，在IB的例子中，可以将以下内容作为 kwargs 传递：
    ```
    orderType='LIT', lmtPrice=10.0, auxPrice=9.8
    ```
    这将覆盖backtrader创建的设置，并生成一个触及价格为9.8、限价为10.0的限价单。

> 注意!     
> 平仓 `close` 方法将检查当前头寸 `position`，并相应地使用买入或卖出来有效地平仓。`size` 也将自动计算，除非参数是用户的输入，在这种情况下可以实现部分关闭或反转


# Order notification
为了接收通知，`notify_order` 方法必须在user子类策略中被重写（默认行为是什么都不做）。以下内容适用于这些通知：

* 在调用策略的 `next` 方法之前发出

* 在同一个的 next 循环中，可能会对同一订单以相同或不同状态发生多次（并将发生多次）. 一个订单可以被提交到 broker 并被接受, 其执行完成将发生在 `next` 被再次调用之前. 这个例子中至少发生3个notification, 带着以下这些 status 值:
  * `Order.Submitted`: 因为订单已经被发送给 broker
  * `Order.Accepted`: 因为订单已经由 broker 接手，等待下一步执行
  * `Order.Completed`: 因为在这个例子中，它很快就被匹配并完全完成了交易（市场订单通常就是这样）

对于 `Order.Partial`，相同状态的通知可能会发生几次(部分成交)。这个状态在回测中是看不到的（匹配时不考虑 `volume`），但是它肯定由真实的 brokers 设置。

实际的 `broker` 可能会在更新 `position` 之前执行一次或多次，这组执行将构成 `Order.Partial` 的通知。

实际执行的数据在属性中：`order.executed` 是一个 `OrderData` 对象（参见下面的引用），通常包含 `size` 与 `price` 字段。

创建时的值存储在 `order.created`, 在订单的整个生命周期中保持不变

# Order Status values

* `Order.Created`: 在Order创建实例时设置。最终用户不可见，除非 order 手动创建，而不是通过实例 `buy`, `sell` 和 `close`

* `Order.Submitted`: 当 order 实例传输到broker时设置。这仅表示它已发送。在回测模式中，这将是一个瞬间的动作，但它可能采用真实的 broker 的实际时间，当已经被转发到交易所时, 可以收到订单，只有第一个会通知

`Order.Accepted`: broker 已收到订单，并且已在系统中（或已经在交易所中）根据设置的参数（例如执行类型，size，price 和 valid）等待执行

`Order.Partial`: order已部分执行。order.executed包含当前的填报的 size 和 平均价格。

`order.executed.exbits` 包含 ExecutionBits 详细列出部分填报的完整列表

`Order.Complete`:已完全填报的平均价格。

`Order.Rejected`: broker已拒绝订单。参数 valid 可能不会被 broker 接受（例如确定其有效生命期），order不能被接受

将通过策略的 `notify_store` 方法通知原因。尽管这看起来很尴尬，但现实中 broker 会在事件发生时通知此情况，该事件可能与订单无关。但仍可以在 `notify_store` 中看到来自 broker 的通知。

此状态在 backtesting broker 中是看不到的

`Order.Margin`: 订单执行将暗示追加保证金(margin call)，并且先前接受的订单已从系统中删除

`Order.Cancelled` (or `Order.Canceled`): 确认用户请求取消

必须考虑到，通过策略的 `cancel` 方法请求取消订单 是不能保证一定会取消的。订单可能已经执行，但 broker 可能尚未通知该执行 或 通知可能尚未传递给策略

`Order.Expired`: 具有时间有效性的先前已被接受的订单过期，并已从系统中删除

# Reference: Order and associated classes
这些对象是backtrader生态系统中的通用类。与其他 broker 一起操作时，它们可能会扩展包含额外的嵌入信息。请参阅相应broker文档

## class backtrader.order.Order()
```
class backtrader.order.Order()
```
该类包含 creation/execution 数据, 还有 order 类型

order可能有以下这些状态:

* `Submitted`: 发送到 broker 并等待确认

* `Accepted`: 被 broker 接收

* `Partial`: 部分执行

* `Completed`: 全部执行

* `Canceled/Cancelled`: 用户取消

* `Expired`: 过期

* `Margin`: 没有足够 cash 执行 order 

* `Rejected`: 被broker拒绝

    这可能发生在提交订单的过程中（因此，订单将不会达到“接受”状态）或在执行每个新的 bar price 之前，这是因为其他来源提取了现金（类似未来的指令可能减少了现金或订单已经被执行了）

### Member Attributes:

`ref`: unique order identifier

`created`: OrderData holding creation data

`executed`: OrderData holding execution data

`info`: 通过 `addinfo()` 方法传递的自定义信息。它以`OrderedDict`的形式保存，该类已被子类化，因此也可以使用 “. ” 指定符号

### User Methods:

`isbuy()`: returns bool indicating if the order buys

`issell()`: returns bool indicating if the order sells

`alive()`: returns bool if order is in status Partial or Accepted


## class backtrader.order.OrderData()
```
class backtrader.order.OrderData(dt=None, size=0, price=0.0, pricelimit=0.0, remsize=0, pclose=0.0, trailamount=0.0, trailpercent=0.0)
```
保留用于创建和执行的实际订单数据。

在创建的情况下，发出请求，在执行的情况下，产生实际结果。

### Member Attributes:

* `exbits` : iterable of OrderExecutionBits for this OrderData

* `dt`: datetime (float) creation/execution time

* `size`: requested/executed size

* price: 执行价格注意, 如果未给出价格且未给出 `pricelimit`，则以当时或创建订单时的收盘价为参考

* `pricelimit`: 保存 `StopLimit` 的价格限制（先触发）

* `trailamount`: 追踪止损中的绝对价格距离

* `trailpercent`: 追踪止损中的百分比价格距离

* `value`: market value for the entire bit size

* `comm`: commission for the entire bit execution

* `pnl`: pnl generated by this bit (if something was closed)

* `margin`: 订单产生的保证金 margin（如果有）

* `psize`: current open position size

* `pprice`: current open position price


## class backtrader.order.OrderExecutionBit()
```
class backtrader.order.OrderExecutionBit(dt=None, size=0, price=0.0, closed=0, closedvalue=0.0, closedcomm=0.0, opened=0, openedvalue=0.0, openedcomm=0.0, pnl=0.0, psize=0, pprice=0.0)
```
旨在保存有关订单执行的信息。“位”不能确定订单是否已全部/部分执行，它只是保存信息。

### Member Attributes:

* `dt`: datetime (float) execution time

* `size`: how much was executed

* `price`: execution price

* `closed`: how much of the execution closed an existing postion

* `opened`: how much of the execution opened a new position

* `openedvalue`: market value of the “opened” part

* `closedvalue`: market value of the “closed” part

* `closedcomm`: commission for the “closed” part

* `openedcomm`: commission for the “opened” part

* `value`: market value for the entire bit size

* `comm`: commission for the entire bit execution

* `pnl`: pnl generated by this bit (if something was closed)

* `psize`: current open position size

* `pprice`: current open position price


# [Orders - Creation/Execution](./mkd02_Creation_Execution.md)
# [Orders - Target Orders](./mkd03_Target_Orders.md)
# [Orders - OCO](./mkd04_OCO.md)
# [Orders - Brackets](./mkd05_Brackets.md)
# [Orders - Future-Spot Compensation](./mkd06_Future_Spot_Compensation.md)
# [Orders - StopTrail](./mkd07_StopTrail.md)